import os
from google.cloud import aiplatform

def summarize_message_results(results: str) -> str:
    """
    Summarizes message processing results using Google Cloud's Generative AI.
    """
    # Initialize Vertex AI
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # or authenticate otherwise.
    aiplatform.init(project=os.getenv("GCP_PROJECT_ID"), location="us-central1")

    # Load the model
    model = aiplatform.preview.generative_models.GenerativeModel("gemini-pro")

    # Generate content
    response = model.generate_content(
        f"Summarize the following message processing results: {results}"
    )

    return response.text

if __name__ == "__main__":
    example_results = """
    Message ID: msg_123, Status: SUCCESS, Processed by: ServiceA, Duration: 150ms
    Message ID: msg_124, Status: FAILED, Error: Timeout, Processed by: ServiceB, Duration: 5000ms
    Message ID: msg_125, Status: SUCCESS, Processed by: ServiceA, Duration: 200ms
    Message ID: msg_126, Status: FAILED, Error: Invalid Payload, Processed by: ServiceC, Duration: 80ms
    """
    summary = summarize_message_results(example_results)
    print("Summary of message processing results:")
    print(summary)
