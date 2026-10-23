import os
import openai

def summarize_incident(error_logs_text: str) -> str:
    """
    Summarizes error log findings for incident review using OpenAI.

    Args:
        error_logs_text: A string containing a collection of error logs.

    Returns:
        A concise summary of the potential incident.
    """
    if not error_logs_text:
        return "No error logs provided to summarize."

    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    prompt = f"""
    The following is a collection of error logs from our system.
    Please analyze these logs and provide a brief, actionable summary for an incident review.
    Identify the potential root cause, affected services, and recommended next steps.

    Logs:
    ---
    {error_logs_text}
    ---
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert system reliability engineer."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.5,
            max_tokens=512,
        )
        summary = response.choices[0].message.content
        return summary.strip() if summary else "Could not generate a summary."
    except Exception as e:
        print(f"An error occurred with the OpenAI API: {e}")
        return "Failed to generate incident summary."

