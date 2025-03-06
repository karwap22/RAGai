function summarizeText() {
    console.log("Webpage detected — extracting with innerText...");
    
    let extractedText = document.body.innerText;
    let url = window.location.href;
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
        const pageUrl = window.location.href;
        const summary = data.summary;
        browser.storage.local.set({ [pageUrl]: summary })
        .then(() => console.log("Summary stored for", pageUrl))
        .catch(err => console.error("Storage error:", err));

        browser.runtime.sendMessage({ type: "summary", data: data.summary });
    })
    .catch(error => {
        console.error("Error fetching summary:", error);
        browser.runtime.sendMessage({ type: "summary", data: "Error fetching summary: " + error });
    });
}

summarizeText();
