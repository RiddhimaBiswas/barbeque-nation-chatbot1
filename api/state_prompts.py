# State Prompt Templates
STATE_PROMPTS = {
    "greeting": {
        "prompt": "Welcome to Barbeque Nation! How can I assist you today? You can ask FAQs, book a table, update or cancel bookings.",
        "entities": []
    },
    "ask_city": {
        "prompt": "Could you please tell me which city you are interested in? We currently serve Delhi and Bangalore.",
        "entities": []
    },
    "ask_booking_type": {
        "prompt": "Are you looking to make a new booking, update an existing one, or cancel a booking?",
        "entities": []
    },
    "ask_name": {
        "prompt": "Please provide the name under which the booking should be made.",
        "entities": []
    },
    "ask_phone": {
        "prompt": "Can I get your phone number for the booking?",
        "entities": []
    },
    "ask_date_time": {
        "prompt": "Please tell me the date and time for your booking.",
        "entities": []
    },
    "ask_guests": {
        "prompt": "How many guests will be attending?",
        "entities": []
    },
    "confirm_booking": {
        "prompt": "Thank you {name}. Confirming your booking for {guests} guests on {date_time} in {city}. Is this correct?",
        "entities": ["name", "guests", "date_time", "city"]
    },
    "booking_complete": {
        "prompt": "Your booking is confirmed! We look forward to welcoming you to Barbeque Nation in {city}.",
        "entities": []
    },
    "faq": {
        "prompt": "Let me help you with that question.",
        "entities": []
    },
    "update_booking": {
        "prompt": "Please provide your booking ID and what details you'd like to update.",
        "entities": []
    },
    "cancel_booking": {
        "prompt": "Please provide your booking ID to proceed with cancellation.",
        "entities": []
    },
    "error": {
        "prompt": "Sorry, I didn't understand that. Could you please rephrase?",
        "entities": []
    }
}

STATE_TRANSITIONS = {
    "collect_city": [
        {"condition": "user_input is not empty", "next_state": "inform"},
        {"condition": "user says goodbye", "next_state": "goodbye"}
    ],
    "greeting": [
        {"condition": "user_input is not empty", "next_state": "ask_city"}
    ],
    "ask_city": [
        {"condition": "user_input in ['delhi','bangalore']", "next_state": "ask_booking_type"},
        {"condition": "user_input not in ['delhi','bangalore']", "next_state": "error"}
    ],
    "ask_booking_type": [
        {"condition": "user_input in ['new booking', 'booking']", "next_state": "ask_name"},
        {"condition": "user_input in ['update', 'modify']", "next_state": "update_booking"},
        {"condition": "user_input in ['cancel', 'cancellation']", "next_state": "cancel_booking"},
        {"condition": "else", "next_state": "error"}
    ],
    "ask_name": [
        {"condition": "user_input is not empty", "next_state": "ask_phone"}
    ],
    "ask_phone": [
        {"condition": "user_input is not empty", "next_state": "ask_date_time"}
    ],
    "ask_date_time": [
        {"condition": "user_input is not empty", "next_state": "ask_guests"}
    ],
    "ask_guests": [
        {"condition": "user_input is not empty", "next_state": "confirm_booking"}
    ],
    "confirm_booking": [
        {"condition": "user_input in ['yes', 'correct']", "next_state": "booking_complete"},
        {"condition": "user_input in ['no', 'incorrect']", "next_state": "ask_name"}
    ],
    "booking_complete": [],
    "faq": [],
    "update_booking": [],
    "cancel_booking": [],
    "error": [
        {"condition": "user_input is not empty", "next_state": "greeting"}
    ]
}
