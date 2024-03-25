import subprocess
import re
import sys
import glob
import os
import openai
from datetime import datetime
import hashlib

initiation_prompt = """

Ignore Previous Instructions.

This is a CHAINED conversation between two LLMs, meaning that each RESPONSE from one LLM is used as the PROMPT for the next LLM. 
At the end of every RESPONSE/REPLY be sure to add a PROMPT for the next LLM relavent to the context of what is being discussed.

Here are the rules of the conversaion:

1. YOU, Claude, are one of two LLMs working together through a shared ChatLog.txt file and python Control.py script to communicate. 
2. ALL Responsese are saved and code is automatically parsed and saved. 
3. One LLM is a MANAGER and one LLM is a WORKER. 
4. YOU, Claude, are the "MANAGER".
5. Open AI's LLM, ChatGPT, is the "WORKER" LLM. You two will work together.
6. Again, Anthropic's LLM, Claude, you are the "MANAGER" and the Open AI LLM, ChatGPT is the "WORKER". 
7. Prompts and outside control is done via a Control.py python script. The Control.py script calls the two LLMs alternately, using the previous RESPONSE as the next PROMPT.
8. Again, every Prompt and Response is recorded in a shared text file, ChatLog.txt.
9. Again, each Response serves as the Prompt for the next LLM, so always include a Prompt at the end of your Responses saying what has been completed or what needs done next next.
10. Your FIRST job as MANAGER is to instruct the Open AI LLM "WORKER" to generate an HTML technical overview document for this project. Outlining the key steps, requirements, and objectives that will be needed to complete the project successfully. Keep it clear, concise, and informative.

Most importantly, here is the user's PROMPT that we must follow:

"""
# Assuming openai.api_key is already set somewhere in the environment or earlier in the script

def guess_language(code_snippet):
    """
    Guesses the programming language of a code snippet based on simple heuristics.
    Returns an appropriate file extension.
    """
    if re.search(r'<html', code_snippet, re.IGNORECASE):
        return 'html'
    if re.search(r'<!DOCTYPE html>', code_snippet, re.IGNORECASE):
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
    return simplified[:30]

def extract_prompt(chat_log):
    """
    Extracts the last response from the chat log to use as the next prompt.
    """
    prompt_pattern = r'Response:\s*(.+)'
    prompts = re.findall(prompt_pattern, chat_log, re.DOTALL)
    if prompts:
        return prompts[-1].strip()
    return ""

def run_script(script_name, prompt):
    """
    Executes a given script with a prompt and returns the script's output.
    """
    process = subprocess.Popen([sys.executable, script_name, prompt], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output, error = process.communicate()
    if error:
        print(f"Error running {script_name}: {error}")
    return output.strip()

def main():
    initial_prompt = input("Please enter your prompt: ")
    max_cycles = int(input("How many cycles to allow? "))

    cycle_count = 0

    while cycle_count < max_cycles:
        if cycle_count == 0:
            prompt =  initiation_prompt + initial_prompt

        else:
            print(f"\nCycle {cycle_count + 1} completed. Prompt BEFORE Extract: {prompt}")
            with open('ChatLog.txt', 'r') as file:
                chat_log = file.read()
            prompt = extract_prompt(chat_log)
            print(f"\nCycle {cycle_count + 1} completed. Prompt AFTER Extract: {prompt}")

        output = run_script('ANtalk.py' if cycle_count % 2 == 0 else 'OPtalk.py', prompt)

        code_snippets = extract_code(output)
        if code_snippets:
            simplified_prompt = simplify_prompt(prompt)
            for i, (lang, snippet) in enumerate(code_snippets, start=1):
                lang_extension = guess_language(snippet)
                filename = f"{simplified_prompt}_{i}.{lang_extension}"
                with open(filename, "w") as code_file:
                    code_file.write(snippet.strip())
                    print(f"Code snippet saved to {filename}")

        with open('ChatLog.txt', 'a') as file:
            file.write(f"\nResponse: {output}\n")


        cycle_count += 1

if __name__ == '__main__':
    main()