import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from tqdm import tqdm
import logging
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager 

class Crawler:
    def __init__(self, base_url, user_prompt, max_depth=3):
        self.base_url = base_url
        self.user_prompt = user_prompt.lower()  # Convert to lowercase for case-insensitive matching
        self.max_depth = max_depth
        self.visited = set()
        self.to_visit = [(base_url, 0)]
        self.logger = self.setup_logger()
        self.keywords = self.extract_keywords(user_prompt)  # Extract keywords from the user prompt
        self.driver = None  # Selenium WebDriver, initialized only if needed

    def setup_logger(self):
        logger = logging.getLogger(__name__)
        if not logger.hasHandlers():
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger

    def extract_keywords(self, prompt):
        return [word.strip() for word in prompt.split()]

    def initialize_selenium(self):
        if not self.driver:  # Initialize only if not already done
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
            self.logger.info("Selenium WebDriver initialized successfully.")

    def is_valid(self, url):
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)

    def get_links(self, content):
        soup = BeautifulSoup(content, 'html.parser')
        links = set()
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            full_url = urljoin(self.base_url, href)
            if self.is_valid(full_url) and self.same_domain(full_url):
                links.add(full_url)
        return links

    def same_domain(self, url):   
    # filters content based on relevance, 
    # ensuring that the crawler processes only the content that matches the base url.


        base_domain = urlparse(self.base_url).netloc
        target_domain = urlparse(url).netloc
        return base_domain == target_domain

    def is_relevant(self, content):
        content = content.lower()  # Convert to lowercase for case-insensitive matching
        return any(keyword in content for keyword in self.keywords)

    def fetch(self, url):
        try:
            headers = {'User-Agent': 'RufusBot/1.0'}
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            if not response.text.strip():  # Check if the response is empty
                self.logger.info(f"Empty response from {url}. Switching to Selenium.")
                return self.fetch_with_selenium(url)  # Fallback to Selenium

            return response.text
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error occurred while fetching {url} with requests: {e}")
            self.logger.info(f"Attempting to fetch using Selenium due to error.")
            return self.fetch_with_selenium(url)  # Fallback to Selenium on any error

    def fetch_with_selenium(self, url):
        self.initialize_selenium()
        try:
            self.driver.get(url)
            time.sleep(3)  # Wait for the page to load completely
            # Handle infinite scroll if necessary
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            while True:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
            return self.driver.page_source
        except Exception as e:
            self.logger.error(f"Error fetching {url} with Selenium: {e}")
            return None

    def crawl(self):
        with tqdm(total=len(self.to_visit), desc="Crawling URLs", unit="url") as pbar:
            while self.to_visit:
                current_url, depth = self.to_visit.pop(0)
                if current_url in self.visited or depth > self.max_depth:
                    pbar.update(1)  # Update progress bar for skipped URLs
                    continue

                self.logger.info(f"Crawling: {current_url} at depth {depth}")
                content = self.fetch(current_url)

                if content and self.is_relevant(content):  # Check if content is relevant
                    self.visited.add(current_url)
                    links = self.get_links(content)
                    for link in links:
                        if link not in self.visited and self.is_relevant(link):  # Check if the link is relevant
                            self.to_visit.append((link, depth + 1))

                pbar.update(1)  # Update progress bar after processing a URL

        # Close the Selenium driver if used
        if self.driver:
            self.driver.quit()

        return self.visited