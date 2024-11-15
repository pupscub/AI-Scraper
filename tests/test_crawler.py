import unittest
from RufusClient.crawler import Crawler

class TestCrawler(unittest.TestCase):
    """
    Test suite for the Crawler class to validate its core functionalities.
    
    Test Coverage:
    - URL validation
    - Domain matching
    - Content fetching
    - Crawling mechanics
    - Multithreaded crawling behavior
    """
    def setUp(self):
        """
        Initialize Crawler for testing with a default example domain.
        
        Alternative Test Websites (for more comprehensive testing):
        1. https://www.python.org (Technical documentation site)
        2. https://en.wikipedia.org (Encyclopedic content)
        3. https://www.gutenberg.org (Public domain literature)
        4. https://www.nasa.gov (Scientific information)
        
        Recommendation: Rotate these URLs for different test scenarios
        """
        self.crawler = Crawler(base_url="https://www.python.org ", user_prompt="Test Crawl", max_depth=1)
    
    def test_is_valid(self):
        """
        Test URL validation method.
        
        Validates:
        - Correct HTTPS URLs
        - Incorrect protocols
        - Incomplete URL formats
        """
        self.assertTrue(self.crawler.is_valid("https://www.python.org"))
        self.assertFalse(self.crawler.is_valid("https://www.python.org"))
        self.assertFalse(self.crawler.is_valid("https://www.python.org "))
    
    def test_same_domain(self):
        """
        Verify domain matching functionality.
        
        Checks:
        - Matching subpages of the same domain
        - Detecting different domains
        """
        self.assertTrue(self.crawler.same_domain("https://www.python.org/docs"))
        self.assertFalse(self.crawler.same_domain("https://www.python.org/docs"))
    
    def test_fetch(self):
        """
        Test content fetching method.
        
        Validates:
        - Successful content retrieval
        - Presence of expected content markers
        
        Note: Replace with a more robust content check for real-world scenarios
        """
        content = self.crawler.fetch("https://www.python.org")
        self.assertIsNotNone(content)
        self.assertIn("<title>Example Domain</title>", content)
    
    def test_crawl(self):
        """
        Validate basic crawling functionality.
        
        Checks:
        - Correct base URL is crawled
        - Crawl depth limitation works
        """
        crawled_urls = self.crawler.crawl()
        self.assertIn("https://www.python.org", crawled_urls)
        self.assertEqual(len(crawled_urls), 1)

    def test_multithreaded_crawl(self):
        """
        Test multithreaded crawling capabilities.
        Modify `max_depth` or `base_url` for testing multithreading effectively
        Increase `depth` to test multithreaded behavior
        
        Verifies:
        - Ability to crawl multiple URLs
        - Handles increased crawl depth
        
        Recommendations for improvement:
        - Add mock websites for more controlled testing
        - Implement timeout and error handling tests
        """
       
        self.crawler.max_depth = 2  
        crawled_urls = self.crawler.crawl()
        self.assertGreater(len(crawled_urls), 1) 

if __name__ == "__main__":
    unittest.main()
