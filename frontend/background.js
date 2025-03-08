// let isSidebarOpen = false;

// browser.browserAction.onClicked.addListener(() => {
//     if (isSidebarOpen) {
//         browser.sidebarAction.setPanel({ panel: "" });
//         isSidebarOpen = false;
//     } else {
//         browser.sidebarAction.setPanel({ panel: "frontend/sidebar.html" });
//         isSidebarOpen = true;
//     }
// });

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
