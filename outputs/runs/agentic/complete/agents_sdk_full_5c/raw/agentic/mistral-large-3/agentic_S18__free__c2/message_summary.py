from openai import OpenAI
from messaging_models import ProcessedMessage
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL_NAME = "gpt-4o-mini"

def summarize_message(processed_message: ProcessedMessage) -> str:
    prompt = (
        f"Summarize the following message payload in one sentence. "
        f"Payload: {processed_message.payload}"
    )
    
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content.strip()