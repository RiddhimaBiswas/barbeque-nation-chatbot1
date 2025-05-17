# State Prompt Templates
STATE_PROMPTS = {
    "greeting": {
        "prompt": "Hello! Welcome to Barbeque Nation. How can I assist you today? You can ask about our menu, make a booking, or update an existing reservation.",
        "entities": [],
        "tools": ["knowledge_base_query"]
    },
    "identify_intent": {
        "prompt": "Based on the user's input: '{user_input}', classify the intent as one of: FAQ, New_Booking, Update_Booking, Cancel_Booking. If unclear, ask: 'Could you clarify if you want to ask a question, make a booking, update a booking, or cancel one?'",
        "entities": ["user_input"],
        "tools": []
    },
    "faq_handling": {
        "prompt": "Using the knowledge base, answer the user's question: '{user_input}' about Barbeque Nation's services in {city}. If no answer is found, say: 'I'm sorry, I don't have that information. Can I help with something else?'",
        "entities": ["user_input", "city"],
        "tools": ["knowledge_base_query"]
    },
    "new_booking": {
        "prompt": "To create a new booking, please provide: Name, Date, Time, Number of Guests, and City (Delhi or Bangalore). Current details collected: {booking_details}. What's the next detail?",
        "entities": ["booking_details"],
        "tools": ["booking_api"]
    },
    "update_booking": {
        "prompt": "To update your booking, please provide your Booking ID and the details to update (e.g., Date, Time, Guests). Current details: {booking_details}. What's the Booking ID or updated detail?",
        "entities": ["booking_details"],
        "tools": ["booking_api"]
    },
    "cancel_booking": {
        "prompt": "To cancel your booking, please provide your Booking ID. Current details: {booking_details}. What's the Booking ID?",
        "entities": ["booking_details"],
        "tools": ["booking_api"]
    },
    "confirm_booking": {
        "prompt": "Booking confirmed! Details: {booking_details}. Would you like to make another booking or ask something else?",
        "entities": ["booking_details"],
        "tools": []
    },
    "confirm_update": {
        "prompt": "Booking updated! Updated details: {booking_details}. Can I assist with anything else?",
        "entities": ["booking_details"],
        "tools": []
    },
    "confirm_cancellation": {
        "prompt": "Booking cancelled for Booking ID: {booking_details}. Can I assist with anything else?",
        "entities": ["booking_details"],
        "tools": []
    },
    "end": {
        "prompt": "Thank you for contacting Barbeque Nation. Have a great day!",
        "entities": [],
        "tools": []
    }
}

# State Transition Prompts
STATE_TRANSITIONS = {
    "greeting": [
        {"condition": "user_input is not empty", "next_state": "identify_intent"}
    ],
    "identify_intent": [
        {"condition": "intent == 'FAQ'", "next_state": "faq_handling"},
        {"condition": "intent == 'New_Booking'", "next_state": "new_booking"},
        {"condition": "intent == 'Update_Booking'", "next_state": "update_booking"},
        {"condition": "intent == 'Cancel_Booking'", "next_state": "cancel_booking"},
        {"condition": "intent is unclear", "next_state": "identify_intent"}
    ],
    "faq_handling": [
        {"condition": "user asks another question", "next_state": "faq_handling"},
        {"condition": "user wants to book", "next_state": "new_booking"},
        {"condition": "user wants to update", "next_state": "update_booking"},
        {"condition": "user wants to cancel", "next_state": "cancel_booking"},
        {"condition": "user says goodbye", "next_state": "end"}
    ],
    "new_booking": [
        {"condition": "all booking details collected", "next_state": "confirm_booking"},
        {"condition": "missing details", "next_state": "new_booking"}
    ],
    "update_booking": [
        {"condition": "booking ID and updates provided", "next_state": "confirm_update"},
        {"condition": "missing details", "next_state": "update_booking"}
    ],
    "cancel_booking": [
        {"condition": "booking ID provided", "next_state": "confirm_cancellation"},
        {"condition": "missing booking ID", "next_state": "cancel_booking"}
    ],
    "confirm_booking": [
        {"condition": "user wants another booking", "next_state": "new_booking"},
        {"condition": "user asks question", "next_state": "faq_handling"},
        {"condition": "user says goodbye", "next_state": "end"}
    ],
    "confirm_update": [
        {"condition": "user wants another action", "next_state": "identify_intent"},
        {"condition": "user says goodbye", "next_state": "end"}
    ],
    "confirm_cancellation": [
        {"condition": "user wants another action", "next_state": "identify_intent"},
        {"condition": "user says goodbye", "next_state": "end"}
    ]
}