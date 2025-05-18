from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import json
import os

app = FastAPI()

# Define paths to JSON files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KNOWLEDGE_BASE_DIR = os.path.join(BASE_DIR, "..", "knowledge_base")

# Load JSON files
def load_json(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

# Load city summaries and detailed area data
DELHI_KB = {
    "summary": load_json(os.path.join(KNOWLEDGE_BASE_DIR, "delhi.json")),
    "Janakpuri": load_json(os.path.join(KNOWLEDGE_BASE_DIR, "janakpuri.json")),
    "Vasant Kunj": load_json(os.path.join(KNOWLEDGE_BASE_DIR, "vasant_kunj.json"))
}

BANGALORE_KB = {
    "summary": load_json(os.path.join(KNOWLEDGE_BASE_DIR, "bangalore.json")),
    "Indiranagar": load_json(os.path.join(KNOWLEDGE_BASE_DIR, "indiranagar.json")),
    "JP Nagar": load_json(os.path.join(KNOWLEDGE_BASE_DIR, "jp_nagar.json")),
    "Electronic City": load_json(os.path.join(KNOWLEDGE_BASE_DIR, "electronic_city.json"))
}

MENU_KB = load_json(os.path.join(KNOWLEDGE_BASE_DIR, "menu.json"))

@app.get("/knowledge-base/{city}")
async def get_knowledge_base(city: str):
    """Return the summary knowledge base for the specified city."""
    if city.lower() == "delhi":
        return DELHI_KB["summary"]
    elif city.lower() == "bangalore":
        return BANGALORE_KB["summary"]
    else:
        raise HTTPException(status_code=404, detail="City not found")

@app.get("/knowledge-base/{city}/{area}")
async def get_area_details(city: str, area: str):
    """Return detailed information for a specific area in a city."""
    city = city.lower()
    area = area.title()  # Match the case used in JSON keys (e.g., "Indiranagar", "JP Nagar")
    
    if city == "delhi":
        if area in DELHI_KB:
            return DELHI_KB[area]
        else:
            raise HTTPException(status_code=404, detail=f"Area '{area}' not found in Delhi")
    elif city == "bangalore":
        if area in BANGALORE_KB:
            return BANGALORE_KB[area]
        else:
            raise HTTPException(status_code=404, detail=f"Area '{area}' not found in Bangalore")
    else:
        raise HTTPException(status_code=404, detail="City not found")

@app.get("/knowledge-base/menu")
async def get_menu():
    """Return the menu details."""
    return MENU_KB

@app.get("/post-call-analysis.xlsx")
async def get_post_call_analysis():
    """Return the post-call analysis Excel file."""
    return FileResponse("post_call_analysis.xlsx")

class Query(BaseModel):
    city: str
    question: str
    area: str = None  # Optional field for area-specific queries

@app.post("/knowledge-base/query")
async def query_knowledge_base(query: Query):
    """Handle queries about the knowledge base, including area-specific and menu queries."""
    city = query.city.lower()
    question = query.question.lower()
    area = query.area.title() if query.area else None

    # Determine the knowledge base to use
    if city == "delhi":
        kb = DELHI_KB
    elif city == "bangalore":
        kb = BANGALORE_KB
    else:
        raise HTTPException(status_code=404, detail="City not found")

    # Handle menu-related queries
    if "menu" in question or "food" in question or "drinks" in question:
        menu = MENU_KB["menu"]
        if "jain" in question:
            return {"answer": menu["jain_food"]}
        elif "halal" in question:
            return {"answer": menu["halal_food"]}
        elif "alcoholic drinks" in question or "drinks" in question:
            return {"answer": menu["alcoholic_drinks"]}
        elif "customize" in question or "customization" in question:
            return {"answer": menu["customization"]}
        elif "fish" in question:
            return {"answer": f"We serve {menu['seafood']['fish']} fish."}
        elif "prawns" in question:
            return {"answer": f"We serve {menu['seafood']['prawns']}."}
        elif "crab" in question:
            return {"answer": menu["seafood"]["crab"]}
        elif "ice cream" in question:
            return {"answer": f"We serve the following ice cream flavors: {', '.join(menu['desserts']['ice_cream'])}."}
        elif "kulfi" in question:
            return {"answer": f"We serve the following kulfi flavors: {', '.join(menu['desserts']['kulfis'])}."}
        elif "biryani" in question:
            return {"answer": menu["biryani"]}
        elif "pizza" in question:
            return {"answer": menu["pizza"]}
        elif "hukkah" in question:
            return {"answer": menu["hukkah"]}
        elif "jataka" in question:
            return {"answer": menu["jataka_food"]}
        elif "mutton" in question:
            return {"answer": menu["mutton"]}
        else:
            return {"answer": "Please specify what you'd like to know about the menu (e.g., Jain food, drinks, biryani)."}

    # Handle area-specific queries
    if area and area in kb:
        area_data = kb[area]
        if "operating hours" in question or "timings" in question:
            timings = area_data["timings"]
            response = (
                f"Timings for {area}, {city.title()}:\n"
                f"Monday to Friday - Lunch: {timings['monday_to_friday']['lunch']['opening']} to {timings['monday_to_friday']['lunch']['closing']}, "
                f"Dinner: {timings['monday_to_friday']['dinner']['opening']} to {timings['monday_to_friday']['dinner']['closing']}\n"
                f"Saturday - Lunch: {timings['saturday']['lunch']['opening']} to {timings['saturday']['lunch']['closing']}, "
                f"Dinner: {timings['saturday']['dinner']['opening']} to {timings['saturday']['dinner']['closing']}\n"
                f"Sunday - Lunch: {timings['sunday']['lunch']['opening']} to {timings['sunday']['lunch']['closing']}, "
                f"Dinner: {timings['sunday']['dinner']['opening']} to {timings['sunday']['dinner']['closing']}"
            )
            return {"answer": response}
        elif "address" in question:
            return {"answer": f"The address for {area}, {city.title()} is: {area_data['address']}"}
        elif "contact" in question or "phone" in question:
            return {"answer": f"Contact numbers for {area}, {city.title()}: {', '.join(area_data['contact_numbers'])}"}
        elif "bar" in question:
            return {"answer": f"Bar availability in {area}, {city.title()}: {area_data['availability']['bar']}"}
        elif "parking" in question:
            return {"answer": f"Parking in {area}, {city.title()}: {area_data['availability']['valet_parking']}"}
        elif "special instructions" in question or "closure" in question:
            return {"answer": area_data["special_instructions"] if area_data["special_instructions"] != "None" else "No special instructions or closures at this time."}
        else:
            return {"answer": f"I'm sorry, I don't have that specific information for {area}. Can I help with something else like timings or the menu?"}

    # Fallback for general queries using the summary FAQ (if any)
    for faq in kb["summary"].get("faqs", []):
        if question in faq["question"].lower():
            return {"answer": faq["answer"]}

    return {"answer": "I'm sorry, I don't have that information. Please specify an area or ask about the menu, timings, or contact details."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)