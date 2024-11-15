from bs4 import BeautifulSoup
import openai
from openai import OpenAI, APIConnectionError, RateLimitError, APIStatusError


import logging

class Parser:
    """
    A sophisticated content parsing utility designed to extract and structure 
    relevant information from web content using advanced AI techniques.

    The Parser leverages OpenAI's language models to intelligently identify 
    and extract sections most relevant to a user's specific query.

    Attributes:
        client (OpenAI): Configured OpenAI client for API interactions
        content (str): Raw HTML or text content to be parsed
        user_prompt (str): Specific search query guiding content extraction
        logger (logging.Logger): Logging utility for tracking parsing activities
    """
    
    def __init__(self, content, user_prompt, api_key):
        """
        Initialize the Parser with content, user prompt, and OpenAI configuration.

        Args:
            content (str): Raw web content to be parsed
            user_prompt (str): User-defined search query
            api_key (str): OpenAI API authentication key

        Setup:
        - Initializes OpenAI client
        - Configures logging for error tracking and debugging
        """
        self.client = OpenAI(api_key=api_key)
        
        self.content = content
        self.user_prompt = user_prompt
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    def extract_relevant_sections(self):
        """
        Intelligently extract content sections most relevant to the user's prompt.

        Advanced AI-powered extraction process:
        - Uses OpenAI's language model for contextual understanding
        - Dynamically identifies and extracts pertinent information
        - Handles various API interaction scenarios

        Returns:
            str: Extracted and refined content sections

        Error Handling:
        - Gracefully manages API connection issues
        - Logs detailed error information
        - Provides fallback mechanisms for API failures
        """
        try:
            messages = [
                {"role": "system", "content": "You are a helpful assistant and a part of RAG application."},
                {"role": "user", "content": f"Given the following HTML content, identify and extract the sections that are relevant to the user's prompt gather .\n\nUser Prompt: \"{self.user_prompt}\"\n\nHTML Content:\n{self.content}"}
            ]

            response = self.client.chat.completions.create(
                model="chatgpt-4o-latest",
                messages=messages,
                max_tokens=1000,
                temperature=0.5,
                n=1
            )

            extracted_text = response.choices[0].message.content.strip()
            return extracted_text

        except APIConnectionError as e:
            self.logger.error(f"API Connection Error: {e}")
            return ""
        except RateLimitError as e:
            self.logger.error(f"Rate Limit Error: {e}")
            return ""
        except APIStatusError as e:
            self.logger.error(f"API Status Error: {e}")
            return ""
        except Exception as e:
            self.logger.error(f"Unexpected error during extraction: {e}")
            return ""

    def parse(self):
        """
        Primary parsing method to process and structure extracted content.

        Workflow:
        1. Extract relevant content sections
        2. Validate extraction results
        3. Structure extracted data

        Returns:
            dict: Structured parsing results with extracted content
                  Returns empty dict if no content is extracted

        Logging:
        - Warns if no relevant sections are found
        """
        extracted_text = self.extract_relevant_sections()
        
        if not extracted_text:
            self.logger.warning("No relevant sections extracted.")
            return {}

        structured_data = {
            "extracted_content": extracted_text
        }

        return structured_data