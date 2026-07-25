from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("AI_API_KEY"), base_url="https://api.groq.com/openai/v1")

response = client.chat.completions.create(
    model=os.getenv("AI_MODEL"),
    messages=[
        {"role": "user", "content": "Say 'API is working' if you can read this."}
    ]
)

print(response.choices[0].message.content)