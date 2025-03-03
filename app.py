from flask import Flask, render_template, request, jsonify
import hashlib
import requests
import os

app = Flask(__name__)

# Use your API Key (Ensure to set this securely in production)
HIBP_API_KEY = "0ca81d0083msh34fcaca754f714cp12ddcejsnac5f263e9e0e"

def check_password(password):
    """
    Check if a password has been exposed in data breaches using k-anonymity
    Returns the number of times the password was found in breaches.
    """
    sha1_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix = sha1_password[:5]
    suffix = sha1_password[5:]
    
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    response = requests.get(url)
    
    if response.status_code != 200:
        return None
        
    hashes = (line.split(':') for line in response.text.splitlines())
    count = next((int(count) for hash_suffix, count in hashes 
                 if hash_suffix == suffix), 0)
    
    return count

def check_email(email):
    """
    Check if an email has appeared in any known data breaches using HaveIBeenPwned API.
    """
    url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
    headers = {
        'hibp-api-key': HIBP_API_KEY,
        'user-agent': 'Flask App Security Checker'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 404:
        return "This email seems safe!"
    elif response.status_code == 200:
        return "Uh Oh! Your email has been compromised."
    else:
        return "An error occurred. Please try again later."

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check():
    data = request.get_json()
    
    if 'email' in data:
        email_result = check_email(data['email'])
        return jsonify({'type': 'email', 'result': email_result})
    
    elif 'password' in data:
        password_count = check_password(data['password'])
        if password_count:
            return jsonify({'type': 'password', 'result': f"This password has been found {password_count} times in breaches!"})
        else:
            return jsonify({'type': 'password', 'result': "This password is safe and has not been found in breaches!"})
    
    return jsonify({'error': 'Invalid request'}), 400

if __name__ == '__main__':
    app.run(debug=True)
