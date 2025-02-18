from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv('API_KEY')
CX = os.getenv('CX')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def retrieve():
    # Get the search type (internship, job, or course) from the form
    search_type = request.form['search_type']  # Assuming form field is named 'search_type'
    topic = request.form['topic']  # The user input for the specific topic

    url = f"https://www.google.com/search?q={topic}+{search_type}"
    
    query = f"{topic} {search_type}"
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={API_KEY}&cx={CX}"    
    response = requests.get(url)
    # print(response)
    data = response.json()
    # print(data)
    links = [item['link'] for item in data.get('items', [])[:5]]  # Extract top 5 links
    # print(links)
    return render_template('results.html', links=links, search_type=search_type)

if __name__ == '__main__':
    app.run(debug=True)