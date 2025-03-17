from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import re
import random

app = Flask(__name__)
CORS(app)

# Common weak passwords to avoid
common_passwords = ['123456', 'password', '123456789', 'qwerty', 'abc123']

# Function to assess password strength and additional features
def assess_password_strength(password):
    strength = 'Weak'
    strength_class = 'weak'
    suggestions = []
    entropy_score = 0

    if len(password) >= 8:
        if re.search(r'[A-Z]', password) and re.search(r'[a-z]', password):
            if re.search(r'\d', password):
                if re.search(r'[@$!%*?&#]', password):
                    strength = 'Strong'
                    strength_class = 'strong'
                    entropy_score = 100
                else:
                    strength = 'Moderate'
                    strength_class = 'moderate'
                    entropy_score = 66
            else:
                strength = 'Moderate'
                strength_class = 'moderate'
                entropy_score = 50
        else:
            entropy_score = 33
    else:
        entropy_score = 20
        suggestions.append("Increase password length to at least 8 characters.")

    # Check for common passwords
    if password in common_passwords:
        strength = 'Very Weak'
        strength_class = 'very-weak'
        suggestions.append("Avoid using common passwords.")

    # Check keyboard pattern (simple check for repetitive patterns)
    if re.search(r'^(1234|qwerty|asdf|password)$', password):
        suggestions.append("Avoid using keyboard patterns.")

    return strength, strength_class, entropy_score, suggestions

# Password generator
def generate_password():
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@$!%*?&#"
    return ''.join(random.choice(characters) for i in range(12))

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/check-password', methods=['POST'])
def check_password():
    data = request.json
    password = data.get('password')
    strength, strength_class, entropy, suggestions = assess_password_strength(password)
    return jsonify({
        'strength': strength,
        'strengthClass': strength_class,
        'entropy': entropy,
        'suggestions': suggestions
    })

@app.route('/generate-password', methods=['GET'])
def generate_password_route():
    password = generate_password()
    return jsonify({'password': password})

if __name__ == '__main__':
    app.run(debug=True,use_reloader = False)
