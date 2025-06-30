from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/get-linkedin-url')
def get_linkedin_url():
    first = request.args.get('first')
    last = request.args.get('last')
    company = request.args.get('company')

    if not all([first, last, company]):
        return jsonify({'error': 'Missing parameters'}), 400

    query = f"{first} {last} {company} site:linkedin.com/in"
    url = f"https://www.google.com/search?q={requests.utils.quote(query)}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    try:
        res = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(res.text, "html.parser")
        for link in soup.find_all("a"):
            href = link.get("href")
            if href and "linkedin.com/in/" in href:
                clean_url = href.split("&")[0].replace("/url?q=", "")
                return jsonify({'url': clean_url})
        return jsonify({'error': 'No LinkedIn profile found'})
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

@app.route('/')
def home():
    return "LinkedIn URL API is running."