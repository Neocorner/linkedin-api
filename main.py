
from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "LinkedIn URL Finder with SerpAPI is running."

@app.route('/get-linkedin-url')
def get_linkedin_url():
    first = request.args.get('first')
    last = request.args.get('last')
    company = request.args.get('company')

    if not first or not last or not company:
        return jsonify({'error': 'Missing parameters'}), 400

    query = f'site:linkedin.com/in "{first} {last}" "{company}"'
    api_key = os.getenv('SERPAPI_KEY')

    if not api_key:
        return jsonify({'error': 'Missing SERPAPI_KEY in environment'}), 500

    params = {
        'q': query,
        'api_key': api_key,
        'engine': 'google',
        'num': 1
    }

    try:
        res = requests.get('https://serpapi.com/search', params=params)
        data = res.json()

        if 'organic_results' in data and len(data['organic_results']) > 0:
            link = data['organic_results'][0].get('link', '')
            if 'linkedin.com/in/' in link:
                return jsonify({'url': link})

        return jsonify({'url': 'Aucun résultat'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
