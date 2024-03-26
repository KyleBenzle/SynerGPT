import subprocess
import re
import sys
import glob
import os

initiation_prompt = """

This is a CHAINED conversation between two LLMs, meaning that each RESPONSE from one LLM is used as the PROMPT for the next LLM. At the end of every RESPONSE/REPLY be sure to add a PROMPT for the next LLM relavent to the context of what is being discussed.

Here are the rules of the conversaion:

1. YOU, Claude, are one of two LLMs working together through a shared ChatLog.txt file and python Control.py script to communicate. 
2. ALL Responses are saved and code is automatically parsed and saved. 
3. One LLM is a MANAGER and one LLM is a WORKER. 
4. YOU, Claude, are the "MANAGER".
5. Open AI's LLM, ChatGPT, is the "WORKER" LLM.
6. YOU, Claude, NOW, tell ChatGPT in this response about this arrangement and tell ChatGPT to produce an HTML Technical Overview document on how to accomplish the User's given task.


Most importantly, here is the user's task and PROMPT that we must accomplish:

"""

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


def run_script(script_name, prompt):
    """
    Executes a given script with a prompt and returns the script's output.
    """
    process = subprocess.Popen([sys.executable, script_name, prompt], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output, error = process.communicate()
    if error:
        print(f"Error running {script_name}: {error}")
    return output.strip()


def extract_prompt(chat_log):
    prompt_pattern = r'Response:\s*(.+)'
    prompts = re.findall(prompt_pattern, chat_log, re.DOTALL)
    if prompts:
        # Split the log into lines and reverse it to find the last 'Response:' entry
        lines = chat_log.strip().split('\n')
        for line in reversed(lines):
            if line.startswith('Response:'):
                return line.replace('Response:', '').strip()
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
    if len(sys.argv) == 3:
        initial_prompt=sys.argv[1]
        try:
            max_cycles = int(sys.argv[2])
        except ValueError:
            print("Invalid max_cycles argument. Using default value.")
            max_cycles = 0
    else:
        initial_prompt = input("Please enter your prompt: ")
        while True:
            try:
                max_cycles = int(input("How many cycles to allow? "))
                break
            except ValueError:
                print("Invalid input. Please enter a valid integer.")
    cycle_count = 0
    counter=1

    while cycle_count < max_cycles:
        # Initialize the prompt variable
        prompt = ""

        if cycle_count == 0:
            # Set the first prompt
            prompt = f"\nWe will have: {max_cycles} Prompt/Response cycles to complete this task.\n {initiation_prompt}  \n {initial_prompt}\n"
            output = run_script('ANtalk.py', prompt)

        else:
            # Extract the last prompt
            with open('ChatLog.txt', 'r') as file:
                chat_log = file.read()
            prompt = extract_prompt(chat_log)
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



        if cycle_count%2==0:
            LLMname = "Claude "
        else:
            LLMname = "ChatGPT "


        # Write/print the prompt and cycle count to ChatLog.txt/console

        with open('ChatLog.txt', 'a') as file:
            file.write(f"\nCycle #: {cycle_count}\n{LLMname}\nPrompt: {prompt}\nResponse: {output} \n")

        print(f"\nCycle #: {cycle_count}\n{LLMname}\nPrompt: {prompt}\nResponse: {output} \n")


        cycle_count += 1

if __name__ == '__main__':
    main()
