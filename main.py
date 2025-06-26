
from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import urllib.parse

app = Flask(__name__)

@app.route('/get-linkedin-url')
def get_linkedin_url():
    first = request.args.get('first', '')
    last = request.args.get('last', '')
    company = request.args.get('company', '')

    query = f'site:linkedin.com/in/ "{first} {last}" "{company}"'
    query_encoded = urllib.parse.quote_plus(query)
    url = f"https://www.google.com/search?q={query_encoded}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    for link in soup.find_all('a'):
        href = link.get('href')
        if href and '/url?q=https://www.linkedin.com/in/' in href:
            real_url = href.split('/url?q=')[1].split('&')[0]
            return jsonify({'url': real_url})

    return jsonify({'error': 'No LinkedIn profile found'})
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
