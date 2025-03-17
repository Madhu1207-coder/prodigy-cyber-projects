const express = require('express');
const bodyParser = require('body-parser');
const path = require('path');
const rateLimit = require('express-rate-limit');

const app = express();
const port = 3001;

app.use(bodyParser.json());
app.use(express.static('public')); // Serve static files from public directory

let captchaText = '';
let attempts = {}; // Track user attempts

// Rate limiting middleware
const limiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 5, // Limit each IP to 5 requests per windowMs
    message: "Too many requests from this IP, please try again later."
});

// Generate random CAPTCHA
function generateCaptcha() {
    captchaText = '';
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    for (let i = 0; i < 6; i++) {
        captchaText += characters.charAt(Math.floor(Math.random() * characters.length));
    }
    return captchaText;
}

// Endpoint to get CAPTCHA
app.get('/captcha', (req, res) => {
    const captcha = generateCaptcha();
    res.json({ captcha });
});

// Endpoint to validate CAPTCHA
app.post('/validate-captcha', limiter, (req, res) => {
    const { userInput } = req.body;
    const ip = req.ip;

    if (!attempts[ip]) {
        attempts[ip] = 0; // Initialize attempts for this IP
    }

    if (userInput === captchaText) {
        attempts[ip] = 0; // Reset attempts on successful validation
        res.json({ success: true, message: 'CAPTCHA verified successfully' });
    } else {
        attempts[ip] += 1; // Increment attempts on failure
        res.json({ success: false, message: 'CAPTCHA does not match' });
    }

    // Optionally reset CAPTCHA after 3 failed attempts
    if (attempts[ip] >= 3) {
        generateCaptcha();
    }
});

// Serve the frontend (index.html)
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Start server
app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});



