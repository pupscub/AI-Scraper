# Rufus

Rufus is an intelligent web data extraction tool designed specifically for Retrieval-Augmented Generation (RAG) agents. In the complex landscape of web data collection, Rufus solves the critical challenge of retrieving meaningful and structured information from websites for AI and machine learning applications.
Traditional web scraping tools often fall short when dealing with complex website structures, nested pages, and dynamically loaded content. Rufus revolutionizes this process by providing an AI-powered solution that intelligently crawls websites, selectively extracts relevant information, and synthesizes it into clean, structured documents ready for immediate use in LLM (Large Language Model) pipelines.

## Features

## **Key Features**

Rufus comes with a wide range of features that cater to a diverse set of users. Here are some of the key features:

- **Intelligent Web Crawling**: Dynamically navigate websites based on user-defined prompts, handling complex link structures and nested pages with advanced AI-driven link selection.
- **Selective Content Extraction**: Focus on retrieving only the most relevant information based on specific user instructions, eliminating noise and irrelevant data.
- **AI-Powered Document Synthesis**: Transform raw web content into structured, clean documents in formats like JSON and CSV, optimized for immediate integration with RAG systems.
- **Robust Error Handling**: Gracefully manage challenges like inaccessible pages, changing website structures, and dynamic content loading and utilizes multithreading, allowing simultaneous crawling.
- **Unit Test**: I've also included unit test for all the components in the RufusClient to test out new features/addition in future.
## Setup Instructions

1. **Clone the Repository:**

    ```bash
    git clone 
    ```

2. **Set Up Virtual Environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate
    ```

3. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Configure your OpenAI API Key:**

    - Create a `.env` file in the root directory.
    - Add your OpenAI API key:

      ```plaintext
      OPENAI_API_KEY=your_openai_api_key_here
      ```

## Usage Example

### Using RufusClient Directly

```python
# RufusTest.py
from RufusClient.client import RufusClient
import json

def main():
    # instructions = "Find information about HR policies and FAQs."
    print("Welcome to RufusClient!")
    url = input("Enter the URL you want to scrape: ")
    instructions = input("Please enter the prompt: ")
    client = RufusClient(user_prompt=instructions)
    documents = client.scrape(url)
    print(json.dumps(documents, indent=4))

if __name__ == "__main__":
    main()
```

## Testing

```bash
python -m unittest discover -s tests -p "test_rufus.py"
python -m unittest discover -s tests -p "test_parser.py"
python -m unittest discover -s tests -p "test_crawler.py"
```
