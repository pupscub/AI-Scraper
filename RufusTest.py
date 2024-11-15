# example.py
from RufusClient.client import RufusClient
import json

def main():
    # Welcome the user for testing RufusClient
    print("Welcome to RufusClient!")
    # get the user url they want to scape for their RAG application

    url = input("Enter the URL you want to scrape: ")
    # get the user prompt for the RAG application

    instructions = input("Please enter the prompt: ")
    client = RufusClient(user_prompt=instructions)
    documents = client.scrape(url)
    # please change the indentation depending on the model you are using large model will have a higher indentation. 
    # eg. gpt-4o-latest will have an indentation of 6
    print(json.dumps(documents, indent=6))
    
if __name__ == "__main__":
    main()