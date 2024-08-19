const chatBox = document.getElementById('chat-box');
const userInput = document.getElementById('user-input');

function sendMessage() {
    const message = userInput.value;
    if (message.trim() === '') return;

    addMessageToChatBox(`You: ${message}`);
    userInput.value = '';

    fetchResponse(message);
}

function addMessageToChatBox(message) {
    const messageElement = document.createElement('div');
    messageElement.textContent = message;
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight;
}

async function fetchResponse(message) {
    let response;

    if (message.toLowerCase().includes('hi')) {
        response = { message: "Hi there! I'm here to help you connect with top-rated contractors. How can I assist you today?" };
    } else if (message.toLowerCase().includes('service')) {
        response = await fetch('/service/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ option: message })
        }).then(res => res.json());
    } else if (message.toLowerCase().includes('faq')) {
        response = await fetch(`/faq/?question=${message.split(' ')[1]}`).then(res => res.json());
    } else if (message.toLowerCase().includes('my name is')) {
        let name = message.split(' ').slice(-1)[0];
        let email = prompt("Please provide your email:");
        let phone = prompt("Please provide your phone number:");
        response = await fetch('/user/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, email, phone, service: 'service type' })
        }).then(res => res.json());
    } else {
        response = { message: "Sorry, I didn't understand that." };
    }

    addMessageToChatBox(`Bot: ${response.message || response.answer || response.options}`);
}



