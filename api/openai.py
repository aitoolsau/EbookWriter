import os
import openai
from config import openai_api_key

openai.api_key = openai_api_key
openai.organization = "org-ZQOf6hs159BbSTWZ6iPesyqm"

def generate_text(prompt):
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
        {
          "role": "user",
          "content": prompt
        }
      ]
    )
    return response['choices'][0]['message']['content']

# Test the function
if __name__ == "__main__":
    prompt = "Translate the following English text to French: '{}'"
    print(generate_text(prompt.format("Hello, how are you?")))
