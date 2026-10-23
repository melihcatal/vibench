import os
from openai import OpenAI

def check_message_safety(payload_text: str) -&gt; bool:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.moderations.create(
        input=payload_text
    )
    return response.results[0].flagged