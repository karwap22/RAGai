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
            .then(response => response.json())
            .then(data => {
                console.log("Answer of the question:", data.answer);
                const pageUrl = window.location.href + "-ans";
                const answer = data.answer;
                browser.storage.local.set({ [pageUrl]: answer })
                .then(() => console.log("Answer stored for", pageUrl))
                .catch(err => console.error("Storage error:", err));
            
                browser.runtime.sendMessage({ type: "answer", data: data.answer });
            })
            .catch(error => {
                console.error("Error fetching summary:", error);
                browser.runtime.sendMessage({ type: "answer", data: "Error fetching summary: " + error });
            });
        }
    });
    
    
}


questionAns();
