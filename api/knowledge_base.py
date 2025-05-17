from fastapi import FastAPI, HTTPException
import json

app = FastAPI()

# Load knowledge base
with open("knowledge_base/delhi.json", "r") as f:
    delhi_kb = json.load(f)
with open("knowledge_base/bangalore.json", "r") as f:
    bangalore_kb = json.load(f)

@app.get("/knowledge-base/{city}")
async def get_knowledge_base(city: str):
    if city.lower() == "delhi":
        return delhi_kb
    elif city.lower() == "bangalore":
        return bangalore_kb
    else:
        raise HTTPException(status_code=404, detail="City not found")

@app.post("/knowledge-base/query")
async def query_knowledge_base(request: dict):
    city = request.get("city")
    question = request.get("question")
    kb = delhi_kb if city.lower() == "delhi" else bangalore_kb
    for faq in kb["faqs"]:
        if question.lower() in faq["question"].lower():
            return {"answer": faq["answer"]}
    return {"answer": "I'm sorry, I don't have that information. Can I help with something else?"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)