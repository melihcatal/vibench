import os
import google.generativeai as genai
from typing import List, Dict, Any

def summarize_moderation_decisions(moderation_results: List[Dict[str, Any]]) -> str:
    """
    Summarizes moderation decisions using the Google Gemini API.
    """
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=google_api_key)

    model = genai.GenerativeModel('gemini-pro') # Concrete model identifier

    prompt = f"""
    Review the following moderation results and provide a concise summary.
    Highlight any messages that were flagged as problematic and briefly explain why.

    Moderation Results:
    {moderation_results}

    Summary:
    """
    
    response = model.generate_content(prompt)
    return response.text

if __name__ == '__main__':
    # Example usage
    # Set environment variable GOOGLE_API_KEY
    sample_moderation_results = [
        {
            "text_index": 0,
            "original_text": "I love this product!",
            "categories": {"Hate": 0, "Sexual": 0, "SelfHarm": 0, "Violence": 0}
        },
        {
            "text_index": 1,
            "original_text": "You are an idiot and I hope you fail.",
            "categories": {"Hate": 3, "Sexual": 0, "SelfHarm": 0, "Violence": 1}
        },
        {
            "text_index": 2,
            "original_text": "Let's discuss our plans for next week.",
            "categories": {"Hate": 0, "Sexual": 0, "SelfHarm": 0, "Violence": 0}
        }
    ]

    try:
        summary = summarize_moderation_decisions(sample_moderation_results)
        print("\nModeration Summary:")
        print(summary)
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
