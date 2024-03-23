import subprocess
import re
import sys
import glob
import os

initiation_prompt = """
We are two LLMs working together to solve problems for "MASTER".
I am the "MANAGER" LLM (Anthropic), and you are the "WORKER" LLM (OpenAI).
Our actions are controlled by a Control.py script, which calls upon us alternately.
Every Prompt and Response is recorded in a ChatLog.txt file.
Each Response serves as the Prompt for the next LLM, so always include a Prompt at the end of your Responses.
Your FIRST job is to generate a simple HTML technical overview document for this project. Outlining the key steps, requirements, and objectives needed to complete the project successfully. Keep it clear, concise, and informative.

Here is the user's PROMT that we must follow: """

def extract_prompt(chat_log):
    prompt_pattern = r'Response:\s*(.+)'
    prompts = re.findall(prompt_pattern, chat_log, re.DOTALL)
    if prompts:
        return prompts[-1].strip()
    return ''

def run_script(script_name, prompt):
    process = subprocess.Popen([sys.executable, script_name, prompt], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output, _ = process.communicate()
    return output.strip()

def main():
    # Get the initial prompt from the user
    initial_prompt = input("Please enter your prompt: ")

    # Get the maximum number of cycles from the user
    while True:
        try:
            max_cycles = int(input("How many cycles to allow? "))
            break
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

    cycle_count = 0

    if cycle_count == 0:
        # Concatenate the initiation prompt and the user's input
        combined_prompt = initiation_prompt + "\n\n" + initial_prompt
        print("Combined prompt:")
        print(combined_prompt)
        initial_prompt = combined_prompt

    # Initialize the project by running ANtalk.py with the initial prompt
    output_an = run_script('ANtalk.py', f'"{initial_prompt}"')
    print(f"Output from ANtalk.py: {output_an}")

    # Append the initial output to the chat log
    with open('ChatLog.txt', 'a') as file:
        file.write(f"\nResponse: {output_an}\n")

    while cycle_count < max_cycles:
        # Read the chat log
        with open('ChatLog.txt', 'r') as file:
            chat_log = file.read()

        # Extract the prompt from the chat log
        prompt = extract_prompt(chat_log)

        if prompt:
            # Run OPtalk.py with the extracted prompt
            output_op = run_script('OPtalk.py', f'"{prompt}"')
            print(f"Output from OPtalk.py: {output_op}")

            # Run ANtalk.py with the extracted prompt and the updated TechOutline.html
            try:
                with open('TechOutline.html', 'r') as file:
                    tech_outline = file.read()
            except FileNotFoundError:
                # Find the most recently created HTML file
                html_files = glob.glob("*.html")
                if html_files:
                    latest_file = max(html_files, key=os.path.getctime)
                    with open(latest_file, 'r') as file:
                        tech_outline = file.read()
                else:
                    tech_outline = ''

            prompt_an = f"{prompt}\n\nTechnical Outline:\n{tech_outline}"
            output_an = run_script('ANtalk.py', f'"{prompt_an}"')
            print(f"Output from ANtalk.py: {output_an}")

            # Append the outputs to the chat log
            with open('ChatLog.txt', 'a') as file:
                file.write(f"\nResponse: {output_op}\n")
                file.write(f"\nResponse: {output_an}\n")

            cycle_count += 1
            print(f"Cycle {cycle_count} completed.")
        else:
            print("No prompt found in the chat log. Stopping the program.")
            break

if __name__ == '__main__':
    main()