from flask import Flask, request, jsonify
from utils import search_linkedin_profile

app = Flask(__name__)

@app.route('/get-linkedin-url')
def get_linkedin_url():
    first = request.args.get('first')
    last = request.args.get('last')
    company = request.args.get('company')

    if not all([first, last, company]):
        return jsonify({'error': 'Missing parameters'}), 400

    url = search_linkedin_profile(first, last, company)

    if url:
        return jsonify({'url': url})
    else:
        return jsonify({'error': 'No LinkedIn profile found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)