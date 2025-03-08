function questionAns() {
let extractedText = document.body.innerText;
browser.storage.local.get("question").then((result) => {
    const questionExtracted = result.question;
    console.log("Question Asked here -", questionExtracted);
    
    if (questionExtracted !== "") {
    fetch("http://localhost:5000/question", {
        method: "POST",
        headers: {
        "Content-Type": "application/json"
        },
        body: JSON.stringify({ text: extractedText, question: questionExtracted })
    })
    .then(response => {
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let answerText = "";
        let buffer = "";

        // Process buffered text for complete SSE events.
        function processBuffer() {
        const parts = buffer.split("\n\n");
        buffer = parts.pop(); // Keep any incomplete chunk
        
        for (let part of parts) {
            // Each SSE event may include multiple "data:" lines
            const lines = part.split("\n");
            let eventData = lines
            .filter(line => line.startsWith("data:"))
            .map(line => line.replace(/^data:\s*/, '').trim())
            .join(" ");
            eventData = eventData.trim();
            
            // If the event signals the end, finalize the answer.
            if (eventData === "[DONE]") {
            console.log("Streaming complete. Final answer:", answerText);
            const pageUrl = window.location.href + "-ans";
            browser.storage.local.set({ [pageUrl]: answerText })
                .then(() => console.log("Answer stored for", pageUrl))
                .catch(err => console.error("Storage error:", err));
            return true; // Signal that we're done.
            } else {
            answerText += eventData + " ";
            // console.log("Streaming update answer:", answerText);
            browser.runtime.sendMessage({ type: "answer", data: answerText });
            }
        }
        return false;
        }

        // Read the stream recursively.
        function read() {
        return reader.read().then(({ done, value }) => {
            if (done) {
            console.log("Stream reading completed.");
            return;
            }
            buffer += decoder.decode(value, { stream: true });
            if (!processBuffer()) {
            return read();
            }
        });
        }
        return read();
    })
    .catch(error => {
        console.error("Error fetching answer:", error);
        browser.runtime.sendMessage({ type: "answer", data: "Error fetching answer: " + error });
    });
    }
});
}

questionAns();
