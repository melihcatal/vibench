import json
import os
from observability_client import ObservabilityClient
from observability_models import LogQueryResult

def summarize_error_logs(error_logs: LogQueryResult):
    client = ObservabilityClient()
    
    if not client.openai_client:
        print("Azure OpenAI client not initialized. Cannot summarize logs.")
        return ""

    if not error_logs.raw_data:
        return "No error logs to summarize."

    log_messages = [str(log) for log in error_logs.raw_data]
    
    prompt = f"""Summarize the following error logs for an incident review. Identify common patterns, critical issues, and potential root causes.
    
    Error logs:
    {json.dumps(log_messages, indent=2)}
    """
    
    try:
        response = client.openai_client.chat.completions.create(
            model=client.azure_openai_deployment_name,
            messages=[
                {"role": "system", "content": "You are an AI assistant that summarizes log data for incident response."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        summary = response.choices[0].message.content
        return summary
        
    except Exception as e:
        print(f"Error summarizing error logs with Azure OpenAI: {e}")
        return f"Failed to summarize logs due to error: {e}"