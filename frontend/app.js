document.getElementById("queryForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const youtubeUrl = document.getElementById("youtubeUrl").value.trim();
  const query = document.getElementById("query").value.trim();
  const responseBox = document.getElementById("responseBox");

  if (!youtubeUrl || !query) {
    responseBox.style.display = "block";
    responseBox.style.opacity = 1;
    responseBox.value = "⚠️ Please fill in both Link and Query fields.";
    // responseBox.style.height = "auto";
    // responseBox.style.height = responseBox.scrollHeight + "px";
    return;
  }

  responseBox.style.display = "block";
  responseBox.style.opacity = 1;
  responseBox.value = "Loading... ⏳";
  // responseBox.style.height = "auto";
  // responseBox.style.height = responseBox.scrollHeight + "px";

  try {
    const response = await fetch("/query", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ youtube_url: youtubeUrl, query: query }),
    });

    const data = await response.json();

    if (response.ok) {
      responseBox.value = data.result;
    } else {
      responseBox.value = `❌ Error: ${data.detail}`;
    }

    // responseBox.style.height = "auto";
    // responseBox.style.height = responseBox.scrollHeight + "px";
  } catch (error) {
    responseBox.value = `❌ Unexpected error: ${error.message}`;
    // responseBox.style.height = "auto";
    // responseBox.style.height = responseBox.scrollHeight + "px";
  }
});

document.getElementById("resetBtn").addEventListener("click", () => {
  document.getElementById("youtubeUrl").value = "";
  document.getElementById("query").value = "";

  const responseBox = document.getElementById("responseBox");
  responseBox.style.opacity = 0;
  setTimeout(() => {
    responseBox.style.display = "none";
    responseBox.value = "";
    // responseBox.style.height = "auto";
  }, 300);
});
