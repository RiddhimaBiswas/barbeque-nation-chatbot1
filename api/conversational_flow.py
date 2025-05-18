from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
import httpx

# Import state prompts and transitions
from state_prompts import STATE_PROMPTS, STATE_TRANSITIONS

# Load environment variables from .env
load_dotenv()
RETELL_AI_API_KEY = os.getenv("RETELL_AI_API_KEY")

app = FastAPI()

# CORS configuration
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:8001",
    "https://barbeque-nation-chatbot.vercel.app",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cities and areas available in the knowledge base
AVAILABLE_CITIES = {
    "delhi": ["Janakpuri", "Vasant Kunj"],
    "bangalore": ["Indiranagar", "JP Nagar", "Electronic City"]
}

@app.get("/")
def read_root():
    return {"message": "Server is running!"}

@app.post("/conversational-flow")
async def handle_conversation(request: Request):
    try:
        data = await request.json()
        user_input = data.get("user_input", "")
        current_state = data.get("current_state", "greeting")
        entities = data.get("entities", {})

        print(f"Received user_input: {user_input}, current_state: {current_state}, entities: {entities}")

        # Retrieve prompt template for current state
        state_config = STATE_PROMPTS.get(current_state)
        if not state_config:
            return {"error": f"Unknown state: {current_state}"}

        # Initialize prompt and next state
        prompt = state_config["prompt"]
        ai_reply = None
        next_state = current_state

        # Handle specific intents from option buttons
        user_input_lower = user_input.lower()
        if "menu" in user_input_lower:
            async with httpx.AsyncClient(timeout=10) as client:
                try:
                    kb_response = await client.post(
                        "https://barbeque-nation-knowledge-base.onrender.com/knowledge-base/query",
                        json={"city": entities.get("city", "bangalore"), "question": "menu"}
                    )
                    kb_response.raise_for_status()
                    information = kb_response.json().get("answer", "No menu information available.")
                except Exception as e:
                    print(f"Knowledge Base API error: {e}")
                    information = "Sorry, I couldn't retrieve the menu at this time."
            entities["information"] = information
            prompt = f"Here is the menu information: {information}"
            next_state = "inform"

        elif "timings" in user_input_lower:
            city = entities.get("city")
            area = entities.get("area")
            if not city or not area:
                prompt = "I need to know which city and area you're interested in to provide the timings. Could you please tell me?"
                next_state = "collect_city"
            else:
                async with httpx.AsyncClient(timeout=10) as client:
                    try:
                        kb_response = await client.post(
                            "https://barbeque-nation-knowledge-base.onrender.com/knowledge-base/query",
                            json={"city": city, "area": area, "question": "operating hours"}
                        )
                        kb_response.raise_for_status()
                        information = kb_response.json().get("answer", "No timing information available.")
                    except Exception as e:
                        print(f"Knowledge Base API error: {e}")
                        information = "Sorry, I couldn't retrieve the timings at this time."
                entities["information"] = information
                prompt = f"Here are the timings: {information}"
                next_state = "inform"

        # Handle city collection and verification
        elif current_state == "collect_city":
            city = None
            area = None
            for c, areas in AVAILABLE_CITIES.items():
                if c in user_input_lower:
                    city = c
                    break
                for a in areas:
                    if a.lower() in user_input_lower:
                        city = c
                        area = a
                        break

            if city:
                entities["city"] = city
                if area and area in [a.lower() for a in AVAILABLE_CITIES[city]]:
                    entities["area"] = area.title()
                    prompt = f"You are looking for information about {area}, {city.title()}. Is that correct?"
                    next_state = "inform"
                else:
                    prompt = f"You are looking for information about {city.title()}. Could you please specify the area?"
                    next_state = "collect_city"
            else:
                prompt = "I'm sorry, we do not have any outlets in the area you mentioned. Would you like to know about any other area?"
                next_state = "collect_city"

        # Handle informing the user
        elif current_state == "inform":
            city = entities.get("city")
            area = entities.get("area")
            if not city or not area:
                prompt = "I need more information to proceed. Could you please tell me which city and area you're interested in?"
                next_state = "collect_city"
            else:
                async with httpx.AsyncClient(timeout=10) as client:
                    try:
                        kb_response = await client.post(
                            "https://barbeque-nation-knowledge-base.onrender.com/knowledge-base/query",
                            json={"city": city, "area": area, "question": "operating hours"}
                        )
                        kb_response.raise_for_status()
                        information = kb_response.json().get("answer", "No information available.")
                    except Exception as e:
                        print(f"Knowledge Base API error: {e}")
                        information = "Sorry, I couldn't retrieve the information at this time."
                entities["information"] = information
                prompt = state_config["prompt"].format(information=information)
                next_state = "inform"

        # Format prompt with entities if needed
        try:
            prompt = prompt.format(**{k: entities.get(k, "") for k in state_config.get("entities", [])})
        except Exception as e:
            print(f"Prompt formatting error: {e}")

        # Call Retell AI API
        headers = {
            "Authorization": f"Bearer {RETELL_AI_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8001",
            "X-Title": "Chatbot Flow"
        }

        async with httpx.AsyncClient(timeout=10) as client:
            try:
                response = await client.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    json={
                        "model": "mistralai/mistral-7b-instruct",
                        "messages": [
                            {"role": "system", "content": "You are a helpful assistant for Barbeque Nation. Provide information politely and avoid using any prohibited words or triggering external functions."},
                            {"role": "user", "content": prompt + "\n\nUser: " + user_input}
                        ]
                    }
                )
                response.raise_for_status()
                result = response.json()
                ai_reply = result["choices"][0]["message"]["content"]
            except Exception as e:
                print(f"Retell AI API error: {e}")
                ai_reply = f"(Mocked) Sorry, the AI service is unavailable. Your input was: '{user_input}'."

        # Determine next state based on transitions
        for transition in STATE_TRANSITIONS.get(current_state, []):
            if evaluate_condition(transition["condition"], user_input, data):
                next_state = transition["next_state"]
                break

        return {
            "response": ai_reply,
            "next_state": next_state,
            "entities": entities
        }

    except Exception as e:
        return {"error": "Unexpected server error", "details": str(e)}

def evaluate_condition(condition: str, user_input: str, data: dict) -> bool:
    if condition == "user_input is not empty":
        return bool(user_input.strip())
    if condition.startswith("intent == "):
        intent = condition.split("==")[1].strip().strip("'").lower()
        return intent in user_input.lower()
    if condition == "user says goodbye":
        return any(kw in user_input.lower() for kw in ["bye", "thank you", "goodbye"])
    if condition == "all booking details collected":
        entities = data.get("entities", {})
        required = ["name", "date", "time", "number_of_guests", "city"]
        return all(key in entities and entities[key] for key in required)
    if condition == "missing details":
        return not evaluate_condition("all booking details collected", user_input, data)
    if condition == "booking ID and updates provided":
        entities = data.get("entities", {})
        return "booking_id" in entities and any(k in entities for k in ["date", "time", "number_of_guests"])
    if condition == "missing booking ID":
        entities = data.get("entities", {})
        return "booking_id" not in entities
    return False

@app.get("/check-api-key")
def check_api_key():
    return {"api_key_loaded": bool(RETELL_AI_API_KEY)}

if __name__ == "__main__":
    import uvicorn
    print("⚙️  Starting FastAPI server...")
    uvicorn.run("conversational_flow:app", host="0.0.0.0", port=8001, reload=True)