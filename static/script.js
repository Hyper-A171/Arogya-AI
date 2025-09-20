document.addEventListener("DOMContentLoaded", () => {
    const chatBox = document.getElementById("chat-box");
    const userInput = document.getElementById("user-input");
    const sendBtn = document.getElementById("send-btn");

    // Function to add a message to the chat display
    function addMessage(text, sender) {
        const messageElement = document.createElement("div");
        messageElement.classList.add("message", `${sender}-message`);
        messageElement.textContent = text;
        chatBox.appendChild(messageElement);
        // Scroll to the latest message
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    // Add the initial AI welcome message
    addMessage("Hello! I'm Arogya AI. What is your primary health goal today?", "ai");

    async function sendMessage() {
        const userMessage = userInput.value.trim();
        if (!userMessage) return;

        addMessage(userMessage, "user");
        userInput.value = "";

        try {
            // Add a loading indicator
            const loadingIndicator = document.createElement("div");
            loadingIndicator.classList.add("message", "ai-message");
            loadingIndicator.textContent = "● ● ●";
            chatBox.appendChild(loadingIndicator);
            chatBox.scrollTop = chatBox.scrollHeight;

            // Send user message to the Flask back-end
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: userMessage }),
            });

            // Remove loading indicator
            chatBox.removeChild(loadingIndicator);

            if (!response.ok) {
                throw new Error("Network response was not ok");
            }

            const data = await response.json();
            addMessage(data.reply, "ai");

        } catch (error) {
            console.error("Fetch Error:", error);
            addMessage("Sorry, I'm having trouble connecting. Please try again.", "ai");
        }
    }

    sendBtn.addEventListener("click", sendMessage);
    userInput.addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
            sendMessage();
        }
    });
});
