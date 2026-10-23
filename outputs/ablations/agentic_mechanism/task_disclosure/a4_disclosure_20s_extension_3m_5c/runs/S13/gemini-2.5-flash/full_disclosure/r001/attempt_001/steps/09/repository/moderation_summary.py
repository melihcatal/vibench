import google.generativeai as genai
import os

def summarize_moderation_decisions(decisions: list[dict]) -> str:
    """
    Summarizes a list of moderation decisions using Google Generative AI.

    Args:
        decisions: A list of dictionaries, where each dictionary represents a
                   moderation decision. Each dictionary is expected to have
                   at least a "text" field with the moderated content and
                   a "decision" field with the moderation outcome.
                   Example: [{"text": "...", "decision": "..."}]

    Returns:
        A string containing the summary of the moderation decisions.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')

    decision_texts = []
    for i, decision in enumerate(decisions):
        decision_texts.append(f"Decision {i+1}: Text: "{decision.get("text", "N/A")}", Outcome: {decision.get("decision", "N/A")}")

    prompt = "Summarize the following moderation decisions:\n" + "\n".join(decision_texts)
    
    response = model.generate_content(prompt)
    return response.text

