document.getElementById("extractText").addEventListener("click", () => {
    document.getElementById("events").innerText = "Generating the Summary!";
    browser.tabs.executeScript({ file: "summary.js" });
});

document.getElementById("clearText").addEventListener("click",()=>{
    browser.tabs.query({ active: true, currentWindow: true })
    .then((tabs) => {
        const currentUrl = tabs[0].url;
        const summary = "Generate New Summary";
        browser.storage.local.set({ [currentUrl]: summary })
        .then(() => console.log("Summary stored for", currentUrl))
        .catch(err => console.error("Storage error:", err));
        document.getElementById("summary").innerText = summary;
        return browser.storage.local.get(currentUrl);
    })
    .catch(error => {
        console.error("Error clearing summary:", error);
    });


});

document.getElementById("ask").addEventListener("click", ()=>{
  if(document.getElementById("question").value!=""){
    document.getElementById("events").innerText = "Asked a QUESTION";
    browser.storage.local.set({"question":document.getElementById("question").value});
    browser.tabs.executeScript({file:"question.js"});
  }
  

});

browser.runtime.onMessage.addListener((message) => {
    if (message.type === "summary") {
        document.getElementById("summary").innerText = message.data;
    }
    if (message.type === "answer") {
        document.getElementById("answer").innerText = message.data;
    }
});


browser.tabs.query({ active: true, currentWindow: true })
  .then((tabs) => {
    const currentUrl = tabs[0].url;
    return browser.storage.local.get(currentUrl);
  })
  .then((result) => {
    const summaryDiv = document.getElementById("summary");
    if (result && result[Object.keys(result)[0]]) {
      summaryDiv.innerText = result[Object.keys(result)[0]];
    } else {
      summaryDiv.innerText = "Generate the Summary first";
    }
  })
  .catch(error => {
    console.error("Error retrieving summary:", error);
  });





browser.tabs.query({ active: true, currentWindow: true })
.then((tabs) => {
  const currentUrl = tabs[0].url+"-ans";
  return browser.storage.local.get(currentUrl);
})
.then((result) => {
  const answerDiv = document.getElementById("answer");
  if (result && result[Object.keys(result)[0]]) {
    answerDiv.innerText = result[Object.keys(result)[0]];
  } else {
    answerDiv.innerText = "Ask the Question first";
  }
})
.catch(error => {
  console.error("Error retrieving summary:", error);
});

