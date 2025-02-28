document.getElementById("extractText").addEventListener("click", () => {
  browser.tabs.executeScript({
      file: "content.js"
  });
});
