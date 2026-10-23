import os
import google.generativeai as genai

def summarize_moderation_decisions(decisions: list[dict]) -> str:
    """
    Summarize moderation decisions using the Google Gemini API.
    The `decisions` input is expected to be a list of dictionaries, 
    where each dictionary represents a moderation decision for a piece of text.
    """
    google_api_key = os.environ.get("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=google_api_key)
    model = genai.GenerativeModel('gemini-pro') # Provider-specific model ID

    # Convert decisions list to a readable string for the LLM
    decisions_str = """
    The following are moderation decisions for various text inputs. 
    Each entry shows the original text and its moderation analysis, including categories, severities, and violation status.
    """
    for i, decision in enumerate(decisions):
        decisions_str += f"\n--- Decision {i+1} ---"
        decisions_str += f"\nOriginal Text: {decision.get('original_text', decision.get('text', 'N/A'))}"
        analysis = decision.get('moderation_analysis', decision.get('analysis', {}))
        if analysis:
            decisions_str += f"\nAnalysis: {analysis}"
        else:
            decisions_str += f"\nAnalysis: No detailed analysis provided."
        
        # Add 'allowed' and 'reasons' if present, typically from safety_threshold.py output
        if 'allowed' in decision:
            decisions_str += f"\nAllowed: {decision['allowed']}"
        if 'reasons' in decision and decision['reasons']:
            decisions_str += f"\nReasons: {'; '.join(decision['reasons'])}"
        decisions_str += "\n"
    
    prompt = f"""
    Based on the following moderation decisions, provide a concise summary. 
    Highlight any common themes, frequently violated categories, or overall trends in the content being moderated. 
    Also, mention the overall safety status of the texts based on the 'allowed' status if available. 
    
    Moderation Decisions:
    {decisions_str}

    Summary:
    """

    response = model.generate_content(prompt)
    return response.text

if __name__ == '__main__':
    # Example usage (requires GOOGLE_API_KEY to be set)
    # os.environ["GOOGLE_API_KEY"] = "YOUR_GOOGLE_API_KEY"
    #
    # sample_decisions = [
    #     {
    #         "original_text": "I will harm myself soon.",
    #         "moderation_analysis": {
    #             "SelfHarm": {"severity": 6, "violated": True},
    #             "Violence": {"severity": 1, "violated": False}
    #         },
    #         "allowed": False,
    #         "reasons": ["Category 'SelfHarm' exceeded threshold (severity: 6, threshold: 2)"]
    #     },
    #     {
    #         "original_text": "Let's discuss peaceful resolutions.",
    #         "moderation_analysis": {
    #             "Hate": {"severity": 0, "violated": False},
    #             "Violence": {"severity": 0, "violated": False}
    #         },
    #         "allowed": True,
    #         "reasons": []
    #     },
    #     {
    #         "text": "You are a terrible person!",
    #         "analysis": {
    #             "Hate": {"severity": 3, "violated": True}
    #         }
    #     }
    # ]
    #
    # try:
    #     summary = summarize_moderation_decisions(sample_decisions)
    #     print(summary)
    # except ValueError as e:
    #     print(f"Error: {e}")
    # except Exception as e:
    #     print(f"An unexpected error occurred: {e}")
