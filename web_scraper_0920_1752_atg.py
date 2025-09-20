# 代码生成时间: 2025-09-20 17:52:34
# web_scraper.py
#
# A simple web scraping tool using Python and the Bottle framework.

import bottle
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Define the base URL for scraping
BASE_URL = 'http://example.com'

# Home route to display a simple form for entering a URL
@bottle.route('/')
def home():
    return bottle.template('form', {'base_url': BASE_URL})

# Route to scrape the content from a given URL
@bottle.route('/scrape', method='POST')
def scrape():
    # Retrieve the URL from the form data
    url = bottle.request.forms.get('url')
    
    # Check if the URL is not empty
    if not url:
        return bottle.template('error', {'error_message': 'Please provide a URL to scrape.'})
        
    try:
        # Make a GET request to the URL
        response = requests.get(url)
        
        # Raise an exception if the request was unsuccessful
        response.raise_for_status()
        
        # Parse the content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract the content from the parsed HTML
        content = soup.get_text()
        
        # Return the scraped content as a JSON response
        return {'status': 'success', 'content': content}
    except requests.exceptions.RequestException as e:
        # Handle any request-related errors
        return bottle.template('error', {'error_message': f'Request failed: {e}'})
    except Exception as e:
        # Handle any other errors
        return bottle.template('error', {'error_message': f'An unexpected error occurred: {e}'})

# Run the Bottle application
if __name__ == '__main__':
    bottle.run(host='localhost', port=8080, debug=True)
