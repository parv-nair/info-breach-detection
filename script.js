let usageCount = localStorage.getItem("usageCount") || 0; // Store usage count locally
document.getElementById("usageCounter").innerText = `Site used: ${usageCount} times`;

async function checkEmail() {
    let email = document.getElementById("email").value;
    let result = document.getElementById("emailResult");

    result.innerHTML = "🔍 Fetching results...";

    let response = await fetch("/check", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email })
    });

    let data = await response.json();
    setTimeout(() => {
        if (data.breaches.length > 0) {
            result.innerHTML = `<strong>⚠️ Email Found in Breaches:</strong><br>${data.breaches.join("<br>")}`;
        } else {
            result.innerHTML = "<strong>✅ This email seems safe.</strong>";
        }

        usageCount++;
        localStorage.setItem("usageCount", usageCount);
        setTimeout(() => {
            window.location.href = "/"; // Return to loading screen
        }, 5000);
    }, 1000);
}

async function checkPassword() {
    let password = document.getElementById("password").value;
    let result = document.getElementById("passwordResult");

    result.innerHTML = "🔍 Fetching results...";

    let response = await fetch("/check", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ password })
    });

    let data = await response.json();
    setTimeout(() => {
        if (data.count > 0) {
            result.innerHTML = `<strong>⚠️ This password has been found ${data.count} times in breaches! Change it!</strong>`;
        } else {
            result.innerHTML = "<strong>✅ This password seems safe.</strong>";
        }

        usageCount++;
        localStorage.setItem("usageCount", usageCount);
        setTimeout(() => {
            window.location.href = "/"; // Return to loading screen
        }, 5000);
    }, 1000);
}
