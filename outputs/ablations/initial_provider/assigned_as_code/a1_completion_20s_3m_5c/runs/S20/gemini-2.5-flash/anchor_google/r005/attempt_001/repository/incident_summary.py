from google.cloud import aiplatform
import os

def incident_summary(project_id: str, location: str, error_logs: list[dict]) -> str:
    # Initialize the AI Platform client
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set or gcloud is authenticated
    aiplatform.init(project=project_id, location=location)

    # Use the Gemini Pro model for text generation
    model_name = "gemini-pro"
    model = aiplatform.preview.generative_models.GenerativeModel(model_name)

    # Concatenate error logs into a single string for summarization
    log_texts = []
    for log in error_logs:
        if log.get("json_payload") and log["json_payload"].get("message"):
            log_texts.append(log["json_payload"]["message"])
        elif log.get("text_payload"):
            log_texts.append(log["text_payload"])
    
    if not log_texts:
        return "No error logs provided for summarization."

    combined_logs = "\n".join(log_texts)

    prompt = f"Summarize the following error logs for an incident review, highlighting key issues and potential impact:\n\n{combined_logs}\n\nSummary:"

    response = model.generate_content(prompt)
    return response.text
