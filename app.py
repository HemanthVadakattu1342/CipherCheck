from flask import Flask, request, jsonify, render_template
import re

app = Flask(__name__)


def check_password_strength(password):
    score = 0
    feedback = []

    # Rule 1: Minimum length
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Use at least 8 characters")

    # Rule 2: Bonus for longer passwords
    if len(password) >= 12:
        score += 1

    # Rule 3: Has uppercase letters?
    if re.search(r'[A-Z]', password):
        score += 1
    else:
        feedback.append("Add uppercase letters (A-Z)")

    # Rule 4: Has lowercase letters?
    if re.search(r'[a-z]', password):
        score += 1
    else:
        feedback.append("Add lowercase letters (a-z)")

    # Rule 5: Has numbers?
    if re.search(r'[0-9]', password):
        score += 1
    else:
        feedback.append("Add numbers (0-9)")

    # Rule 6: Has special characters?
    if re.search(r'[!@#$%^&*(),.?":{}|<>_\-=+\[\]|;\'",.<>?/`~]', password):
        score += 1
    else:
        feedback.append("Add special characters (!@#$...)")

    # Determine strength label
    if score <= 2:
        label = "Weak"
    elif score <= 3:
        label = "Fair"
    elif score <= 4:
        label = "Good"
    elif score == 5:
        label = "Strong"
    else:
        label = "Very Strong"

    return {
        "score": score,
        "max": 6,
        "label": label,
        "tips": feedback
    }


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/check', methods=['POST'])
def check():
    data = request.get_json()
    password = data.get('password', '')
    result = check_password_strength(password)
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)