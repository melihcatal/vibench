from openai import OpenAI
from observability_models import IncidentSummaryRequest

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_incident_summary(request: IncidentSummaryRequest) -> str:
    """Summarize error-log findings for incident review using OpenAI GPT-4."""
    log_text = "\n".join([entry["message"] for entry in request.log_entries])
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are an incident response assistant. Summarize the following error logs."
            },
            {
                "role": "user",
                "content": f"Error logs:\n{log_text}\n\nSummary:"
            }
        ],
        temperature=0.3,
        max_tokens=500
    )
    
    return response.choices[0].message.content.strip()