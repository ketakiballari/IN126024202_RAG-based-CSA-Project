# RAG-Based Customer Support Assistant

This project implements a Retrieval-Augmented Generation (RAG) based customer support system using LangGraph with Human-in-the-Loop (HITL).

## Overview

The system answers user queries using a PDF knowledge base. It retrieves relevant information and returns accurate responses. If no relevant answer is found, the query is escalated to a human.

## Key Features

* Document-based Question Answering
* Retrieval-Augmented Generation (RAG) pipeline
* Workflow orchestration using LangGraph
* Human-in-the-Loop (HITL) escalation
* Command-Line Interface for interaction

## Architecture

The system follows a structured pipeline:

User → Document Processing → Retrieval → Decision → Output / Human

## Technologies Used

* Python
* LangGraph
* PyPDFLoader
* Basic Retrieval Logic

## How It Works

1. Load PDF document
2. Split into chunks
3. Retrieve relevant information based on query
4. Return answer or escalate to human

## Example Queries

* What is refund policy?
* How to cancel order?
* What are payment methods?

## Future Improvements

* Integrate vector database (ChromaDB)
* Use LLMs for better response generation
* Build web-based interface
* Add conversational memory


