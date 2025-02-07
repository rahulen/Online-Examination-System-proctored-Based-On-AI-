document.getElementById('logoutButton').addEventListener('click', function() {
    // Perform logout logic here, e.g., clearing session storage, redirecting, etc.
    console.log('User logged out');
    
    // Example: Redirect to login page or home page
    window.location.href = '/login.html'; // Change this to the correct path
}); 