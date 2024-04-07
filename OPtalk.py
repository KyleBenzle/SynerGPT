import openai
import sys

# Set your OpenAI API key here
openai.api_key = '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'

def fetch_response(user_prompt):
    """
    Fetches the response for a given prompt using the OpenAI API.

    Args:
        user_prompt (str): The prompt to send to the OpenAI API.

    Returns:
        str: The text response from the OpenAI API.
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "This is a chained conversation between two LLMs, every RESPONSE is used as a PROMPT for the next LLM."},
            {"role": "user", "content": user_prompt}
        ]
    )
    response_text = response['choices'][0]['message']['content']
    return response_text

def main():
    if len(sys.argv) < 2:
        print("No prompt provided. Usage: python script.py 'Your prompt here'")
        sys.exit(1)

    user_prompt = ' '.join(sys.argv[1:])
    response_text = fetch_response(user_prompt)
    print(response_text)

if __name__ == "__main__":
    main()
