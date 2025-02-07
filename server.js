const express = require("express");
const session = require("express-session");

const app = express();

// Setup session middleware
app.use(
  session({
    secret: "your-secret-key",
    resave: false,
    saveUninitialized: true,
    cookie: { secure: false }, // Set to true if using HTTPS
  })
);

// Logout route
app.get("/logout", (req, res) => {
  // Destroy the session
  req.session.destroy((err) => {
    if (err) {
      return res.status(500).send("Error logging out");
    }
    // Redirect to login page
    res.redirect("/login.html");
  });
});

// Start the server
app.listen(3000, () => {
  console.log("Server is running on port 3000");
});
