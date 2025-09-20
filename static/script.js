document.addEventListener("DOMContentLoaded", () => {
    // Chat elements
    const chatBox = document.getElementById("chat-box");
    const userInput = document.getElementById("user-input");
    const sendBtn = document.getElementById("send-btn");
    
    // Navigation elements
    const navLinks = document.querySelectorAll('.nav-link');
    const views = document.querySelectorAll('.view');

    // --- Core Chat Functionality ---

    /**
     * Creates and adds a message bubble to the chat box.
     * @param {string} text - The message content.
     * @param {string} sender - 'user' or 'ai'.
     */
    function addMessage(text, sender) {
        const messageContainer = document.createElement("div");
        messageContainer.classList.add("message-container");

        if (sender === "user") {
            messageContainer.classList.add("user-message-container");
            messageContainer.innerHTML = `
                <div class="user-message-bubble">
                    <p class="text-sm">${text}</p>
                </div>
            `;
        } else {
            messageContainer.classList.add("ai-message-container");
            messageContainer.innerHTML = `
                <div class="ai-icon">
                    <i class="ph-robot-fill text-gray-300 text-2xl"></i>
                </div>
                <div class="ai-message-bubble">
                    <p class="text-sm">${text}</p>
                </div>
            `;
        }
        
        chatBox.appendChild(messageContainer);
        // Scroll to the bottom to see the latest message
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    /**
     * Sends the user's message to the backend and displays the response.
     */
    async function sendMessage() {
        const userMessage = userInput.value.trim();
        if (!userMessage) return;

        // Display user's message immediately
        addMessage(userMessage, "user");
        userInput.value = ""; // Clear input field

        // Display a loading indicator for the AI response
        const loadingIndicator = document.createElement("div");
        loadingIndicator.classList.add("message-container", "ai-message-container");
        loadingIndicator.id = "loading-indicator";
        loadingIndicator.innerHTML = `
            <div class="ai-icon">
                <i class="ph-robot-fill text-gray-300 text-2xl"></i>
            </div>
            <div class="ai-message-bubble">
                <div class="flex items-center justify-center gap-1 p-2">
                    <div class="w-2 h-2 bg-gray-400 rounded-full animate-pulse" style="animation-delay: 0s;"></div>
                    <div class="w-2 h-2 bg-gray-400 rounded-full animate-pulse" style="animation-delay: 0.2s;"></div>
                    <div class="w-2 h-2 bg-gray-400 rounded-full animate-pulse" style="animation-delay: 0.4s;"></div>
                </div>
            </div>`;
        chatBox.appendChild(loadingIndicator);
        chatBox.scrollTop = chatBox.scrollHeight;

        try {
            // Send message to the Flask backend
            const response = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: userMessage }),
            });

            // Remove the loading indicator
            document.getElementById("loading-indicator")?.remove();

            if (!response.ok) {
                throw new Error(`Network response was not ok: ${response.statusText}`);
            }

            const data = await response.json();
            // Display the actual AI reply
            addMessage(data.reply, "ai");

        } catch (error) {
            console.error("Fetch Error:", error);
            document.getElementById("loading-indicator")?.remove();
            addMessage("Sorry, I'm having trouble connecting. Please check the console and try again.", "ai");
        }
    }

    // --- Event Listeners ---

    sendBtn.addEventListener("click", sendMessage);
    userInput.addEventListener("keypress", (event) => {
        if (event.key === "Enter") {
            sendMessage();
        }
    });

    // --- UI and Navigation Logic ---

    /**
     * Handles clicking on a suggestion chip.
     * @param {string} text - The suggestion text to send.
     */
    window.useSuggestion = (text) => {
        userInput.value = text;
        sendMessage();
    };

    /**
     * Switches between different views (Chat, Dashboard, etc.).
     * @param {string} viewId - The ID of the view to show.
     * @param {HTMLElement} element - The clicked navigation link.
     */
    window.showView = (viewId, element) => {
        // Hide all views
        views.forEach(view => view.classList.add('hidden'));

        // Show the selected view
        const activeView = document.getElementById(viewId);
        if (activeView) {
            activeView.classList.remove('hidden');
        }

        // Update active state in the sidebar
        navLinks.forEach(link => {
            link.classList.remove('bg-gray-700', 'text-white', 'font-semibold');
        });
        if (element) {
            element.classList.add('bg-gray-700', 'text-white', 'font-semibold');
        }
    }

    // --- Initial Message ---
    // Add the initial AI welcome message when the page loads
    addMessage("Hello! I'm Arogya AI. What is your primary health goal today?", "ai");
});

document.addEventListener("DOMContentLoaded", () => {
  const chatBox = document.getElementById("chat-box");
  const userInput = document.getElementById("user-input");
  const sendBtn = document.getElementById("send-btn");
  const navLinks = document.querySelectorAll(".nav-link");
  const views = document.querySelectorAll(".view");

  function addMessage(text, sender) {
    const message = document.createElement("div");
    message.classList.add("mb-4", "flex", sender === "user" ? "justify-end" : "justify-start");

    if (sender === "user") {
      message.innerHTML = `<div class="bg-blue-600 text-white px-4 py-2 rounded-xl max-w-xs">${text}</div>`;
    } else {
      message.innerHTML = `<div class="bg-gray-700 text-gray-100 px-4 py-2 rounded-xl max-w-xs">${text}</div>`;
    }

    chatBox.appendChild(message);
    chatBox.scrollTop = chatBox.scrollHeight;
  }

  async function sendMessage() {
    const text = userInput.value.trim();
    if (!text) return;
    addMessage(text, "user");
    userInput.value = "";

    addMessage("...", "ai"); // temporary loading bubble

    try {
      const res = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text }),
      });
      const data = await res.json();
      chatBox.lastChild.remove();
      addMessage(data.reply, "ai");
    } catch (err) {
      chatBox.lastChild.remove();
      addMessage("⚠️ Error: Could not connect to AI", "ai");
    }
  }

  sendBtn?.addEventListener("click", sendMessage);
  userInput?.addEventListener("keypress", e => { if (e.key === "Enter") sendMessage(); });

  window.showView = (viewId, element) => {
    views.forEach(v => v.classList.add("hidden"));
    document.getElementById(viewId)?.classList.remove("hidden");
    navLinks.forEach(link => link.classList.remove("bg-gray-700", "text-white"));
    element.classList.add("bg-gray-700", "text-white");
  };

  if (chatBox) addMessage("👋 Hi, I’m Arogya AI! What’s your health goal today?", "ai");
});
