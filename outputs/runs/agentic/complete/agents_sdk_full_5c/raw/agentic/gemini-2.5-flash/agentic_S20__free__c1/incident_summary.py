import os
from typing import List, Dict, Any
import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part, Image

def summarize_error_logs_for_incident(error_logs: List[Dict[str, Any]], project_id: str, location: str = "us-central1") -> str:
    """Summarizes error log findings for incident review using Vertex AI Generative Model."""
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel("gemini-pro") # Using Gemini Pro for summarization

    if not error_logs:
        return "No error logs provided for summarization."

    # Concatenate relevant parts of error logs into a single string for summarization
    log_texts = []
    for log in error_logs:
        # Prioritize textPayload or jsonPayload.message, otherwise take the entire entry as string
        if "textPayload" in log:
            log_texts.append(log["textPayload"])
        elif "jsonPayload" in log and "message" in log["jsonPayload"]:
            log_texts.append(log["jsonPayload"]["message"])
        else:
            log_texts.append(str(log))

    # Join a reasonable number of log entries to avoid excessively long prompts
    # For very large sets, consider chunking or more sophisticated aggregation before summarization
    concatenated_logs = "\n".join(log_texts[:50]) # Summarize up to 50 recent error log messages

    prompt = f"""Summarize the following error logs to provide a concise overview for an incident review. 
Identify key issues, common patterns, and potential root causes if evident. 

Error Logs:
{concatenated_logs}

Summary:"""
    
    print(f"Sending prompt to Vertex AI for summarization (first 50 logs)..")
    response = model.generate_content(prompt)

    if response.candidates and response.candidates[0].content.parts:
        return response.candidates[0].content.parts[0].text
    else:
        return "Failed to generate a summary for the provided error logs."

if __name__ == '__main__':
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        print("GOOGLE_CLOUD_PROJECT environment variable not set.")
        exit(1)

    # Example usage with dummy error logs
    sample_error_logs = [
        {"severity": "ERROR", "timestamp": "2023-10-27T10:00:00Z", "jsonPayload": {"message": "Database connection failed", "service": "backend-api"}},
        {"severity": "ERROR", "timestamp": "2023-10-27T10:01:00Z", "textPayload": "NullPointerException in user service"},
        {"severity": "ERROR", "timestamp": "2023-10-27T10:02:00Z", "jsonPayload": {"message": "Failed to write to cache", "cache_key": "user_session_123"}},
        {"severity": "WARNING", "timestamp": "2023-10-27T10:03:00Z", "textPayload": "High latency detected in auth service", "severity": "ERROR"}, # Example of inconsistent severity
        {"severity": "ERROR", "timestamp": "2023-10-27T10:04:00Z", "jsonPayload": {"message": "Database connection failed", "service": "backend-api"}},
    ]

    summary = summarize_error_logs_for_incident(sample_error_logs, project_id)
    print("\n--- Incident Summary ---")
    print(summary)
