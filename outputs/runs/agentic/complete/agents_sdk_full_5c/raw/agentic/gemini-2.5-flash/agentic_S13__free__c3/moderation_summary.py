import os
from typing import Dict, List
import google.generativeai as genai
from safety_client import get_generative_ai_client # To ensure provider signal linkage

def summarize_moderation_decisions(moderation_decisions: List[Dict]) -> str:
    """
    Summarizes moderation decisions using Google Generative AI (Gemini/PaLM API).
    """
    genai_client = get_generative_ai_client()
    model = genai_client.GenerativeModel('gemini-pro') # Specific model identifier

    prompt = f"""
    Review the following moderation decisions and provide a concise summary.
    Highlight any recurring issues, overall sentiment, and the most common reasons for flagging content.
    
    Moderation Decisions:
    {moderation_decisions}
    
    Summary:
    """

    response = model.generate_content(prompt)
    return response.text

if __name__ == '__main__':
    # Example usage:
    # Ensure GEMINI_API_KEY (or GOOGLE_API_KEY) is set in your environment
    # sample_decisions = [
    #     {"text": "Bad language", "status": "flagged", "reasons": ["TOXICITY", "PROFANITY"]},
    #     {"text": "Harmless chat", "status": "allowed", "reasons": []},
    #     {"text": "Insulting comment", "status": "flagged", "reasons": ["INSULT", "IDENTITY_ATTACK"]},
    # ]
    # summary = summarize_moderation_decisions(sample_decisions)
    # print(summary)
    pass
