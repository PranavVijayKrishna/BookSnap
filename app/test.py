import requests
import json
import re

# --- CONFIGURATION ---
# Replace 'YOUR_API_KEY' with your key from the Google Cloud Console.
GOOGLE_BOOKS_API_KEY = "AIzaSyAqtEjEVuP6EqFyBoeDO4VAW4Qk1dBzt1Q"

# --- Text Cleaning ---
def clean_text_for_api_query(text):
    """
    Cleans the raw text to make it suitable for an API search query.
    Removes special characters and normalizes whitespace.
    """
    # Remove leading/trailing whitespace
    text = text.strip()
    
    # Remove unwanted punctuation and characters that aren't letters, numbers, or spaces.
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    
    # Normalize whitespace (replace multiple spaces with a single space).
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

# --- API Lookup ---
def get_book_details_by_text(query, api_key):
    """
    Fetches book details from the Google Books API using a general text search.
    """
    # The 'q' parameter in the API search is for a general text query.
    # requests.utils.quote() properly encodes the text for the URL.
    url = f"https://www.googleapis.com/books/v1/volumes?q={requests.utils.quote(query)}&key={api_key}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        data = response.json()
        
        if data.get('totalItems', 0) > 0:
            # Return the details of the first (most relevant) result
            item = data['items'][0]
            volume_info = item.get('volumeInfo', {})
            sale_info = item.get('saleInfo', {})
            
            title = volume_info.get('title')
            authors = volume_info.get('authors', ['N/A'])
            publisher = volume_info.get('publisher')
            
            # New details to extract
            description = volume_info.get('description', 'No description available.')
            ratings_count = volume_info.get('ratingsCount', 'N/A')
            average_rating = volume_info.get('averageRating', 'N/A')
            page_count = volume_info.get('pageCount', 'N/A')
            categories = volume_info.get('categories', ['N/A'])

            buy_link = sale_info.get('buyLink', 'No buying link available.')
            
            return {
                "title": title,
                "authors": ", ".join(authors),
                "publisher": publisher,
                "description": description,
                "ratings_count": ratings_count,
                "average_rating": average_rating,
                "page_count": page_count,
                "categories": ", ".join(categories),
                "buy_link": buy_link
            }
        
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        
    return None

# --- Main Logic ---
if __name__ == "__main__":
    # Your cleaned text is ready to be used.
    extracted_text = "1888. John Edgeland is the heir to an industrial\n\nempire, devastated by the loss of his wife and\n\nunwilling to face his new responsibilities. Fleeing to an\n\nisolated hydropathic hotel in the wilds of Yorkshire, he is\nsubjected to bizarre water treatments and begins to\n\nexperience even stranger events. Who is the mysterious mutilated\ngirl he rescues from a moor fire, and how is she linked\n\nto the sinister, cult-like mill town of Blackmoor?\n\nPolly Hardacre is 2 chambermaid at the hotel, doing her best to keep\nher head down and feed her family. When she is called to take on a\nsecret assignment, to care for a sick guest in a long-abandoned\nroom, she sees a way to lift herself out of drudgery. But, just as she\nbegins to discover herself in her new work, she starts to question if\nshe is a nursemaid or a jailer...\n\nMoorrire Press\n\nwow strangetalesfromtbchills. com\n\nMoortirt\nPRrss\n"

    if GOOGLE_BOOKS_API_KEY == "YOUR_API_KEY":
        print("🛑 Please replace 'YOUR_API_KEY' with your actual API key.")
    else:
        print("--- Raw Extracted Text ---")
        print(extracted_text)
        
        # Clean the text to ensure it's a valid search query.
        cleaned_text = clean_text_for_api_query(extracted_text)
        print("\n--- Cleaned Text Sent to API ---")
        print(cleaned_text)
        
        # Call the function to get book details.
        book_details = get_book_details_by_text(cleaned_text, GOOGLE_BOOKS_API_KEY)
        
        if book_details:
            print("\n--- Book Details from Google Books API ---")
            print(f"\nTitle: {book_details['title']}")
            print(f"\nAuthor(s): {book_details['authors']}")
            print(f"\nPublisher: {book_details['publisher']}")
            print(f"\nDescription: {book_details['description']}")
            print(f"\nAverage Rating: {book_details['average_rating']} ({book_details['ratings_count']} ratings)")
            print(f"\nPage Count: {book_details['page_count']}")
            print(f"\nCategories: {book_details['categories']}")
            print(f"Buy Link: {book_details['buy_link']}")
        else:
            print("❌ Could not find book details using the cleaned text.")