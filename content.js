function getAllText() {
    console.log("Webpage detected — extracting with innerText...");
    summarizeText(document.body.innerText);
}

function summarizeText(extractedText) {
    fetch("http://localhost:5000/summarize", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ text: extractedText })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Summary from Ollama:", data.summary);
        // browser.storage.local.set({"summary": data.summary });
        browser.runtime.sendMessage({ type: "summary", data: data.summary });
    })
    .catch(error => {
        console.error("Error fetching summary:", error);
        browser.runtime.sendMessage({ type: "summary", data: "Error fetching summary: " + error });
    });
}

getAllText();
