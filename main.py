from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/get-linkedin-url', methods=['GET'])
def get_linkedin_url():
    first = request.args.get('first')
    last = request.args.get('last')
    company = request.args.get('company')

    if not first or not last or not company:
        return jsonify({'error': 'Missing parameters'}), 400

    # Construire la requête Google
    query = f'site:linkedin.com/in "{first} {last}" "{company}"'
    search_url = f"https://www.google.com/search?q={requests.utils.quote(query)}"

    # Faire la requête à Google
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(search_url, headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')

    # Chercher le premier lien LinkedIn dans les résultats
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and "linkedin.com/in/" in href:
            # Nettoyer l'URL
            clean_url = href.split('&')[0].replace('/url?q=', '')
            return jsonify({"url": clean_url})

    return jsonify({"url": None})  # Aucun résultat trouvé
