document.getElementById("extractText").addEventListener("click", () => {
  browser.tabs.executeScript({
      file: "summary.js"
  });
});


document.getElementById("ask").addEventListener("click", () => {
  browser.tabs.executeScript({
      file: "question.js"
  });
});
