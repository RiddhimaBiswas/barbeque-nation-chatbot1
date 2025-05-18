document.addEventListener("DOMContentLoaded", () => {
    const chatWindow = document.getElementById("chat-window");
    const userInput = document.getElementById("user-input");
    const sendButton = document.getElementById("send-btn");
    const optionButtons = document.querySelectorAll(".option-btn");

    let currentState = "greeting";
    let entities = {};

    function appendMessage(sender, data) {
        const messageDiv = document.createElement("div");
        messageDiv.className = `message ${sender}-message`;

        if (sender === "bot") {
            const typingSpan = document.createElement("span");
            typingSpan.className = "typing";
            typingSpan.textContent = "Typing...";
            messageDiv.appendChild(typingSpan);
            chatWindow.appendChild(messageDiv);
            chatWindow.scrollTop = chatWindow.scrollHeight;

            setTimeout(() => {
                messageDiv.removeChild(typingSpan);

                if (data.type === "menu") {
                    // Render structured menu
                    const menu = data.content;
                    const menuContainer = document.createElement("div");
                    menuContainer.className = "menu-container";

                    for (const [category, items] of Object.entries(menu)) {
                        const categoryDiv = document.createElement("div");
                        categoryDiv.className = "menu-category";

                        const categoryTitle = document.createElement("h3");
                        categoryTitle.textContent = category;
                        categoryDiv.appendChild(categoryTitle);

                        const itemList = document.createElement("ul");
                        items.forEach(item => {
                            const listItem = document.createElement("li");
                            listItem.textContent = item;
                            itemList.appendChild(listItem);
                        });
                        categoryDiv.appendChild(itemList);
                        menuContainer.appendChild(categoryDiv);
                    }

                    const note = document.createElement("p");
                    note.className = "menu-note";
                    note.textContent = "Please note that the menu may vary by location. For the most accurate information, contact your local Barbeque Nation restaurant.";
                    menuContainer.appendChild(note);

                    messageDiv.appendChild(menuContainer);
                } else {
                    // Render plain text
                    messageDiv.textContent = data.content;
                }

                chatWindow.scrollTop = chatWindow.scrollHeight;
            }, 1000);
        } else {
            messageDiv.textContent = data;
            chatWindow.appendChild(messageDiv);
            chatWindow.scrollTop = chatWindow.scrollHeight;
        }
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

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const data = await response.json();
            if (data.error) {
                appendMessage("bot", { type: "text", content: `Error: ${data.error}` });
                return;
            }

            currentState = data.next_state;
            entities = data.entities || {};
            appendMessage("bot", data.response);
        } catch (error) {
            appendMessage("bot", { type: "text", content: "Sorry, I'm having trouble connecting. Please try again later." });
            console.error("Error:", error);
        }
    }

    sendButton.addEventListener("click", (e) => {
        e.preventDefault();
        const userMessage = userInput.value.trim();
        if (userMessage) sendMessage(userMessage);
    });

    userInput.addEventListener("keypress", (e) => {
        if (e.key === "Enter") {
            e.preventDefault();
            const userMessage = userInput.value.trim();
            if (userMessage) sendMessage(userMessage);
        }
    });

    optionButtons.forEach(button => {
        button.addEventListener("click", () => {
            const userMessage = button.getAttribute("data-msg");
            sendMessage(userMessage);
        });
    });

    appendMessage("bot", { type: "text", content: "Hello! Welcome to Barbeque Nation. How can I assist you today?" });
});