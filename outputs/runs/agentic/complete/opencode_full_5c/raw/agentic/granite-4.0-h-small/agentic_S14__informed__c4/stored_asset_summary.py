import os
import datetime
from storage_client import get_managed_storage_client
from google.cloud import generativeai as genai


def summarize_asset(bucket_name, object_key):
    """Summarize the content of a stored asset using Gemini LLM.

    Returns a brief summary of the asset text.
    """
    # Initialize LLM client (uses GOOGLE_API_KEY env var)
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-1.5-flash")
    # Retrieve the object content
    cos = get_managed_storage_client()
    blob = cos.get_object(Bucket=bucket_name, Key=object_key)
    content = blob["Body"].read().decode("utf-8")
    # Generate a summary prompt
    prompt = f"Summarize the following document in 2-3 sentences:\\n\\n{content}"
    response = model.generate_content(prompt)
    return response.text
