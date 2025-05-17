import re

def clean_text_response(text):
    """Clean up text response by removing markdown formatting"""
    text = re.sub(r'[\*_]{1,2}([^*_]+)[\*_]{1,2}', r'\1', text)
    return text.strip()
