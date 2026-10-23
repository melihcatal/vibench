import os
from google.cloud import aiplatform

def check_log_text_safety(log_message: str) -> dict:
    project_id = os.getenv("GCP_PROJECT_ID")
    region = os.getenv("GCP_REGION", "us-central1")

    if not project_id:
        return {"error": "GCP_PROJECT_ID environment variable not set."}

    aiplatform.init(project=project_id, location=region)

    model = aiplatform.GenerativeModel("gemini-pro")

    prompt = f"""Analyze the following log message for any unsafe content, such as personally identifiable information (PII), sensitive data, or inappropriate language. Return a brief assessment and flag any identified issues. \n\nLog Message: {log_message}"""

    try:
        response = model.generate_content(prompt)
        safety_assessment = response.text
        print("Successfully performed safety check on log message using Google Cloud Vertex AI (Gemini Pro).")
        print("Safety Assessment:")
        print(safety_assessment)
        return {"assessment": safety_assessment}
    except Exception as e:
        print(f"Error checking log text safety with Google Cloud Vertex AI: {e}")
        return {"error": f"Failed to check log text safety due to an error: {e}"}

# Example Usage (will not be part of the final file)
# if __name__ == "__main__":
#     # os.environ["GCP_PROJECT_ID"] = "your-gcp-project-id"
#     # os.environ["GCP_REGION"] = "us-central1"
#     check_log_text_safety("User 'john.doe@example.com' tried to access /admin with password 'MySecurePass123!'")
#     check_log_text_safety("Successfully processed payment for order 789.")
