from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

@app.route('/get-linkedin-url')
def get_linkedin_url():
    firstname = request.args.get('first')
    lastname = request.args.get('last')
    company = request.args.get('company')

    if not firstname or not lastname or not company:
        return jsonify({'error': 'Missing parameters'}), 400

    query = f"{firstname} {lastname} {company} site:linkedin.com/in"
    url = f"https://www.google.com/search?q={requests.utils.quote(query)}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')

        for link in soup.find_all('a'):
            href = link.get('href')
            if href and "linkedin.com/in/" in href:
                clean_url = href.split("&")[0].replace("/url?q=", "")
                return jsonify({'url': clean_url})

        return jsonify({'error': 'No LinkedIn profile found'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
