from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/get-linkedin-url')
def get_linkedin_url():
    first = request.args.get('first')
    last = request.args.get('last')
    company = request.args.get('company')

    query = f'site:linkedin.com/in "{first} {last}" "{company}"'
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    google_url = f"https://www.google.com/search?q={requests.utils.quote(query)}"

    response = requests.get(google_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    for link in soup.find_all('a'):
        href = link.get('href')
        if href and 'linkedin.com/in/' in href:
            full_url = href.split("&")[0].replace("/url?q=", "")
            return jsonify({"url": full_url})

    return jsonify({"url": None})

