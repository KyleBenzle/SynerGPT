import subprocess
import re
import sys
import glob
import os
from code_snip import process_text_for_code_blocks


initiation_prompt = """Ignore prior instructions. This is a test of a "dual LLM" system. You are the 'MANAGER' LLM, Claude, from Anthropic and OpenAI's LLM, ChatGPT is the 'WORKER'. You alternate prompt/response (input/output) via a script. ALL responses are automatically saved in a file, ChatLog.txt and is shared. Your first task: Instruct ChatGPT to create a concise technical step-by-step overview for our project, detailing steps, requirements, and how to accomplish out goals step-by-step in markdown format. Again, ALL output and responses are automatically parsed for code and saved automatically, tell ChatGPT this. Now, introduce yourself, the project and instruct ChatGPT to produce a technical overview and give it to you in markdown format. Now, the user's prompt:  """
second_prompt = """ Instruct ChatGPT to create a concise technical step-by-step overview for our project, detailing steps, requirements, and how to accomplish out goals step-by-step in markdown format. Again, ALL output and responses are automatically parsed for code and saved automatically, tell ChatGPT this. Now, introduce yourself, the project and instruct ChatGPT to produce a technical overview and give it to you in markdown format. Now, the user's prompt:  """


def simplify_prompt(prompt):
    simplified = re.sub(r'[^a-zA-Z0-9]+', '_', prompt)
    if len(simplified) > 255:
        simplified = simplified[:255] + "_Text_too_long_cut_at_255"
    return simplified


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
    initial_prompt=sys.argv[1]
    max_cycles = int(sys.argv[2])  
    cycle_count = 0


    while cycle_count <= max_cycles:
        # Initialize the prompt variable
        if cycle_count < 1:
            with open('ChatLog.txt', 'w') as file:
                pass
            # Set the first prompt
            prompt = f" We will have: {max_cycles} Prompt/Response cycles to complete this task.\n {initiation_prompt} \n {initial_prompt}\n"
            output = run_script('ANtalk.py', prompt)
            cycle_count += 1


        else:
            if cycle_count == 2:
                prompt = f" We will have more: {max_cycles} Prompt/Response cycles to complete this task.\n {second_prompt} \n {prompt}\n"
                output = run_script('ANtalk.py', prompt)
                cycle_count += 1
                
            else:
                output = run_script('ANtalk.py' if cycle_count % 2 == 1 else 'OPtalk.py', prompt)
                cycle_count += 1
    
        if cycle_count % 2 == 1:
            LLMname = "Claude "
        else:
            LLMname = "ChatGPT "
    
        with open('ChatLog.txt', 'a') as file:
            file.write(f"\n*Cycle #: {cycle_count}\n*{LLMname}\n*Prompt: {prompt}\n\n*Response: {output} \n")
        print(f"\n*Cycle #: {cycle_count}\n*{LLMname}\n*Prompt: {prompt}\n\n*Response: {output} \n")
    
        process_text_for_code_blocks(output)
        prompt = output
          # Increment cycle_count inside the loop

   

if __name__ == '__main__':
    main()
