import subprocess
import re
import sys
import glob
import os

initiation_prompt = """

*** START: Here is the user's PROMPT: 

"""

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
