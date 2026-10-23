import os
from google.cloud import aiplatform

def summarize_moderation_decisions(decisions: list[dict]) -> str:
    """
    Summarize moderation decisions using Google Cloud AI Platform's generative models.

    Args:
        decisions: A list of dictionaries, where each dictionary represents a moderation decision.
                   Each decision might contain 'text', 'is_allowed', 'reasons_for_denial', etc.

    Returns:
        A string summarizing the moderation outcomes.
    """
    project_id = os.environ.get("GCP_PROJECT_ID")
    location = os.environ.get("GCP_LOCATION", "us-central1")

    aiplatform.init(project=project_id, location=location)
    model = aiplatform.get_model("text-bison@001") # Using text-bison for summarization

    decision_strings = []
    for i, decision in enumerate(decisions):
        text = decision.get("text", "N/A")
        is_allowed = decision.get("is_allowed", False)
        reasons = "; ".join(decision.get("reasons_for_denial", ["No specific reason."])) if not is_allowed else "Allowed."
        decision_strings.append(f"Item {i+1}: Text: \"{text}\". Status: {'Allowed' if is_allowed else 'Denied'}. Reasons: {reasons}")

    prompt = """
    Summarize the following moderation decisions. Highlight any patterns in denials or approvals.

    Moderation Decisions:
    """ + "\n".join(decision_strings) + "\n\nSummary:"

    response = model.predict(instances=[{"prompt": prompt}])

    summary = "No summary generated." # Default if response is empty
    if response.predictions:
        # Accessing the generated text from the model's response
        # The exact field depends on the client library version and model response structure.
        # Common fields include `predictions[0]['content']` or `candidates[0].text`
        if isinstance(response.predictions[0], dict) and 'content' in response.predictions[0]:
            summary = response.predictions[0]['content']
        elif hasattr(response, 'candidates') and response.candidates:
            summary = response.candidates[0].text # For newer SDK versions/Gemini models
        else:
             summary = str(response.predictions[0]) # Fallback

    return summary

if __name__ == "__main__":
    mock_decisions = [
        {
            "text": "Hello, this is a safe message.",
            "is_allowed": True,
            "reasons_for_denial": []
        },
        {
            "text": "I will hurt you!",
            "is_allowed": False,
            "reasons_for_denial": ["Content scored 0.9 for HARM_CATEGORY_DANGEROUS", "High score for HARM_CATEGORY_TOXICITY"]
        },
        {
            "text": "Let's talk about puppies.",
            "is_allowed": True,
            "reasons_for_denial": []
        },
        {
            "text": "You are a terrible person!",
            "is_allowed": False,
            "reasons_for_denial": ["Content scored 0.75 for HARM_CATEGORY_HATE_SPEECH"]
        }
    ]

    summary = summarize_moderation_decisions(mock_decisions)
    print("\n--- Moderation Summary ---")
    print(summary)
