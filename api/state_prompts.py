# State Prompt Templates
STATE_PROMPTS = {
    "greeting": {
        "prompt": "Hello! Welcome to Barbeque Nation. How can I assist you today?"
    },
    "collect_city": {
        "prompt": "I need to know which city and area you're interested in to provide the timings. Could you please tell me?"
    },
    "inform": {
        "prompt": "Here is the information you requested: {information}"
    },
    "goodbye": {
        "prompt": "Thank you for contacting Barbeque Nation. Have a great day!"
    }
}

STATE_TRANSITIONS = {
    "greeting": [
        {"condition": "user_input is not empty", "next_state": "collect_city"},
        {"condition": "user says goodbye", "next_state": "goodbye"}
    ],
    "collect_city": [
        {"condition": "user_input is not empty", "next_state": "inform"},
        {"condition": "user says goodbye", "next_state": "goodbye"}
    ],
    "inform": [
        {"condition": "user says goodbye", "next_state": "goodbye"},
        {"condition": "user_input is not empty", "next_state": "collect_city"}
    ]
}