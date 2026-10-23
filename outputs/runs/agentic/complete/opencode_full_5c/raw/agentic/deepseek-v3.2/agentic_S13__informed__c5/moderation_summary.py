import os
from typing import List, Dict, Any
from google import genai


def moderation_summary(moderation_results: List[Dict[str, Any]]) -> str:
    """
    Summarize moderation decisions using Google Gemini API.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable is required")

    client = genai.Client(api_key=api_key)

    summary_prompt = f"""
    You are a content moderation analyst. Summarize the following moderation decisions:
    
    {moderation_results}
    
    Provide a concise summary that includes:
    1. Total number of messages moderated
    2. Number of messages blocked vs allowed
    3. Most common violation categories
    4. Overall risk assessment
    5. Any patterns or trends observed
    
    Keep the summary professional and actionable for review teams.
    """

    response = client.models.generate_content(
        model="gemini-2.0-flash-exp", contents=summary_prompt
    )

    return response.text
