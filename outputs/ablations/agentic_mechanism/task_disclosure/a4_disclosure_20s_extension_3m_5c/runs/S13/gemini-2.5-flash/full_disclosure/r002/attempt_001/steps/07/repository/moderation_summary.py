import google.generativeai as genai
import os

def summarize_moderation_decisions(decisions: list[dict]) -> str:
    """
    Summarizes a list of moderation decisions using Google Generative AI.

    Args:
        decisions: A list of dictionaries, where each dictionary represents a
                   moderation decision. Each dictionary is expected to have
                   at least a 'content' field and a 'decision' field.

    Returns:
        A string containing the summary of the moderation decisions.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')

    decision_texts = []
    for i, decision in enumerate(decisions):
        decision_texts.append(
            f"Decision {i+1}: Content: '{decision.get("content", "N/A")}', "
            f"Decision: '{decision.get("decision", "N/A")}'"
        )

    prompt = (
        "Summarize the following moderation decisions. "
        "Highlight any trends or notable outcomes:

"
        + "\n".join(decision_texts) +
        "\n\nSummary:"
    )

    response = model.generate_content(prompt)
    return response.text
