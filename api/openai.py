import openai

openai.api_key = 'your-api-key'

def generate_text(prompt):
    response = openai.Completion.create(
      engine="text-davinci-002",
      prompt=prompt,
      max_tokens=100
    )
    return response.choices[0].text.strip()
