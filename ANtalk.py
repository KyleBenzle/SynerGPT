import os
import re
import sys
from anthropic import Client, HUMAN_PROMPT, AI_PROMPT

# Replace 'your_anthropic_api_key' with your actual API key
anthropic_api_key = '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'

# Initialize the Anthropic API client
client = Client(api_key=anthropic_api_key)

# Function to append a message to the chat log
def append_to_chat_log(message):
    with open("ChatLog.txt", 'a') as file:
        file.write(message + '\n')

# Function to save code to a file
def save_code_to_file(code, filename):
    with open(filename, 'w') as file:
        file.write(code)

def main():
    # Get the prompt from the command line arguments
    if len(sys.argv) < 2:
        print("Please provide a prompt as a command line argument.")
        sys.exit(1)
    prompt = sys.argv[1]

    try:
        # Send the prompt to the Anthropic API and get the response
        response = client.completions.create(
            prompt=f"{HUMAN_PROMPT} {prompt}{AI_PROMPT}",
            max_tokens_to_sample=150,
            model="claude-v1"
        )

        # Extract the generated response
        generated_response = response.completion.strip()

        # Append the prompt and response to the chat log
        append_to_chat_log(f"Prompt: {prompt}")
        append_to_chat_log(f"Response: {generated_response}")

        # Check if the response contains code
        code_blocks = re.findall(r'```(.+?)\n(.+?)```', generated_response, re.DOTALL)
        for language, code in code_blocks:
            # Determine the file extension based on the code language
            if 'python' in language.lower():
                file_extension = '.py'
            elif 'javascript' in language.lower():
                file_extension = '.js'
            elif 'html' in language.lower():
                file_extension = '.html'
            elif 'css' in language.lower():
                file_extension = '.css'
            else:
                file_extension = '.txt'
            
            # Save the code to a file with an appropriate name
            filename = f"code_snippet{file_extension}"
            save_code_to_file(code.strip(), filename)
            print(f"Code saved to {filename}")

        print(generated_response)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()