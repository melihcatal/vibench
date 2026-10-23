from google.cloud import aiplatform


def summarize_error_logs(
    error_texts: list[str], project: str, location: str = "us-central1"
) -> str:
    """
    Summarizes a list of error log messages for incident review using Vertex AI.
    """
    aiplatform.init(project=project, location=location)

    # Using the Gemini model for summarization
    model = aiplatform.gapic.PredictionServiceClient(
        client_options={"api_endpoint": f"{location}-aiplatform.googleapis.com"}
    ).model("gemini-1.0-pro-001")

    prompt = f"""
    Summarize the following error log messages for a technical incident report.
    Identify common themes, root causes, and potential impact.
    
    Error Logs:
    ---
    {" ".join(error_texts)}
    ---
    
    Summary:
    """

    instances = [{"prompt": prompt}]

    response = model.predict(instances=instances, parameters={"max_output_tokens": 256})

    return response.predictions[0].get("content")


if __name__ == "__main__":
    import os

    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if project_id:
        errors = [
            "AuthError: User token expired for user_id: 123",
            "DatabaseConnectionError: Failed to connect to primary DB.",
            "AuthError: Invalid API key provided for service call.",
            "TimeoutError: Upstream service 'payment-processor' failed to respond.",
            "AuthError: User token expired for user_id: 456",
        ]
        summary = summarize_error_logs(errors, project=project_id)
        print("Incident Summary:")
        print(summary)
    else:
        print("GOOGLE_CLOUD_PROJECT environment variable not set.")
