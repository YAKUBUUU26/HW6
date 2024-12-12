const express = require("express");
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

const app = express();
const PORT = 3000;
const USER_FILE = path.join(__dirname, 'users.json');

// Load or initialize user data
let users = {};
if (fs.existsSync(USER_FILE)) {
    users = JSON.parse(fs.readFileSync(USER_FILE, "utf8"));
}

// Save users to the file
const saveUsers = () => {
    fs.writeFileSync(USER_FILE, JSON.stringify(users, null, 4));
};

// Helper function to authenticate users by email and API key
const authenticate = (email, apiKey) => {
    const user = users[email];
    if (!user || user.apiKey !== apiKey) {
        const error = new Error("Unauthorized access");
        error.status = 403;
        throw error;
    }
    return email;
};

// Middleware for error handling
app.use(express.json());
app.use((err, req, res, next) => {
    res.status(err.status || 500).json({ error: err.message });
});

// Add a new user
app.post("/users", (req, res) => {
    const { email, age } = req.body;

    if (!email || !age) {
        return res.status(400).json({ error: "Email and age are required" });
    }
    if (users[email]) {
        return res.status(400).json({ error: "User already exists" });
    }

    // Generate an API key for the user
    const apiKey = crypto.randomBytes(16).toString("hex");

    // Add user to the database
    users[email] = { email, age, apiKey };
    saveUsers();
    res.status(201).json({ message: "User added successfully", apiKey });
});

// Retrieve user profile
app.get("/users/:email", (req, res, next) => {
    try {
        const { email } = req.params;
        const apiKey = req.headers["api-key"];
        authenticate(email, apiKey);
        res.json(users[email]);
    } catch (err) {
        next(err);
    }
});

// Update user profile
app.put("/users/:email", (req, res, next) => {
    try {
        const { email } = req.params;
        const apiKey = req.headers["api-key"];
        authenticate(email, apiKey);

        const { age } = req.body;
        if (!age) {
            return res.status(400).json({ error: "Age is required" });
        }

        // Update user's age
        users[email].age = age;
        saveUsers();
        res.json({ message: "User updated successfully" });
    } catch (err) {
        next(err);
    }
});

// Delete user profile
app.delete("/users/:email", (req, res, next) => {
    try {
        const { email } = req.params;
        const apiKey = req.headers["api-key"];
        authenticate(email, apiKey);

        delete users[email];
        saveUsers();
        res.json({ message: "User deleted successfully" });
    } catch (err) {
        next(err);
    }
});

// Home route
app.get("/", (req, res) => {
    res.send("Welcome to the User API!");
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server is running on http://127.0.0.1:${PORT}`);
});
