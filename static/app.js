const form = document.querySelector("#form");
form.addEventListener("submit", function(e){
    e.preventDefault();
    getColors();
});

function getColors() {
    const query = form.elements.query.value;
    fetch("/palette", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: new URLSearchParams({
            query: query
        })
    })
    .then((response) => response.json())
    .then(data => {
        const colors = data.colors;
        const container = document.querySelector(".container");
        createColorBoxes(colors, container);
    })
}

const chatContainer = document.getElementById('chat-container');
const userInputForm = document.getElementById('user-input');
const userMessageInput = document.getElementById('userMessage');

userInputForm.onsubmit = function(event) {
    event.preventDefault();

    const userMessage = userMessageInput.value;
    appendMessage('User', userMessage);

    fetch('/chat', {
        method: 'POST',
        body: new URLSearchParams({
            'userMessage': userMessage
        })
    })
    .then(response => response.text())
    .then(response => {
        appendMessage('Chatbot', response);
        userMessageInput.value = '';
    });
}

//------------------------------------
function createColorBoxes(colors, parent) {
    parent.innerHTML = "";
    for(const color of colors) {
        const div = document.createElement("div");
        div.classList.add("color");
        div.style.backgroundColor = color;

        div.addEventListener("click", function() {
            navigator.clipboard.writeText(color);
        })

        const span = document.createElement("span");
        //span.innerText = "HELLO!"
        span.innerText = color;
        div.appendChild(span);
        parent.appendChild(div);
    }
}

function appendMessage(author, message) {
    const messageElement = document.createElement('p');
    messageElement.innerHTML = `<strong>${author}:</strong> ${message}`;
    chatContainer.appendChild(messageElement);
}
