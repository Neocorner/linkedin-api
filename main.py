
from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

app = Flask(__name__)

@app.route('/')
def home():
    return "LinkedIn URL Finder API is running."

@app.route('/get-linkedin-url')
def get_linkedin_url():
    first = request.args.get('first')
    last = request.args.get('last')
    company = request.args.get('company')

    if not first or not last or not company:
        return jsonify({'error': 'Missing parameters'}), 400

    query = f'site:linkedin.com/in "{first} {last}" "{company}"'
    encoded_query = quote(query)
    search_url = f"https://www.google.com/search?q={encoded_query}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    try:
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        for a in soup.find_all('a'):
            href = a.get('href')
            if href and 'linkedin.com/in/' in href:
                # Nettoyage de l'URL
                start = href.find("http")
                end = href.find("&", start)
                linkedin_url = href[start:end] if end != -1 else href[start:]
                return jsonify({'url': linkedin_url})

        return jsonify({'url': 'Aucun résultat'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
