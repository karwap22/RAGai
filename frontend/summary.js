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
    .then(response => {
      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let summaryText = "";
      let buffer = "";
  
      // Process buffered text for complete SSE events.
      function processBuffer() {
        // SSE events are separated by two newlines.
        const parts = buffer.split("\n\n");
        // Save the last, possibly incomplete, part in the buffer.
        buffer = parts.pop();
        
        for (let part of parts) {
          // For events with multiple "data:" lines, split them and combine.
          const lines = part.split("\n");
          let eventData = lines
            .filter(line => line.startsWith("data:"))
            .map(line => line.replace(/^data:\s*/, '').trim())
            .join(" ");
          eventData = eventData.trim();
          
          // If the event signals the end, stop processing.
          if (eventData === "[DONE]") {
            console.log("Streaming complete. Final summary:", summaryText);
            browser.storage.local.set({ [url]: summaryText })
              .then(() => console.log("Summary stored for", url))
              .catch(err => console.error("Storage error:", err));
            return true; // Signal that we're done.
          } else {
            summaryText += eventData + " ";
            console.log("Streaming update:", summaryText);
            browser.runtime.sendMessage({ type: "summary", data: summaryText });
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
          // Append the decoded chunk to our buffer.
          buffer += decoder.decode(value, { stream: true });
          // Process complete events from the buffer.
          if (!processBuffer()) {
            return read();
          }
        });
      }
      return read();
    })
    .catch(error => {
      console.error("Error fetching summary:", error);
      browser.runtime.sendMessage({ type: "summary", data: "Error fetching summary: " + error });
    });
  }
  
  summarizeText();
  