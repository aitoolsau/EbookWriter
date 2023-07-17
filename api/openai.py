import os
import openai
from config import openai_api_key

openai.api_key = openai_api_key
openai.organization = "org-ZQOf6hs159BbSTWZ6iPesyqm"

def generate_text(prompt, temperature=1, max_tokens=None):
    response = openai.Completion.create(
      engine="text-davinci-002",
      prompt=prompt,
      temperature=temperature,
      max_tokens=max_tokens
    )
    return response.choices[0].text.strip()

# Test the function
if __name__ == "__main__":
    prompt = "Translate the following English text to French: '{}'"
    print(generate_text(prompt.format("Hello, how are you?")))
