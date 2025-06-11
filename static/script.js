document.getElementById('chat-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const input = document.getElementById('user-input');
    const text = input.value.trim();
    if (!text) return;
    addMessage(text, 'user');
    input.value = '';
    fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text })
    })
    .then(res => res.json())
    .then(data => {
        addMessage(data.response, 'bot');
    })
    .catch(() => addMessage('Error contacting bot.', 'bot'));
});

function addMessage(text, sender) {
    const chatbox = document.getElementById('chatbox');
    const msg = document.createElement('div');
    msg.className = 'message ' + sender;
    msg.textContent = text;
    chatbox.appendChild(msg);
    chatbox.scrollTop = chatbox.scrollHeight;
}
