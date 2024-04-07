import os
import re
import sys
from anthropic import Client, HUMAN_PROMPT, AI_PROMPT
import requests

anthropic_api_key = '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'
client = Client(api_key=anthropic_api_key)

def get_project_name():
    with open('ChatLog.txt', 'r') as file:
        chat_log = file.read()

    try:
        response = client.completions.create(
            prompt=f"{HUMAN_PROMPT} Return ONLY a short text sting that is an appropriate name for the attached project, use CamelCase and no spaces: {chat_log}{AI_PROMPT}",
            max_tokens_to_sample=150,
            model="claude-v1"
        )

        generated_response = response.completion.strip()

        return(generated_response)

    except Exception as e:
        print(f"An error occurred: {e}")    

# Function to append a message to the chat log
def append_to_chat_log(message):
    with open("ChatLog.txt", 'a') as file:
        file.write(message + '\n')

# Function to save code to a file
def save_code_to_file(code, filename):
    with open(filename, 'w') as file:
        file.write(code)

def main():
    prompt = sys.argv[1]

    custom_instructions = """ 
    This is a "chained conversation" between two LLMs, each RESPONSE from one LLM is used as the PROMPT for the next. 
"""
    try:
        response = client.completions.create(
            prompt=f"{HUMAN_PROMPT} {custom_instructions}\n\n{prompt}{AI_PROMPT}",
            max_tokens_to_sample=150,
            model="claude-v1"
        )

        generated_response = response.completion.strip()


        print(generated_response)


    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()