const API_URL = "http://localhost:8000";

function showSection(sectionId) {
    // Hide all sections
    document.querySelectorAll('.section').forEach(sec => sec.classList.add('hidden'));
    document.querySelectorAll('.sidebar li').forEach(li => li.classList.remove('active'));

    // Show selected section
    document.getElementById(sectionId).classList.remove('hidden');

    // Highlight sidebar
    const map = {
        'dashboard': 0,
        'email-scan': 1,
        'url-scan': 2,
        'chatbot': 3
    };
    const index = map[sectionId];
    if (index !== undefined) {
        document.querySelectorAll('.sidebar li')[index].classList.add('active');
    }
}

async function scanEmail() {
    const text = document.getElementById('emailInput').value;
    if (!text) return alert("Please enter text to scan.");

    try {
        const response = await fetch(`${API_URL}/predict/text`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: text })
        });

        const data = await response.json();
        const resultDiv = document.getElementById('emailResult');
        resultDiv.classList.remove('hidden');

        document.getElementById('emailPrediction').innerText = data.prediction;
        document.getElementById('emailConfidence').innerText = (data.confidence * 100).toFixed(2);
        document.getElementById('emailExplanation').innerText = data.explanation;

        if (data.prediction === 'Phishing') {
            document.getElementById('emailPrediction').style.color = '#ff7675';
        } else {
            document.getElementById('emailPrediction').style.color = '#55efc4';
        }

    } catch (error) {
        alert("Error connecting to server. Ensure backend is running.");
        console.error(error);
    }
}

async function scanUrl() {
    const url = document.getElementById('urlInput').value;
    if (!url) return alert("Please enter a URL.");

    try {
        const response = await fetch(`${API_URL}/predict/url`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url: url })
        });

        const data = await response.json();
        const resultDiv = document.getElementById('urlResult');
        resultDiv.classList.remove('hidden');

        document.getElementById('urlPrediction').innerText = data.prediction;
        document.getElementById('urlConfidence').innerText = (data.confidence * 100).toFixed(2);

        if (data.prediction === 'Phishing') {
            document.getElementById('urlPrediction').style.color = '#ff7675';
        } else {
            document.getElementById('urlPrediction').style.color = '#55efc4';
        }

    } catch (error) {
        alert("Error connecting to server.");
        console.error(error);
    }
}

async function sendMessage() {
    const input = document.getElementById('chatInput');
    const msg = input.value;
    if (!msg) return;

    // Add user message to history
    const history = document.getElementById('chatHistory');
    history.innerHTML += `<div class="msg user-msg">${msg}</div>`;
    input.value = '';

    // Scroll to bottom
    history.scrollTop = history.scrollHeight;

    try {
        const response = await fetch(`${API_URL}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: msg })
        });

        const data = await response.json();
        history.innerHTML += `<div class="msg bot-msg">${data.response}</div>`;
        history.scrollTop = history.scrollHeight;

    } catch (error) {
        history.innerHTML += `<div class="msg bot-msg">Error: Could not reach chatbot.</div>`;
    }
}
