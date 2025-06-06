document.addEventListener("DOMContentLoaded", function () {
    const registerForm = document.getElementById("registerForm");

    registerForm.addEventListener("submit", function (event) {
        event.preventDefault(); // Prevent normal form submission

        const email = document.getElementById("email").value.trim();
        const username = document.getElementById("username").value.trim();
        const password = document.getElementById("password").value;
        const confirmPassword = document.getElementById("confirm_password").value;

        // Client-side validation
        if (!validateEmail(email)) {
            alert("Please enter a valid email address.");
            return;
        }
        if (username.length < 3) {
            alert("Username must be at least 3 characters long.");
            return;
        }
        if (password.length < 6) {
            alert("Password must be at least 6 characters long.");
            return;
        }
        if (password !== confirmPassword) {
            alert("Passwords do not match.");
            return;
        }

        // Prepare form data for sending
        const formData = new FormData();
        formData.append("email", email);
        formData.append("username", username);
        formData.append("password", password);
        formData.append("confirm_password", confirmPassword);

        fetch(registerForm.action, {
            method: registerForm.method, // typically "POST"
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest' // optional, can help server identify AJAX requests
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error("Network response was not ok: " + response.status);
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                alert(data.message || "Registration successful!");
                window.location.href = data.redirect_url || "/login"; // Redirect to login page
            } else {
                alert("Registration failed: " + (data.message || "Unknown error"));
            }
        })
        .catch(error => {
            console.error("Fetch error:", error);
            alert("There was a problem submitting the form. Please try again.");
        });
    });
});

function validateEmail(email) {
    const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return emailPattern.test(email);
}
