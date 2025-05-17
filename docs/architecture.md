Architecture Documentation
System Overview
The Barbeque Nation Chatbot Agent is a conversational AI system for handling enquiries and bookings for Barbeque Nation properties in Delhi and Bangalore. Components include:

State Machine: Manages conversational flow using state prompts and transitions.
Knowledge Base: JSON files with FAQs and booking info.
API Layer: FastAPI endpoints for knowledge base and conversational flow.
Chatbot Frontend: Web-based UI for user interaction.
Post-Call Analysis: Generates Excel reports from logs.

Architecture Diagram
[User] <--> [Chatbot Frontend / Phone]
             |
     [Conversational Flow API]
             |
[State Machine] <--> [Knowledge Base API]
             |
       [Retell AI Platform]
             |
     [Post-Call Analysis]

Component Interaction

Users interact via the frontend or phone.
The conversational flow API processes input, uses the state machine, and queries Retell AI.
The knowledge base API answers FAQs.
Post-call analysis generates reports.

