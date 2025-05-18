document.addEventListener("DOMContentLoaded", () => {
    const chatWindow = document.getElementById("chat-window");
    const userInput = document.getElementById("user-input");
    const sendButton = document.getElementById("send-btn");
    const optionButtons = document.querySelectorAll(".option-btn");

    let currentState = "greeting";
    let entities = {};

    function appendMessage(sender, message) {
        const messageDiv = document.createElement("div");
        messageDiv.className = `message ${sender}-message`;
        messageDiv.textContent = message;
        chatWindow.appendChild(messageDiv);
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }

    async function sendMessage(userMessage) {
        if (!userMessage) return;

        appendMessage("user", userMessage);
        userInput.value = "";

        try {
            const response = await fetch("https://barbeque-nation-conversational-flow1.onrender.com/conversational-flow", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    user_input: userMessage,
                    current_state: currentState,
                    entities: entities
                })
            });

            const data = await response.json();
            if (data.error) {
                appendMessage("bot", `Error: ${data.error}`);
                return;
            }

            currentState = data.next_state;
            entities = data.entities || {};
            appendMessage("bot", data.response);
        } catch (error) {
            appendMessage("bot", "Sorry, something went wrong. Please try again.");
            console.error("Error:", error);
        }
    }

    // Handle text input and send button
    sendButton.addEventListener("click", (e) => {
        e.preventDefault(); // Prevent form submission
        const userMessage = userInput.value.trim();
        if (userMessage) sendMessage(userMessage);
    });

    userInput.addEventListener("keypress", (e) => {
        if (e.key === "Enter") {
            e.preventDefault(); // Prevent form submission
            const userMessage = userInput.value.trim();
            if (userMessage) sendMessage(userMessage);
        }
    });

    // Handle option buttons
    optionButtons.forEach(button => {
        button.addEventListener("click", () => {
            const userMessage = button.getAttribute("data-msg");
            sendMessage(userMessage);
        });
    });

    // Initialize conversation
    appendMessage("bot", "Hello! Welcome to Barbeque Nation. How can I assist you today?");
});