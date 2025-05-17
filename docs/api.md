API Documentation
Knowledge Base API

GET /knowledge-base/{city}

Description: Retrieves the knowledge base for a city.
Parameters:
city: String (e.g., "Delhi", "Bangalore")


Response: JSON with FAQs and booking info.
Example:GET /knowledge-base/Delhi
Response: { "city": "Delhi", "faqs": [...], "booking_info": {...} }




POST /knowledge-base/query

Description: Queries the knowledge base for an answer.
Body:
city: String
question: String


Response: JSON with the answer.
Example:POST /knowledge-base/query
Body: { "city": "Delhi", "question": "What are the operating hours?" }
Response: { "answer": "Our Delhi branches are open from 12 PM to 11 PM daily." }





Conversational Flow API

POST /conversational-flow
Description: Processes user input and returns the response and next state.
Body:
user_input: String
current_state: String (optional, defaults to "greeting")
entities: Object (optional)


Response: JSON with response and next state.
Example:POST /conversational-flow
Body: { "user_input": "What are your hours?", "current_state": "greeting" }
Response: { "response": "Our Delhi branches are open from 12 PM to 11 PM daily.", "next_state": "faq_handling" }





