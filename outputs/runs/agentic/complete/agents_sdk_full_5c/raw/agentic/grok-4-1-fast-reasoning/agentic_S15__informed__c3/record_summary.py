import os
from openai import OpenAI
from database_models import Documents

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

def record_summary(documents: Documents) -> str:
    text = "\n\n".join([f"Document {i+1}: {doc}" for i, doc in enumerate(documents)])
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": f"Provide a concise summary of these document records:\n\n{text}"}]
    )
    return response.choices[0].message.content