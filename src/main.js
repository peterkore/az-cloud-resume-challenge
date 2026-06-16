const functionApiUrl =
  "https://resume-counter-api.azurewebsites.net/api/GetResumeCounter";

const getVisitorCounter = async () => {
  let countElement = document.getElementById("counter");

  try {
    const response = await fetch(functionApiUrl);

    // Check if the response is successful
    if (response.ok) {
      const data = await response.json();
      countElement.innerText = data.count;
    } else {
      console.error("Failed to fetch visitor counter:", response.statusText);
      countElement.innerText = "Error fetching counter";
    }
  } catch (error) {
    console.error("Error to connect backend", error);
    countElement.innerText = "Error";
  }
};

// Call the function to get the visitor counter when the page loads
document.addEventListener("DOMContentLoaded", (event) => {
  getVisitorCounter();
});
