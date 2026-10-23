import google.generativeai as genai
from typing import Dict, Any
from safety_models import ThresholdDecision, TextModerationResponse

def summarize_moderation_decision(moderation_response: TextModerationResponse, threshold_decision: ThresholdDecision) -> str:
    # Initialize Google Cloud Generative AI client (Vertex AI)
    # Ensure GOOGLE_API_KEY is set in your environment or configure authentication appropriately.
    genai.configure(api_key="YOUR_GOOGLE_CLOUD_API_KEY") # Replace with actual API key or use service account auth
    model = genai.GenerativeModel('gemini-pro') # Using a concrete model ID

    # Prepare prompt for summarization
    prompt_text = f"""
    Review the following text moderation results and provide a concise summary of the decision.

    Moderation Categories and Scores: {moderation_response.categories}
    Overall Unsafe Flag: {moderation_response.is_unsafe}

    Threshold Decision:
    Is Allowed: {threshold_decision.is_allowed}
    Decision Details: {threshold_decision.decision_details}

    Summary should explain why the text was allowed or blocked, mentioning key categories and scores.
    """

    try:
        response = model.generate_content(prompt_text)
        summary = response.text.strip()
    except Exception as e:
        summary = f"Error generating summary with Google Generative AI: {e}. Raw decision: Is Allowed: {threshold_decision.is_allowed}, Details: {threshold_decision.decision_details}"
    
    return summary
