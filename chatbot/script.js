async function sendMessage() {
    const input = document.getElementById("user-input");
    const chatContainer = document.getElementById("chat-container");
    const userMessage = input.value;
    
    // Display user message
    chatContainer.innerHTML += `<p><strong>You:</strong> ${userMessage}</p>`;
    
    // Call conversational flow API
    const response = await fetch("https://barbeque-nation-chatbot1-1.onrender.com", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_input: userMessage, current_state: "greeting" })
});
    const data = await response.json();
    
    // Display bot response
    chatContainer.innerHTML += `<p><strong>Bot:</strong> ${data.response}</p>`;
    input.value = "";
    chatContainer.scrollTop = chatContainer.scrollHeight;
}