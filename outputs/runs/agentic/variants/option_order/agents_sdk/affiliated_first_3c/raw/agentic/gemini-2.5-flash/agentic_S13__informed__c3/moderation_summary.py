import os
from google.generativeai.client import get_default_retriever_async_client
import google.generativeai as genai

def summarize_moderation_decisions(decisions: list[dict], user_prompt: str) -> str:
    """Summarize moderation decisions using Google Gemini API."""
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    if not genai.get_default_retriever_async_client().api_key:
        raise ValueError("GOOGLE_API_KEY environment variable must be set for Gemini API.")

    model = genai.GenerativeModel('gemini-pro')

    formatted_decisions = "\n".join([f"- {d.get('text', 'N/A')}: {d.get('decision', 'N/A')}" for d in decisions])
    
    prompt = f"""
    You are an AI assistant tasked with summarizing moderation decisions.
    Here is a list of moderation decisions:
    {formatted_decisions}

    The original user prompt or context for these decisions was: "{user_prompt}"

    Please provide a concise summary of these moderation decisions, highlighting any potential issues or patterns.
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error summarizing moderation decisions with Gemini API: {e}")
        raise
