// script.js - Connects to Ollama chatbot backend
document.addEventListener('DOMContentLoaded', () => {
  const chatForm = document.getElementById('chat-form');
  const userInput = document.getElementById('user-input');
  const chatWindow = document.getElementById('chat-window');

  const endpoint = 'http://localhost:8000/chat'; // backend endpoint

  // Helper to append a message bubble
  function addMessage(text, role) {
    const msgDiv = document.createElement('div');
    msgDiv.classList.add('message', role);
    msgDiv.textContent = text;
    chatWindow.appendChild(msgDiv);
    chatWindow.scrollTop = chatWindow.scrollHeight;
  }

  chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const message = userInput.value.trim();
    if (!message) return;
    addMessage(message, 'user');
    userInput.value = '';
    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message })
      });
      if (!response.ok) {
        throw new Error(`Server responded ${response.status}`);
      }
      const data = await response.json();
      // Assume response format { reply: '...' }
      const reply = data.reply || data.response || data.answer || '';
      addMessage(reply, 'assistant');
    } catch (err) {
      console.error(err);
      addMessage('Error: could not get response.', 'assistant');
    }
  });
});
