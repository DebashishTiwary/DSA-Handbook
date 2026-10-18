const express = require('express');
const { OAuth2Client } = require('google-auth-library');
const cors = require('cors');

const app = express();
app.use(express.json());
app.use(cors()); // Allows your frontend to talk to this backend

// TODO: Replace with your actual Google Client ID from Google Cloud Console
const CLIENT_ID = '600778720893-aka0nllru69u6s525ue0ijpqkuf5h14m.apps.googleusercontent.com';
const client = new OAuth2Client(CLIENT_ID);

// API endpoint that your frontend login page will call
app.post('/api/google-login', async (req, res) => {
    const { token } = req.body;

    try {
        // Verify the token securely with Google's servers
        const ticket = await client.verifyIdToken({
            idToken: token,
            audience: CLIENT_ID,
        });
        
        const payload = ticket.getPayload();
        
        console.log(`Successfully verified user: ${payload.name} (${payload.email})`);

        // Send safe user info back to the frontend
        res.status(200).json({
            success: true,
            name: payload.name,
            email: payload.email,
            picture: payload.picture
        });

    } catch (error) {
        console.error("Authentication failed:", error);
        res.status(401).json({ success: false, message: 'Invalid Google token' });
    }
});

// Start the backend server on port 3000
app.listen(3000, () => {
    console.log('Backend server running on http://localhost:3000');
});