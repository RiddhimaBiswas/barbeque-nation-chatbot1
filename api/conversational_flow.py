from fastapi import FastAPI, Request
import requests
from state_prompts import STATE_PROMPTS, STATE_TRANSITIONS
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env
RETELL_AI_API_KEY = os.getenv("RETELL_AI_API_KEY")

app = FastAPI()

@app.post("/conversational-flow")
async def handle_conversation(request: Request):
    data = await request.json()
    user_input = data.get("user_input")
    current_state = data.get("current_state", "greeting")
    entities = data.get("entities", {})
    
    state_config = STATE_PROMPTS.get(current_state)
    prompt = state_config["prompt"].format(**entities)
    
    # Retell AI integration
    headers = {
        "Authorization": f"Bearer {RETELL_AI_API_KEY}",
        "Content-Type": "application/json"
    }
    retell_response = requests.post(
        "https://beta.retellai.com/api/v1/converse",
        json={"prompt": prompt, "user_input": user_input},
        headers=headers
    ).json()
    
    next_state = current_state
    for transition in STATE_TRANSITIONS.get(current_state, []):
        if evaluate_condition(transition["condition"], user_input, data):
            next_state = transition["next_state"]
            break
    
    return {
        "response": retell_response.get("response"),
        "next_state": next_state
    }

def evaluate_condition(condition: str, user_input: str, data: dict) -> bool:
    if condition == "user_input is not empty":
        return bool(user_input)
    if condition.startswith("intent == "):
        intent = condition.split("==")[1].strip().strip("'")
        if intent.lower() in user_input.lower():
            return True
    if condition == "user says goodbye":
        return "bye" in user_input.lower() or "thank you" in user_input.lower()
    if condition == "all booking details collected":
        return "name" in data.get("entities", {}) and "date" in data.get("entities", {})
    return False

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)