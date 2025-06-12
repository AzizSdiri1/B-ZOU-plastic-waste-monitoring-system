let currentEmail = "";

async function register() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirm-password").value;
    const error = document.getElementById("error");

    try {
        const response = await fetch("/auth/register", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password, confirm_password: confirmPassword })
        });
        const data = await response.json();
        if (response.ok) {
            currentEmail = email;
            document.getElementById("register-form").classList.add("hidden");
            document.getElementById("otp-form").classList.remove("hidden");
            error.textContent = "";
        } else {
            error.textContent = data.detail;
        }
    } catch (err) {
        error.textContent = "An error occurred";
    }
}

async function verifyOTP() {
    const otp = document.getElementById("otp").value;
    const error = document.getElementById("error");

    try {
        const response = await fetch("/auth/verify-register", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email: currentEmail, code: otp })
        });
        const data = await response.json();
        if (response.ok) {
            window.location.href = data.redirect;
        } else {
            error.textContent = data.detail;
        }
    } catch (err) {
        error.textContent = "An error occurred";
    }
}

async function login() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const error = document.getElementById("error");

    try {
        const response = await fetch("/auth/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        });
        const data = await response.json();
        if (response.ok) {
            currentEmail = email;
            document.getElementById("login-form").classList.add("hidden");
            document.getElementById("otp-form").classList.remove("hidden");
            error.textContent = "";
        } else {
            error.textContent = data.detail;
        }
    } catch (err) {
        error.textContent = "An error occurred";
    }
}

async function verifyLoginOTP() {
    const otp = document.getElementById("otp").value;
    const error = document.getElementById("error");

    try {
        const response = await fetch("/auth/verify-login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email: currentEmail, code: otp })
        });
        const data = await response.json();
        if (response.ok) {
            window.location.href = data.redirect;
        } else {
            error.textContent = data.detail;
        }
    } catch (err) {
        error.textContent = "An error occurred";
    }
}

async function resendOTP() {
    const error = document.getElementById("error");

    try {
        const response = await fetch("/auth/resend-otp", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email: currentEmail })
        });
        const data = await response.json();
        if (response.ok) {
            error.textContent = "New OTP sent";
        } else {
            error.textContent = data.detail;
        }
    } catch (err) {
        error.textContent = "An error occurred";
    }
}