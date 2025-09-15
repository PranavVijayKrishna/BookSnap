import requests
import json
import re

def clean_raw_string(raw_text):

    text = raw_text.strip()

    cleaned_text = re.sub(r'[^a-zA-Z0-9\s]', '', text)

    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()

    return cleaned_text




