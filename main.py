from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/get-linkedin-url')
def get_linkedin_url():
    first = request.args.get('first', '')
    last = request.args.get('last', '')
    company = request.args.get('company', '')

    # Construction de la requête Google avec nom + prénom + entreprise
    query = f'site:linkedin.com/in "{first} {last}" "{company}"'
    google_url = f'https://www.google.com/search?q={requests.utils.quote(query)}'

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        res = requests.get(google_url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')

        link = None
        for a in soup.find_all('a'):
            href = a.get('href')
            if href and 'linkedin.com/in/' in href:
                link = href
                break

        if link:
            # Nettoyage du lien (format Google)
            link = link.split("/url?q=")[-1].split("&")[0]
            return jsonify({'url': link})
        else:
            return jsonify({'url': None})
    except Exception as e:
        return jsonify({'error': str(e)})
