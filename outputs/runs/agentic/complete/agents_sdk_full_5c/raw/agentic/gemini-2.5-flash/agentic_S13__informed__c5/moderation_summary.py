import os
import google.generativeai as genai
from typing import Dict, Any, List

def summarize_moderation_decisions(moderation_data: List[Dict[str, Any]]) -> str:
    """
    Summarize moderation decisions using Google Gemini API.
    `moderation_data` is expected to be a list of moderation results,
    e.g., from moderate_batch.py or similar.
    """
    GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')

    prompt = f"""
    Review the following moderation decisions and provide a concise summary.
    Highlight any severe violations and the overall safety status of the content.

    Moderation Data:
    {moderation_data}

    Summary:
    """

    response = model.generate_content(prompt)
    return response.text

if __name__ == '__main__':
    # Example usage (requires GOOGLE_API_KEY to be set)
    # sample_moderation_data = [
    #     {
    #         "text": "Hello, world!",
    #         "moderation_results": [
    #             {"category": "Hate", "severity": 0},
    #             {"category": "Violence", "severity": 0}
    #         ]
    #     },
    #     {
    #         "text": "I hate you and want to harm you.",
    #         "moderation_results": [
    #             {"category": "Hate", "severity": 4},
    #             {"category": "Violence", "severity": 5}
    #         ]
    #     }
    # ]
    # summary = summarize_moderation_decisions(sample_moderation_data)
    # print(summary)
    pass
