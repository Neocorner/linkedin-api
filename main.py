from flask import Flask, request, jsonify
import urllib.parse
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/")
def index():
    return "API LinkedIn fonctionne sur Render !"

@app.route("/get-linkedin-url", methods=["GET"])
def get_linkedin_url():
    first = request.args.get("first", "")
    last = request.args.get("last", "")
    company = request.args.get("company", "")

    if not first or not last or not company:
        return jsonify({"url": ""})

    query = f'site:linkedin.com/in "{first} {last}" "{company}"'
    search_url = "https://www.google.com/search?q=" + urllib.parse.quote_plus(query)
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(search_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and "linkedin.com/in" in href:
                linkedin_url = href.split("&")[0].replace("/url?q=", "")
                return jsonify({"url": linkedin_url})
    except Exception as e:
        return jsonify({"error": str(e)})

    return jsonify({"url": ""})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)