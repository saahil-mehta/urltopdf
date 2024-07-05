# Webpage PDF Generator

This repository provides a Python script to convert HTML URLs into PDF files. The script is particularly tailored to handle web pages from Google's Cloud Platform (webpage) documentation, ensuring that the content is rendered fully and in English. The PDFs are saved in a structured manner within a specified folder hierarchy.

## Features

- Converts one or multiple HTML URLs to PDFs.
- Generates comprehensible filenames from URLs.
- Ensures the PDF content is in English.
- Saves PDFs to specified subfolders within a `KnowledgeBase` directory.

## Prerequisites

- Python 3.11 or higher
- `pdfkit` library
- `wkhtmltopdf` executable

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/saahil-mehta/urltopdf.git
   cd webpage-knowledge-base-pdf-generator
   ```

2. **Set up the Conda environment:**
   Create and activate a new Conda environment with the required Python version and dependencies.
   ```bash
   conda create --name webpage_pdf_generator python=3.11
   conda activate webpage_pdf_generator
   ```

3. **Install required Python packages:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install `wkhtmltopdf`:**
   - For macOS:
     ```bash
     brew install wkhtmltopdf
     ```
   - For Linux:
     ```bash
     sudo apt-get install wkhtmltopdf
     ```

## Usage

### Function: `save_webpages_as_pdfs`

This function converts one or multiple HTML URLs to PDFs and saves them in a specified subfolder within the `webpage-KnowledgeBase` directory.

#### Parameters:
- `urls` (list or str): A list of HTML URLs or a single URL to be converted to PDFs.
- `destination` (str): The subfolder within `webpage-KnowledgeBase` where PDFs will be saved.

#### Example:
```python
import os
import re
import pdfkit
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

def save_webpages_as_pdfs(urls, destination):
    """
    Convert one or multiple HTML URLs to PDFs and save them with comprehensible filenames.

    Parameters:
    urls (list): A list of HTML URLs to be converted to PDFs.
    destination (str): The subfolder within webpage-KnowledgeBase where PDFs will be saved.

    Returns:
    None
    """
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
        filename = re.sub(r'[^a-zA-Z0-9\-]', '', filename)  # Keep only alphanumeric and hyphen characters
        return filename + '.pdf'
    
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
        query_params['hl'] = 'en'  # Google-specific query parameter for language
        new_query = urlencode(query_params, doseq=True)
        modified_url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, new_query, parsed_url.fragment))
        return modified_url

    output_dir = os.path.join('webpage-KnowledgeBase', destination)
    os.makedirs(output_dir, exist_ok=True)
    
    if isinstance(urls, str):
        urls = [urls]
    
    # PDFKit options to ensure full-page rendering and English language
    options = {
        'no-stop-slow-scripts': '',
        'custom-header': [
            ('Accept-Language', 'en')
        ],
        'enable-local-file-access': ''
    }

    for url in urls:
        try:
            english_url = ensure_english_language(url)
            output_file = os.path.join(output_dir, make_comprehensible_name(english_url))
            pdfkit.from_url(english_url, output_file, options=options)
            print(f"Saved: {output_file}")
        except Exception as e:
            print(f"Error saving {url}: {e}")

# Example usage:
save_webpages_as_pdfs(
    urls=[
        "https://cloud.google.com/bigquery/docs/auditing-policy-tags",
        "https://cloud.google.com/bigquery/docs/column-data-masking-audit-logging",
        "https://cloud.google.com/billing/docs/how-to/export-data-bigquery"
    ],
    destination='bigquery_docs'
)
```

### Running the Script

You can run the script directly from your command line or integrate it into your application as needed.

```bash
python script_name.py
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a pull request

## Acknowledgments

- [pdfkit](https://pypi.org/project/pdfkit/)
- [wkhtmltopdf](https://wkhtmltopdf.org/)

Feel free to create an issue or pull request for any improvements or bug fixes.
