from langchain_community.document_loaders import PyPDFLoader
from langgraph.graph import StateGraph

# -----------------------------
# LOAD PDF
# -----------------------------
loader = PyPDFLoader("data/support.pdf")
documents = loader.load()

# -----------------------------
# LINE-BASED CHUNKING
# -----------------------------
chunks = []
for doc in documents:
    lines = doc.page_content.split("\n")
    for line in lines:
        if line.strip():
            chunks.append(line.strip())

# -----------------------------
# SMART RETRIEVAL
# -----------------------------
def retrieve_chunks(query):
    query = query.lower()

    for i, chunk in enumerate(chunks):
        text = chunk.lower()

        if "refund" in query and "refund" in text:
            return [chunk + " " + (chunks[i+1] if i+1 < len(chunks) else "")]
        
        if "return" in query and "return" in text:
            return [chunk + " " + (chunks[i+1] if i+1 < len(chunks) else "")]
        
        if "cancel" in query and ("cancel" in text or "cancellation" in text):
            return [chunk + " " + (chunks[i+1] if i+1 < len(chunks) else "")]
        
        if "delivery" in query and "deliver" in text:
            return [chunk + " " + (chunks[i+1] if i+1 < len(chunks) else "")]
        
        if "payment" in query and "payment" in text:
            return [chunk + " " + (chunks[i+1] if i+1 < len(chunks) else "")]
        
        if "support" in query and "support" in text:
            return [chunk + " " + (chunks[i+1] if i+1 < len(chunks) else "")]

    return []

# -----------------------------
# GENERATE ANSWER
# -----------------------------
def generate_answer(query):
    docs = retrieve_chunks(query)

    if not docs:
        return "NO_CONTEXT"

    return docs[0]

# -----------------------------
# CONFIDENCE CHECK
# -----------------------------
def check_confidence(answer):
    if answer == "NO_CONTEXT":
        return "HUMAN"
    return "OK"

# -----------------------------
# GRAPH NODES
# -----------------------------
def process_node(state):
    answer = generate_answer(state["query"])
    return {"query": state["query"], "answer": answer}

def decision_node(state):
    decision = check_confidence(state["answer"])
    return {**state, "decision": decision}

def human_node(state):
    print("\n⚠️ Escalated to Human Support")
    human = input("Enter manual response: ")
    return {**state, "answer": human}

def output_node(state):
    return state

# -----------------------------
# GRAPH WORKFLOW
# -----------------------------
graph = StateGraph(dict)

graph.add_node("process", process_node)
graph.add_node("decision", decision_node)
graph.add_node("human", human_node)
graph.add_node("output", output_node)

graph.set_entry_point("process")
graph.add_edge("process", "decision")

def route(state):
    return "human" if state["decision"] == "HUMAN" else "output"

graph.add_conditional_edges("decision", route)
graph.add_edge("human", "output")

app = graph.compile()

# -----------------------------
# RUN LOOP
# -----------------------------
while True:
    query = input("\nAsk your question (type 'exit' to quit): ")

    if query.lower() == "exit":
        break

    result = app.invoke({"query": query})
    print("\nAnswer:", result["answer"])