import requests

url = "http://localhost:8001/conversational-flow"
data = {"user_input": "Hello"}
response = requests.post(url, json=data)

print(response.status_code, response.text)