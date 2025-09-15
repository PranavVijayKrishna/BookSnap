from dotenv import load_dotenv
import requests
import json
import re
import os

def clean_raw_string(raw_text):

    text = raw_text.strip()

    cleaned_text = re.sub(r'[^a-zA-Z0-9\s]', '', text)

    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()

    return cleaned_text


def get_book_info(query):

    load_dotenv()

    api_key = os.getenv("GOOGLE_BOOKS_API_KEY")

    if not api_key:
        return "API key not found. Please set the 'API_KEY' environment variable."

    url = f"https://www.googleapis.com/books/v1/volumes?q={requests.utils.quote(query)}&key={api_key}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data.get('totalItems', 0) > 0:
            item = data['items'][0]

            # info
            volume_info = item.get('volumeInfo', {})
            sale_info = item.get('saleInfo', {})

            title = volume_info.get('title')
            authors = volume_info.get('authors', ['N/A'])
            publisher = volume_info.get('publisher')
            buy_link = sale_info.get('buyLink', 'No buying link available.')

            description = volume_info.get('description', 'No description available.')
            ratings_count = volume_info.get('ratingsCount', 'N/A')
            avg_rating = volume_info.get('averageRating', 'N/A')
            page_count = volume_info.get('pageCount', 'N/A')
            categories = volume_info.get('categories', ['N/A'])


            return {
                "title": title,
                "authors": ", ".join(authors),
                "publisher": publisher,
                "buy_link": buy_link,
                "description": description,
                "ratings_count": ratings_count,
                "average_rating": avg_rating,
                "page_count": page_count,
                "categories": ", ".join(categories)
            }

        else:
            return "No book information found for the given query."
        

    except requests.exceptions.RequestException as e:
        return (f"API request failed: {str(e)}")