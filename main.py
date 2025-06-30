from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import urllib.parse

app = Flask(__name__)

@app.route('/get-linkedin-url', methods=['GET'])
def get_linkedin_url():
    first = request.args.get('first')
    last = request.args.get('last')
    company = request.args.get('company')

    if not first or not last or not company:
        return jsonify({'error': 'Missing parameters'}), 400

    query = f"{first} {last} {company} LinkedIn"
    url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    for link in soup.find_all('a'):
        href = link.get('href')
        if href and "linkedin.com/in/" in href:
            clean_url = href.split("&")[0].replace("/url?q=", "")
            return jsonify({'url': clean_url})

    return jsonify({'error': 'No LinkedIn profile found'})