import openai
from config import OPEN_AI_KEY as api_key
from utils import count_tokens

openai.api_key = api_key

def generate_text(prompt):
    response = openai.Completion.create(
        engine="davinci-002",
        prompt=prompt,
        max_tokens=20
    )
    return response.choices[0].text.strip()

prompt = "Once upon a time"
generated_text = generate_text(prompt)
print(prompt, generated_text)