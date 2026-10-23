import os
from typing import List, Dict, Any
from google.cloud import aiplatform

def summarize_error_logs(project_id: str, location: str, error_logs: List[Dict[str, Any]]) -> str:
    aiplatform.init(project=project_id, location=location)

    # Use a generative model (e.g., Gemini or text-bison)
    # For this example, we'll use a placeholder model name. 
    # In a real scenario, you'd specify a concrete model like 'gemini-pro' or 'text-bison@001'
    model = aiplatform.preview.language_models.TextGenerationModel.from_pretrained("gemini-pro")

    if not error_logs:
        return "No error logs provided for summarization."

    log_messages = [log.get('message', {}).get('event', str(log)) for log in error_logs]
    combined_logs_text = "\n".join([str(msg) for msg in log_messages])

    prompt = f"Summarize the following error log findings for an incident review. Focus on identifying patterns, root causes, and impact:\n\n{combined_logs_text}\n\nSummary:"

    response = model.predict(
        prompt,
        max_output_tokens=1024,  # Adjust as needed
        temperature=0.2,       # Adjust for creativity vs. factualness
    )

    return response.text

if __name__ == '__main__':
    PROJECT_ID = os.environ.get('GOOGLE_CLOUD_PROJECT')  # e.g., your-gcp-project-id
    LOCATION = os.environ.get('GOOGLE_CLOUD_REGION', 'us-central1') # e.g., us-central1

    if not PROJECT_ID:
        print("Please set the GOOGLE_CLOUD_PROJECT environment variable.")
    else:
        # Example error logs (in a real scenario, these would come from query_error_logs.py)
        example_error_logs = [
            {
                "timestamp": "2026-09-19T10:00:00Z",
                "message": {"level": "ERROR", "service": "user-service", "event": "Failed to connect to database", "details": {"db_host": "db-prod-1"}}
            },
            {
                "timestamp": "2026-09-19T10:01:00Z",
                "message": {"level": "ERROR", "service": "user-service", "event": "Database connection timed out", "details": {"db_host": "db-prod-1"}}
            },
            {
                "timestamp": "2026-09-19T10:05:00Z",
                "message": {"level": "ERROR", "service": "payment-service", "event": "Third-party payment gateway error", "details": {"gateway": "stripe"}}
            },
        ]

        summary = summarize_error_logs(PROJECT_ID, LOCATION, example_error_logs)
        print("\nIncident Summary:")
        print(summary)
