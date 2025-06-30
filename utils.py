from bs4 import BeautifulSoup
import requests
from urllib.parse import quote

def search_linkedin_profile(first, last, company):
    query = f'site:linkedin.com/in "{first} {last}" "{company}"'
    url = f'https://www.google.com/search?q={quote(query)}'
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    for g in soup.select('.tF2Cxc a'):
        href = g.get('href')
        if 'linkedin.com/in/' in href:
            return href

    return None