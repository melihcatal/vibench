import os
from observability_client import observability_client

def incident_summary(error_logs: list[dict]) -> str:
    if not error_logs:
        return "No error logs provided for summary."

    # Format error logs into a readable string for the LLM
    formatted_logs = "\n".join([
        f"Time: {log.get('TimeGenerated', 'N/A')}, Message: {log.get('Message', 'N/A')}, Details: {log.get('CustomDimensions', 'N/A')}"
        for log in error_logs
    ])

    prompt = f"""
    Review the following error logs and provide a concise summary suitable for an incident review meeting. 
    Highlight the key issues, potential impact, and any recurring patterns. Limit the summary to 200 words.

    Error Logs:
    {formatted_logs}
    """

    try:
        response = observability_client.azure_openai_client.chat.completions.create(
            model=os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-35-turbo"), # Example model
            messages=[
                {"role": "system", "content": "You are an incident response assistant. Summarize error logs concisely."},
                {"role": "user", "content": prompt}
            ]
        )
        summary = response.choices[0].message.content
        print("Incident Summary:\n" + summary)
        return summary

    except Exception as e:
        print(f"Error generating incident summary: {e}")
        return f"Failed to generate summary due to an error: {e}"

# Example usage (for testing purposes)
# if __name__ == "__main__":
#     sample_error_logs = [
#         {"TimeGenerated": "2023-10-27T10:00:00Z", "Message": "Database connection failed", "CustomDimensions": {"errorCode": "DB001"}},
#         {"TimeGenerated": "2023-10-27T10:01:30Z", "Message": "Service X unavailable", "CustomDimensions": {"serviceName": "ServiceX"}},
#         {"TimeGenerated": "2023-10-27T10:02:15Z", "Message": "Database connection failed", "CustomDimensions": {"errorCode": "DB001"}}
#     ]
#     incident_summary(sample_error_logs)
