# barbeque-nation-chatbot1
# 🍽️ Barbeque Nation Conversational AI Agent

This repository contains the full implementation of the **Inbound Enquiry and Booking Chatbot Agent** for Barbeque Nation. The agent answers FAQs, handles new bookings, and manages updates or cancellations for restaurant properties in **Delhi** and **Bangalore**.

---

## 🧠 Purpose

To automate customer interaction through a conversational AI chatbot which:
- Answers frequently asked questions
- Takes new booking requests
- Modifies or cancels existing reservations

---

## 🧱 System Architecture

### 1. **State Machine (Conversational Flow)**
- Implemented using `beta.retellai.com`
- One state active per interaction
- Follows FSM model for transitions

### 2. **State Prompts**
- Each state has a specific role (e.g., `Greeting`, `FAQ_Answer`, `Book_Table`, `Cancel_Booking`)
- Template-based with variable injection

### 3. **State Transition Prompts**
- Conditional logic to guide conversation
- Checks completion status before moving to the next state

### 4. **Knowledge Base**
- Structured JSON containing FAQ, booking, and cancellation data for:
  - **Delhi**
  - **Bangalore**
- Queried by the chatbot to provide contextual responses

### 5. **Post-Call Configuration** ✅ (Bonus)
- Logs user satisfaction, completion status, and booking info
- Exported as Excel for business analytics

### 6. **Chatbot UI** ✅ (Bonus)
- React-based frontend (open source template)
- Backend in Flask (API connection to state machine + knowledge base)
- Hosted for testing and demonstration

---

## 🚀 Live Demo

🔗 **Chatbot Link**: [https://barbeque-chatbot-demo.vercel.app](https://barbeque-chatbot-demo.vercel.app)  
📱 **Agent Linked Phone Number**: `+91-XXXXXXXXXX`

---

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/faq/<city>` | GET | Returns FAQs for selected city |
| `/book` | POST | Accepts new table booking |
| `/cancel` | POST | Cancels or updates existing booking |
| `/state_transition` | POST | Drives the state machine transition |
| `/post_call_analysis` | GET | Exports call analytics (CSV/XLSX) |

---

## 📁 File Structure

