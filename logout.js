// logout.js

function logout() {
    // Send a POST request to the logout route on the server
    $.ajax({
        url: "http://127.0.0.1:5000/logout",
        method: "POST",
        xhrFields: {
            withCredentials: true  // Ensure cookies are sent with the request
        },
        success: function(response) {
            console.log(response.msg);  // Logout successful message

            // Clear the localStorage (or sessionStorage) that holds the token
            localStorage.removeItem("auth-token");  // Remove JWT token from localStorage

            // Optionally, redirect the user to the login page
            window.location.href = "/login.html";  // Adjust to your login page URL
        },
        error: function(error) {
            console.error("Logout failed", error);
        }
    });
}
