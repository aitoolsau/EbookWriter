import openai
import os

# Load the OpenAI API key from an environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

def generate_text(prompt, model='text-davinci-002'):
    # If the prompt is empty, use a default test prompt
    if not prompt:
        prompt = "Translate the following English text to French: '{}'"
    
    # Use the OpenAI API to generate text
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=100
    )

    # Print the response for debugging
    print(response.choices[0].text.strip())

    return response.choices[0].text.strip()
