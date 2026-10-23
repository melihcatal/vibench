from google.cloud import aiplatform
from vertexai.preview.generative_models import GenerativeModel, Part, Image

def summarize_error_logs(error_logs: str) -> str:
    """
    Summarizes error logs for incident review using Google's Generative AI.

    Args:
        error_logs: A string containing the error logs.

    Returns:
        A summarized string of the error logs.
    """
    aiplatform.init(project="your-gcp-project-id", location="us-central1") # Replace with your GCP project ID
    model = GenerativeModel("gemini-pro")
    
    prompt = f"""
    Please summarize the following error logs concisely for an incident review.
    Highlight the most critical errors, their potential causes, and any recurring patterns.

    Error Logs:
    {error_logs}
    """

    response = model.generate_content(prompt)
    return response.text

if __name__ == "__main__":
    # Example Usage (replace with actual error log fetching)
    sample_error_logs = """
    ERROR: [2026-09-19 10:00:01] An authentication error occurred for user 'testuser'. IP: 192.168.1.10
    WARNING: [2026-09-19 10:00:05] Disk space is running low on /var/log. Free space: 10%
    ERROR: [2026-09-19 10:00:10] Database connection failed. Host: db.example.com, Port: 5432
    INFO: [2026-09-19 10:00:15] User 'admin' logged in successfully.
    ERROR: [2026-09-19 10:00:20] An authentication error occurred for user 'testuser'. IP: 192.168.1.11
    CRITICAL: [2026-09-19 10:00:25] System crashed due to out of memory error. Process: data_processor.py
    ERROR: [2026-09-19 10:00:30] Database connection failed. Host: db.example.com, Port: 5432
    """
    
    summary = summarize_error_logs(sample_error_logs)
    print("Incident Summary:")
    print(summary)
