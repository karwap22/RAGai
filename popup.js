document.getElementById("extractText").addEventListener("click", () => {
    browser.tabs.executeScript({ file: "content.js" });
});

browser.runtime.onMessage.addListener((message) => {
    if (message.type === "summary") {
        document.getElementById("summary").innerText = message.data;
    }
});

// browser.storage.local.get("summary").then((result) => {
//     const summaryDiv = document.getElementById("summary");
//     if (result.summary) {
//         summaryDiv.innerText = result.summary;
//     }
// });