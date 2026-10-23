import os
from google.cloud import aiplatform

def incident_summary(error_logs: list[dict]) -> str:
    if not error_logs:
        return "No error logs provided for summarization."

    project_id = os.getenv("GCP_PROJECT_ID")
    region = os.getenv("GCP_REGION", "us-central1")

    if not project_id:
        return "Error: GCP_PROJECT_ID environment variable not set."

    aiplatform.init(project=project_id, location=region)

    # Use the Gemini Pro model
    model = aiplatform.GenerativeModel("gemini-pro")

    log_texts = "\n".join([str(log) for log in error_logs])

    prompt = f"""Summarize the following error logs for an incident review. Focus on identifying common patterns, root causes, affected services, and potential impact. Provide a concise summary. An example of the error logs are as follows: \n\n{log_texts}"""

    try:
        response = model.generate_content(prompt)
        summary = response.text
        print("Successfully generated incident summary using Google Cloud Vertex AI (Gemini Pro).")
        print("Summary:")
        print(summary)
        return summary
    except Exception as e:
        print(f"Error generating incident summary with Google Cloud Vertex AI: {e}")
        return f"Failed to generate incident summary due to an error: {e}"

# Example Usage (will not be part of the final file)
# if __name__ == "__main__":
#     sample_error_logs = [
# #         {"@timestamp": "2023-10-27T10:00:00Z", "severity": "ERROR", "service": "payment-service", "message": "Payment failed for order 123 due to insufficient funds"},
# #         {"@timestamp": "2023-10-27T10:01:00Z", "severity": "ERROR", "service": "payment-service", "message": "Failed to process transaction for user 456"},
# #         {"@timestamp": "2023-10-27T10:02:00Z", "severity": "ERROR", "service": "inventory-service", "message": "Out of stock for product XYZ during order 123"}
#     ]
#     # os.environ["GCP_PROJECT_ID"] = "your-gcp-project-id"
#     # os.environ["GCP_REGION"] = "us-central1"
#     # incident_summary(sample_error_logs)
