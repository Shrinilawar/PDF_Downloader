

import os
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pdf_downloader.log'),
        logging.StreamHandler()
    ]
)

class PDFDownloader:
    def __init__(self, output_folder="downloaded_pdfs"):
        """
        Initialize the PDF downloader with the specified output folder.
        
        Args:
            output_folder (str): Name of the folder where PDFs will be stored
        """
        self.output_folder = output_folder
        self.setup_output_folder()
        self.setup_selenium()
    
    def setup_output_folder(self):
        """Create the output folder if it doesn't exist."""
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
            logging.info(f"Created output folder: {self.output_folder}")
    
    def setup_selenium(self):
        """Configure Selenium WebDriver with Chrome options."""
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Run in headless mode
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_experimental_option(
            'prefs', {
                'download.default_directory': os.path.abspath(self.output_folder),
                'download.prompt_for_download': False,
                'plugins.always_open_pdf_externally': True
            }
        )
        self.driver = webdriver.Chrome(options=chrome_options)
    
    def get_filename_from_url(self, url):
        """
        Extract filename from URL.
        
        Args:
            url (str): URL of the PDF
            
        Returns:
            str: Extracted filename
        """
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        if not filename.endswith('.pdf'):
            filename += '.pdf'
        return filename
    
    def download_with_requests(self, url):
        """
        Download PDF using requests library.
        
        Args:
            url (str): URL of the PDF to download
            
        Returns:
            bool: True if download successful, False otherwise
        """
        try:
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()
            
            # Check if the content is actually a PDF
            if 'application/pdf' not in response.headers.get('content-type', '').lower():
                logging.warning(f"URL {url} does not point to a PDF file")
                return False
            
            filename = self.get_filename_from_url(url)
            filepath = os.path.join(self.output_folder, filename)
            
            # Skip if file already exists
            if os.path.exists(filepath):
                logging.info(f"File already exists: {filename}")
                return True
            
            # Download the file
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            logging.info(f"Successfully downloaded: {filename}")
            return True
            
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to download {url}: {str(e)}")
            return False
    
    def download_with_selenium(self, url):
        """
        Download PDF using Selenium for cases where JavaScript handling is needed.
        
        Args:
            url (str): URL of the PDF to download
            
        Returns:
            bool: True if download successful, False otherwise
        """
        try:
            self.driver.get(url)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Check if PDF is embedded or needs extraction
            pdf_elements = self.driver.find_elements(By.XPATH, "//embed[@type='application/pdf']")
            if pdf_elements:
                pdf_url = pdf_elements[0].get_attribute('src')
                return self.download_with_requests(pdf_url)
            
            return True
            
        except Exception as e:
            logging.error(f"Failed to download {url} with Selenium: {str(e)}")
            return False
    
    def process_url(self, url):
        """
        Process a single URL, attempting different download methods.
        
        Args:
            url (str): URL to process
        """
        url = url.strip()
        if not url:
            return
        
        logging.info(f"Processing URL: {url}")
        
        # Try downloading with requests first
        if self.download_with_requests(url):
            return
        
        # If requests fails, try with Selenium
        logging.info(f"Attempting download with Selenium: {url}")
        self.download_with_selenium(url)
    
    def process_file(self, input_file):
        """
        Process all URLs from the input file.
        
        Args:
            input_file (str): Path to the file containing URLs
        """
        try:
            with open(input_file, 'r') as f:
                urls = f.readlines()
            
            for url in urls:
                self.process_url(url)
                
        except FileNotFoundError:
            logging.error(f"Input file not found: {input_file}")
        except Exception as e:
            logging.error(f"Error processing input file: {str(e)}")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources."""
        if hasattr(self, 'driver'):
            self.driver.quit()

def main():
    """Main entry point of the script."""
    try:
        downloader = PDFDownloader()
        downloader.process_file('links.txt')
        
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main()