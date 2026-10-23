from google.cloud import aiplatform
import os

def summarize_onboarding_state(onboarding_data: dict) -> str:
    """
    Summarizes the onboarding state for support using Google Vertex AI.
    """
    # Initialize Vertex AI client
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set or
    # authenticate using `gcloud auth application-default login`
    aiplatform.init(project=os.getenv("GOOGLE_CLOUD_PROJECT"), location=os.getenv("GOOGLE_CLOUD_REGION", "us-central1"))

    # Use a pre-trained text-bison model for summarization
    model = aiplatform.gapic.PredictionServiceClient.from_service_account_json(
        filename=os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    ).get_model(name="projects/google/locations/us-central1/models/text-bison")


    prompt = f"""
    Please summarize the following onboarding state for a support agent.
    Focus on key information such as user progress, any pending actions, and potential issues.

    Onboarding Data:
    {onboarding_data}

    Summary:
    """

    response = model.predict(instances=[{"prompt": prompt}])
    return response.predictions[0]['content']
