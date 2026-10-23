import os
from google.cloud import aiplatform

def onboarding_summary(onboarding_state_text: str) -> dict:
    # Initialize Vertex AI SDK
    aiplatform.init(
        project=os.environ.get("GCP_PROJECT_ID"),
        location=os.environ.get("GCP_REGION", "us-central1")
    )

    # Specify the model to use
    # For text generation, using a model like 'gemini-pro' or 'text-bison'
    # Ensure the model is available in your specified region
    model_name = "gemini-pro"
    model = aiplatform.preview.language_models.ChatModel.from_pretrained(model_name)

    # Define the prompt for summarization
    prompt = f"Summarize the following onboarding state for a support agent, highlighting key progress and any potential issues:\n\n{onboarding_state_text}\n\nSummary:"

    response = model.predict(
        prompt
    )

    summary = response.text

    return {
        "onboarding_state_text": onboarding_state_text,
        "onboarding_summary": summary,
        "model_used": model_name
    }
