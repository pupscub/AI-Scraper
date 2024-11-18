#test.py

import google.generativeai as genai
import dotenv
import os

dotenv.load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def test(user_input: str) -> list[str]: 
    # Use an f-string to properly insert user_input into the prompt
    prompt = f"""
    You are an intelligent assistant designed to extract relevant keywords from user input. The user will provide a request related to web scraping, and your task is to identify and return only the most important keywords that represent the fields or values that need to be scraped. Return the keywords as a list of strings.

    User Input: "Hi, can you please scrape all the prices and discount values of Black Friday deals from Amazon?"

    Extracted Keywords: ['Prices', 'Discount', 'Black Friday Deals']

    Now, extract the keywords from the following user input:
    "{user_input}"
    
    Return the result as a list of strings.
    """
    
    # Generate content using the model
    response = model.generate_content(prompt)
    
    # Accessing _result instead of result
    if hasattr(response, '_result') and response._result.candidates:
        # Extract and return only the text content (which should be a list of strings)
        result = response._result.candidates[0].content.parts[0].text.strip()
        print(result)
        return result
    else:
        print("No valid candidates found.")
        return []

if __name__ == '__main__':
    user_input = "From the given URL of Chima, get me list of all products they have"
    test(user_input)