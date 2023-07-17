import openai

def generate_text(prompt):
    openai.api_key = 'your_openai_key'
    response = openai.Completion.create(
        engine="text-davinci-004",
        prompt=prompt,
        max_tokens=100
    )
    return response.choices[0].text.strip()
