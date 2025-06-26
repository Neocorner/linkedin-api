
from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/get-linkedin-url')
def get_linkedin_url():
    first = request.args.get('first', '')
    last = request.args.get('last', '')
    company = request.args.get('company', '')

    query = f'site:linkedin.com/in "{first} {last}" "{company}"'
    search_url = f"https://www.google.com/search?q={requests.utils.quote(query)}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    for a in soup.find_all('a'):
        href = a.get('href')
        if href and 'linkedin.com/in' in href:
            url = href.split('&')[0].replace('/url?q=', '')
            return jsonify({"url": url})

    return jsonify({"error": "No LinkedIn URL found"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
