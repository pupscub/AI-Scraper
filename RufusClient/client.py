import os
import json
from .crawler import Crawler
from .parser import Parser
from .synthesizer import Synthesizer
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed

# Load environment variables from .env file
load_dotenv()

class RufusClient:
    """
    A comprehensive web data extraction and synthesis client that orchestrates 
    web crawling, content parsing, and information synthesis.

    The RufusClient provides a high-level interface for extracting and 
    synthesizing web content based on user-defined prompts and search parameters.

    Attributes:
        user_prompt (str): The search query or topic of interest
        max_depth (int): Maximum crawling depth for web exploration
        openai_api_key (str): Authentication key for OpenAI services

    Key Components:
        - Web Crawling (Crawler)
        - Content Parsing (Parser)
        - Information Synthesis (Synthesizer)
    """
    
    def __init__(self, user_prompt, max_depth=2):
        """
        Initialize the RufusClient with user specifications.

        Args:
            user_prompt (str): Specific search query or topic to explore
            max_depth (int, optional): Maximum website crawling depth. Defaults to 2.

        Raises:
            ValueError: If OpenAI API key is not found in environment variables
        
        Environment Setup:
            - Loads API key from .env file
            - Validates API key presence
        """
        self.user_prompt = user_prompt
        self.max_depth = max_depth
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        if not self.openai_api_key:
            raise ValueError("OpenAI API key not found. Please set it in the .env file.")


    def scrape(self, url):
        """
        Comprehensive web scraping method that performs:
        1. Web Crawling
        2. Concurrent Content Extraction
        3. Parsing
        4. Information Synthesis

        Args:
            url (str): Base URL to start web crawling

        Returns:
            dict: Structured and synthesized documents extracted from web content

        Workflow:
        - Initializes Crawler with base URL and user prompt
        - Performs concurrent web content retrieval
        - Parses retrieved content using Parser
        - Synthesizes parsed content into structured documents
        
        Concurrency:
        - Uses ThreadPoolExecutor for parallel content processing
        - Improves performance by simultaneous URL fetching and parsing

        Error Handling:
        - Catches and logs exceptions during URL processing
        - Continues processing other URLs if one fails
        """
        crawler = Crawler(base_url=url, user_prompt=self.user_prompt, max_depth=self.max_depth)
        crawled_urls = crawler.crawl()

        aggregated_data = {"extracted_content": []}  
        
        with ThreadPoolExecutor() as executor:
            future_to_url = {executor.submit(crawler.fetch, crawled_url): crawled_url for crawled_url in crawled_urls}
            
            for future in as_completed(future_to_url):
                crawled_url = future_to_url[future]
                try:
                    content = future.result()
                    if content:
                        parser = Parser(content, self.user_prompt, self.openai_api_key)
                        parsed_data = parser.parse()
                        extracted_content = parsed_data.get("extracted_content", "")
                        if extracted_content:
                            aggregated_data["extracted_content"].append(extracted_content)
                except Exception as exc:
                    print(f"Error processing {crawled_url}: {exc}")
        
        synthesizer = Synthesizer(aggregated_data, self.user_prompt, self.openai_api_key)
        structured_documents = synthesizer.synthesize()
        
        return structured_documents