from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/get-linkedin-url', methods=['GET'])
def get_linkedin_url():
    first = request.args.get('first', '')
    last = request.args.get('last', '')
    company = request.args.get('company', '')

    query = f'site:linkedin.com/in "{first} {last}" "{company}"'
    url = f"https://www.google.com/search?q={requests.utils.quote(query)}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    for link in soup.find_all('a'):
        href = link.get('href', '')
        if "linkedin.com/in" in href:
            linkedin_url = href.split("&")[0].replace("/url?q=", "")
            return jsonify({"url": linkedin_url})

    return jsonify({"url": None})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
