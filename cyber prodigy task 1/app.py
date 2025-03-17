from flask import Flask, render_template, request

app = Flask(__name__)

def caesar_cipher(text, shift, action, case_sensitive):
    result = ""
    shift = shift % 26  # Ensure the shift is within 0-25
    for char in text:
        if char.isalpha():
            shift_amount = shift if action == 'encrypt' else -shift
            
            # Handle case sensitivity
            if case_sensitive == 'sensitive':
                new_char = chr((ord(char) - 65 + shift_amount) % 26 + 65) if char.isupper() else chr((ord(char) - 97 + shift_amount) % 26 + 97)
            else:
                new_char = chr((ord(char.lower()) - 97 + shift_amount) % 26 + 97)  # Convert to lowercase for encryption
                new_char = new_char.upper() if char.isupper() else new_char  # Preserve original case

            result += new_char
        else:
            result += char  # Non-alphabetic characters remain unchanged
    return result

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', message="", shift="", result="")

@app.route('/cipher', methods=['POST'])
def cipher():
    message = request.form['message']
    shift = int(request.form['shift'])
    action = request.form['action']
    case_sensitive = request.form['case']
    result = caesar_cipher(message, shift, action, case_sensitive)
    return render_template('index.html', message=message, shift=shift, result=result)

if __name__ == '__main__':
    app.run(debug=True,use_reloader = False)
