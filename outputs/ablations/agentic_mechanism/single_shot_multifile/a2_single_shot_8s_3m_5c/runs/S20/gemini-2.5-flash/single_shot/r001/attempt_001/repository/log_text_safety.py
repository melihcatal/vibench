import os
from google.cloud import aiplatform
from vertexai.preview.generative_models import GenerativeModel, Part

from observability_client import get_generative_model
from observability_models import SafetyCheckResult

# aiplatform.init(project=os.environ.get("GCP_PROJECT_ID"), location=os.environ.get("GCP_REGION", "us-central1"))

def check_log_message_safety(message_text: str) -> list[SafetyCheckResult]:
    model = get_generative_model(model_name="gemini-pro") # Using Gemini-Pro model

    # For content safety, we typically rely on the built-in safety attributes
    # of generative models like Gemini, rather than a separate API call.
    # The generate_content method will return safety attributes in its response.

    response = model.generate_content(
        [f"Analyze the following log message for any unsafe content (e.g., hate speech, harassment, sexual content, dangerous content). Just respond with 'OK' if safe, otherwise describe the unsafe aspect. Log: {message_text}"],
        safety_settings={
            aiplatform.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: aiplatform.HarmBlockThreshold.BLOCK_ONLY_HIGH,
            aiplatform.HarmCategory.HARM_CATEGORY_HARASSMENT: aiplatform.HarmBlockThreshold.BLOCK_ONLY_HIGH,
            aiplatform.HarmCategory.HARM_CATEGORY_HATE_SPEECH: aiplatform.HarmBlockThreshold.BLOCK_ONLY_HIGH,
            aiplatform.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: aiplatform.HarmBlockThreshold.BLOCK_ONLY_HIGH,
        }
    )

    safety_results = []
    for rating in response.candidates[0].safety_ratings:
        safety_results.append(
            SafetyCheckResult(
                score=rating.probability_score, # numerical score for probability
                category=rating.category.name, # e.g., HARM_CATEGORY_HATE_SPEECH
                blocked=rating.blocked, # True if blocked by the threshold
                details={ "probability": rating.probability.name } # e.g., NEGLIGIBLE, LOW, MEDIUM, HIGH
            )
        )
    return safety_results

