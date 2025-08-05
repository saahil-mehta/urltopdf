import os
import re
import pdfkit
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

def make_comprehensible_name(url):
    """
    Generate a comprehensible filename from a URL.
    
    Parameters:
    url (str): The URL to be converted to a filename.
    
    Returns:
    str: A comprehensible filename.
    """
    parsed_url = urlparse(url)
    filename = parsed_url.path.strip('/').replace('/', '-')
    filename = re.sub(r'[^a-zA-Z0-9\-]', '', filename)
    return filename + '.pdf'

def check_url_response_time(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.elapsed.total_seconds()
    except Exception as e:
        print(f"Error accessing {url}: {e}")
        return None

def save_google_docs_as_pdfs(urls, destination):
    """
    Convert Google Docs URLs to PDFs and save them with comprehensible filenames.

    Parameters:
    urls (list): A list of Google Docs URLs to be converted to PDFs.
    destination (str): The subfolder within GCP-KnowledgeBase where PDFs will be saved.

    Returns:
    None
    """
    def ensure_english_language(url):
        """
        Modify the URL to include a language parameter to force English.

        Parameters:
        url (str): The URL to be modified.

        Returns:
        str: The modified URL with the language parameter set to English.
        """
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        query_params['hl'] = 'en'
        new_query = urlencode(query_params, doseq=True)
        modified_url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, new_query, parsed_url.fragment))
        return modified_url

    output_dir = os.path.join('GCP-KnowledgeBase', destination)
    os.makedirs(output_dir, exist_ok=True)
    
    if isinstance(urls, str):
        urls = [urls]

    options = {
        'no-stop-slow-scripts': '',
        'enable-local-file-access': '',
        'load-error-handling': 'ignore',
        'javascript-delay': 1000,  # Adjust this delay as necessary
        'disable-javascript': '',  # Disable JavaScript if not needed
        'quiet': ''  # Suppress messages
    }

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(process_url, ensure_english_language(url), output_dir, options): url for url in urls}
        for future in as_completed(futures):
            url = futures[future]
            try:
                future.result()
            except Exception as e:
                print(f"Error processing {url}: {e}")

def save_other_webpages_as_pdfs(urls, destination):
    """
    Convert other webpages URLs to PDFs and save them with comprehensible filenames.

    Parameters:
    urls (list): A list of webpage URLs to be converted to PDFs.
    destination (str): The subfolder within KnowledgeBase where PDFs will be saved.

    Returns:
    None
    """
    output_dir = os.path.join('KnowledgeBase', destination)
    os.makedirs(output_dir, exist_ok=True)
    
    if isinstance(urls, str):
        urls = [urls]

    options = {
        'no-stop-slow-scripts': '',
        'enable-local-file-access': '',
        'load-error-handling': 'ignore',
        'javascript-delay': 1000,  # Adjust this delay as necessary
        'disable-javascript': '',  # Disable JavaScript if not needed
        'quiet': ''  # Suppress messages
    }

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(process_url, url, output_dir, options): url for url in urls}
        for future in as_completed(futures):
            url = futures[future]
            try:
                future.result()
            except Exception as e:
                print(f"Error processing {url}: {e}")

def process_url(url, output_dir, options):
    print(f"Processing {url}")
    response_time = check_url_response_time(url)
    if response_time is not None:
        print(f"Response time for {url}: {response_time} seconds")
    try:
        output_file = os.path.join(output_dir, make_comprehensible_name(url))
        pdfkit.from_url(url, output_file, options=options)
        print(f"Saved: {output_file}")
    except Exception as e:
        print(f"Error saving {url}: {e}")
