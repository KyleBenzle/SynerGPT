import openai
import os
import re
from datetime import datetime
import hashlib
import sys  # Import sys to access command line arguments

# Set your OpenAI API key here
openai.api_key = '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'

def guess_language(code_snippet):
    """
    Guesses the programming language of a code snippet based on simple heuristics.
    Returns an appropriate file extension.
    """
    if re.search(r'<html', code_snippet, re.IGNORECASE):
        return 'html'
    elif re.search(r'{|}', code_snippet) and re.search(r'function|var ', code_snippet):
        return 'js'
    elif re.search(r'@import|{', code_snippet):
        return 'css'
    elif re.search(r'def |import |class ', code_snippet):
        return 'py'
    else:
        return 'txt'

def extract_code(text):
    """
    Extracts code snippets from the given text using a basic pattern.
    This function is a simple heuristic and might need adjustments.
    """
    code_pattern = re.compile(r'```(.*?)\n(.*?)\n```', re.DOTALL)
    code_snippets = code_pattern.findall(text)
    return [(lang, code) for lang, code in code_snippets]

def simplify_prompt(prompt):
    """
    Simplifies the user prompt to use in the filename.
    Removes special characters and limits length.
    """
    simplified = re.sub(r'[^a-zA-Z0-9]+', '_', prompt)
    return simplified[:30]  # Limit length to 30 characters

def main():
    # Check if a prompt was provided as a command line argument
    if len(sys.argv) < 2:
        print("No prompt provided. Usage: python script.py 'Your prompt here'")
        sys.exit(1)
    
    user_prompt = ' '.join(sys.argv[1:])  # Join all arguments into a single prompt string
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_prompt}
        ]
    )
    
    response_text = response['choices'][0]['message']['content']
    
    print(response_text)  # Print the response to standard output
    
#    with open("ChatLog.txt", "a") as file:
#        # file.write(f"\n\nWorker Prompt: {user_prompt}\n")
#        file.write(f"\n\nWorker Response: {response_text}\n")
    
    # Extract code snippets from the response
    code_snippets = extract_code(response_text)
    if code_snippets:
        simplified_prompt = simplify_prompt(user_prompt)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        
        for i, (lang, snippet) in enumerate(code_snippets, start=1):
            lang_extension = guess_language(snippet)
            hash_digest = hashlib.md5(snippet.encode()).hexdigest()[:8]
            filename = f"{simplified_prompt}_{i}.{lang_extension}"
            with open(filename, "w") as code_file:
                code_file.write(snippet.strip())
                print(f"Code snippet saved to {filename}")

if __name__ == "__main__":
    main()
