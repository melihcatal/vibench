import os
from openai import OpenAI
from query_error_logs import query_for_recent_errors

def summarize_errors_for_incident():
    """
    Fetches recent error logs and uses OpenAI to generate a summary
    for an incident report.
    """
    print("Fetching recent error logs for summary...")
    error_entries = query_for_recent_errors()

    if not error_entries:
        print("No errors to summarize.")
        return

    # Format the log entries for the prompt
    log_texts = []
    for entry in error_entries:
        payload = entry.payload
        message = payload.get('message', 'No message') if isinstance(payload, dict) else str(payload)
        log_texts.append(f"[{entry.timestamp}] {message}")
    
    log_blob = "\n".join(log_texts)

    if not log_blob.strip():
        print("Log content is empty, cannot generate summary.")
        return

    try:
        # Initialize OpenAI client
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

        prompt = f"""
        The following are recent error logs from our production system.
        Please provide a concise summary for an incident report.
        Focus on identifying potential patterns, unique error messages,
        and the timeline of events.

        Logs:
        ---
        {log_blob}
        ---

        Incident Summary:
        """

        print("\nGenerating summary with OpenAI...")
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes technical logs for incident management."},
                {"role": "user", "content": prompt}
            ]
        )

        summary = response.choices[0].message.content
        print("\n--- Incident Summary ---")
        print(summary)
        print("------------------------")
        return summary

    except Exception as e:
        print(f"An error occurred while generating the incident summary: {e}")
        return None

if __name__ == '__main__':
    summarize_errors_for_incident()
