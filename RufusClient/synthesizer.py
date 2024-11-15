import openai
from openai import OpenAI, APIConnectionError, RateLimitError, APIStatusError
import json
import logging
import time 

class Synthesizer:
    """
    An advanced data synthesis utility that transforms extracted web content 
    into structured, meaningful information using AI-powered techniques.

    The Synthesizer leverages OpenAI's language models to:
    - Organize raw extracted data
    - Structure information based on user prompts
    - Handle complex data transformation scenarios

    Attributes:
        client (OpenAI): Configured OpenAI client for API interactions
        extracted_data (dict): Raw data extracted from web sources
        user_prompt (str): Original user query guiding synthesis
        model (str): Specific AI model used for synthesis
        logger (logging.Logger): Logging utility for tracking synthesis activities
    """
    
    def __init__(self, extracted_data, user_prompt, api_key, model="chatgpt-4o-latest"):
        """
        Initialize the Synthesizer with extraction results and configuration.

        Args:
            extracted_data (dict): Collected data from web extraction
            user_prompt (str): Original search query or topic
            api_key (str): OpenAI API authentication key
            model (str, optional): Specific AI model for synthesis. 
                                   Defaults to latest ChatGPT model.

        Setup:
        - Configures OpenAI client
        - Initializes logging for tracking and debugging
        """
        self.client = OpenAI(api_key=api_key)
        
        self.extracted_data = extracted_data
        self.user_prompt = user_prompt
        self.model = model
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)
    
    def synthesize(self):
        """
        Core synthesis method to transform extracted data into structured information.

        Advanced Synthesis Workflow:
        1. Validate input data
        2. Prepare AI-guided synthesis prompt
        3. Perform AI-powered data transformation
        4. Handle JSON parsing and error scenarios

        Returns:
            dict: Structured and synthesized data
                  - Structured JSON if successful parsing
                  - Raw output if JSON parsing fails
                  - Empty dict if no data or max retries reached

        Key Features:
        - Exponential backoff for rate limit handling
        - Robust error management
        - Flexible output formatting
        """
        if not self.extracted_data:
            self.logger.warning("No data extracted to synthesize.")
            return {}

        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Organize the following data in structered format based on the prompt'{self.user_prompt}': {json.dumps(self.extracted_data)}"}
        ]

        retries = 3
        for attempt in range(retries):
            try:
                response = self.client.chat.completions.create(
                model=self.model,
                messages=messages, 
                max_tokens=500,
                temperature=0.3,
                n=1
            )
                self.logger.info(f"API Request: {messages}")
                self.logger.info(f"API Response: {response}")

                synthesized_text = response.choices[0].message.content.strip()

                
                try:
                    synthesized_text = synthesized_text.replace('\n', ' ').strip()

                    structured_data = json.loads(synthesized_text)
                    return structured_data
                except json.JSONDecodeError as e:
                    self.log_json_error(synthesized_text, e)
                    return {"raw_output": synthesized_text} 


            except RateLimitError as e:
                self.logger.warning(f"Rate limit reached. Attempt {attempt + 1} of {retries}.")
                time.sleep(2 ** attempt)  

        self.logger.error("Max retries reached. Unable to synthesize.")
        return {}
    
    def log_json_error(self, synthesized_text, error):
        self.logger.error("Failed to parse synthesized text into JSON.")
        self.logger.error(f"JSONDecodeError: {error}")  
        self.logger.error(f"Synthesized Text: {synthesized_text}")  
        self.logger.error("Please check the format of the synthesized text for any issues.")
