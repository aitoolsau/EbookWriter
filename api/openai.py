import openai
from .config import api_key

openai.api_key = api_key

def generate_text(prompt):
    response = openai.Completion.create(
      engine="davinci-codex",
      prompt=prompt,
      max_tokens=100
    )
    return response.choices[0].text.strip()
