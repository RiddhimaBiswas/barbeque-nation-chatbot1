const chatWindow = document.getElementById('chat-window');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const optionsContainer = document.getElementById('options');

function appendMessage(text, sender = 'bot') {
  const msgDiv = document.createElement('div');
  msgDiv.classList.add('message');
  msgDiv.classList.add(sender === 'bot' ? 'bot-message' : 'user-message');
  msgDiv.textContent = text;
  chatWindow.appendChild(msgDiv);
  chatWindow.scrollTop = chatWindow.scrollHeight;
}

// Predefined city list for simple recognition
const cities = ['delhi', 'bangalore', 'mumbai', 'chennai'];

async function getBotResponse(message) {
  const lower = message.toLowerCase();

  for (const city of cities) {
    if (lower.includes(city)) {
      return `Ah, I see you are asking about Barbeque Nation in ${city.charAt(0).toUpperCase() + city.slice(1)}. How can I assist you with your booking or enquiries there?`;
    }
  }

  if (lower.includes('booking')) {
    return "Sure! Please tell me the city, date, time, and number of guests you'd like to book for.";
  } else if (lower.includes('menu')) {
    return "Here’s our menu highlights: Paneer Tikka, Chicken Seekh Kebab, Barbeque Platter. Would you like to book a table?";
  } else if (lower.includes('timing') || lower.includes('hours')) {
    return "We are open daily from 12 PM to 11 PM.";
  } else if (lower.includes('update')) {
    return "Please provide your booking ID and the details you'd like to update.";
  } else if (lower.includes('cancel')) {
    return "Please share your booking ID to cancel your reservation.";
  } else if (lower.includes('hello') || lower.includes('hi')) {
    return "Hello! Welcome to Barbeque Nation. How may I assist you today?";
  } else {
    return "I'm sorry, I didn't quite catch that. Could you please rephrase or choose one of the options below?";
  }
}

// On clicking any quick option button
optionsContainer.addEventListener('click', async (e) => {
  if (e.target.classList.contains('option-btn')) {
    const text = e.target.getAttribute('data-msg');
    appendMessage(text, 'user');
    const reply = await getBotResponse(text);
    appendMessage(reply, 'bot');
  }
});

// On sending custom typed message
document.getElementById('input-area').addEventListener('submit', async (e) => {
  e.preventDefault();
  const text = userInput.value.trim();
  if (!text) return;

  appendMessage(text, 'user');
  userInput.value = '';
  const reply = await getBotResponse(text);
  appendMessage(reply, 'bot');
});
