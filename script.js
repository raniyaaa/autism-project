const API_BASE_URL = "http://127.0.0.1:5000";

// Upload PDF to backend
function uploadPDF() {
    let fileInput = document.getElementById("pdfUpload");
    let uploadStatus = document.getElementById("uploadStatus");

    if (fileInput.files.length === 0) {
        alert("Please select a PDF file.");
        return;
    }

    let formData = new FormData();
    formData.append("pdfs", fileInput.files[0]);

    fetch(`${API_BASE_URL}/upload`, {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        uploadStatus.innerText = data.message || "Upload successful!";
    })
    .catch(error => {
        console.error("Error uploading PDF:", error);
        uploadStatus.innerText = "Failed to upload PDF.";
    });
}

// Send user message and get AI response
function sendMessage() {
    let userInput = document.getElementById("userInput");
    let chatBox = document.getElementById("chatBox");

    let userMessage = userInput.value.trim();
    if (!userMessage) return;

    // Display user message
    let userMsgDiv = document.createElement("div");
    userMsgDiv.className = "message user";
    userMsgDiv.innerText = userMessage;
    chatBox.appendChild(userMsgDiv);

    // Clear input field
    userInput.value = "";

    // Send request to Flask backend
    fetch(`${API_BASE_URL}/query`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: userMessage })
    })
    .then(response => response.json())
    .then(data => {
        let botMsgDiv = document.createElement("div");
        botMsgDiv.className = "message bot";
        botMsgDiv.innerText = data.response || "Error getting response.";
        chatBox.appendChild(botMsgDiv);

        // Scroll to latest message
        chatBox.scrollTop = chatBox.scrollHeight;
    })
    .catch(error => {
        console.error("Error getting AI response:", error);
    });
}
