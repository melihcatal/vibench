from google.cloud import aiplatform
import os
from observability_client import get_aiplatform_text_client

def summarize_incident_logs(incident_logs_text: str, model_name: str = "gemini-pro") -> str:
    """
    Summarizes error-log findings for incident review using Google Cloud AI Platform.
    """
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    # Initialize AI Platform client (this sets project and location globally for subsequent calls)
    get_aiplatform_text_client(project_id=project_id)

    # Load the text generation model
    model = aiplatform.GenerativeModel(model_name=model_name)

    prompt = f"""Review the following error logs and provide a concise summary suitable for an incident report. Highlight key errors, potential causes, affected components, and any observable patterns.

    Error Logs:
    '''
    {incident_logs_text}
    '''

    Summary:"""

    try:
        response = model.generate_content(prompt)
        if response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
            summary = "".join([part.text for part in response.candidates[0].content.parts])
            print(f"Generated incident summary using {model_name} from Google Cloud AI Platform.")
            return summary
        else:
            return "Failed to generate summary: No content found in response."
    except Exception as e:
        return f"Error generating summary: {e}"

if __name__ == "__main__":
    # Example usage (requires GOOGLE_CLOUD_PROJECT env var and auth)
    # export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
    sample_error_logs = '''
    [2023-10-26 10:01:23] ERROR: User service unavailable. Failed to fetch user profile for ID 12345.
    [2023-10-26 10:01:25] ERROR: Database connection lost. Retrying in 5 seconds.
    [2023-10-26 10:01:30] ERROR: Database connection lost. Retrying in 5 seconds.
    [2023-10-26 10:01:35] ERROR: Payment gateway timeout for transaction ABC. User ID 12345.
    [2023-10-26 10:01:40] WARNING: High latency detected in API gateway for /api/v1/user.
    [2023-10-26 10:01:42] ERROR: User service unavailable. Failed to fetch user profile for ID 54321.
    '''
    summary = summarize_incident_logs(sample_error_logs)
    print("\n--- Incident Summary ---")
    print(summary)
