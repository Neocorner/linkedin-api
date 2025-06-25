from flask import Flask, request, jsonify
import urllib.parse
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "API LinkedIn Search est en ligne 🚀"

@app.route('/get-linkedin-url')
def get_linkedin_url():
    first = request.args.get('first')
    last = request.args.get('last')
    company = request.args.get('company')

    # Construit la requête Google avec nom + prénom + entreprise
    query = f'site:linkedin.com/in "{first} {last}" "{company}"'
    google_search_url = "/search?q=" + urllib.parse.quote(query)

    return jsonify({"url": google_search_url})

if __name__ == '__main__':
    # 🔧 Corrigé pour Render : écoute sur le bon port
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
