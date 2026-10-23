import vertexai
from vertexai.preview.generative_models import GenerativeModel
from safety_models import ModerationDecision, ModerationResult

def summarize_moderation_decisions(decisions: list[ModerationDecision], moderation_results: list[ModerationResult], project_id: str, location: str = "us-central1") -> str:
    """Summarize moderation decisions using Google Cloud Generative AI."""
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel("gemini-1.5-flash-001") # Using a specific Google Cloud Generative Model

    summary_prompt = "Summarize the following moderation decisions and results:

"
    for i, decision in enumerate(decisions):
        summary_prompt += f"Decision {i+1}: Allow={decision.allow}, Reason={decision.reason}
"
    for i, result in enumerate(moderation_results):
        summary_prompt += f"Result {i+1}: Text='{result.text}', Scores={result.scores}
"

    response = model.generate_content(summary_prompt)
    return response.text
