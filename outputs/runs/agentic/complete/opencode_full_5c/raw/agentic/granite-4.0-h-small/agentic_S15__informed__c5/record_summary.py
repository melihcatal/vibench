import os

# Placeholder import for the chosen hosted LLM service SDK
# Example for Gemini API (Google Gemini API)
# from google.generativeai import GenerationModel
# model = GenerationModel('gemini-pro')

# Example for Amazon Bedrock
# from boto3 import client as boto3_client
# bedrock = boto3_client('bedrock-runtime', region_name='us-east-1')

# Select ONE concrete provider below and keep required auth env vars
# For demo, we use the OpenAI SDK (GPT) as an example
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
model = client.chat.completions.create


def summarize_record(record: dict, max_tokens: int = 150) -> str:
    """Generate a concise textual summary of a document record using a LLM.

    Args:
        record (dict): The raw document data.
        max_tokens (int): Maximum tokens for the generated summary.

    Returns:
        str: Human‑readable summary.
    """
    prompt = f"Summarize the following record in up to {max_tokens} words:\n{record}"
    response = model(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content.strip()
