from openai import OpenAI
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)


def summarize_audit_events(audit_records):
    prompt = (
        "Summarize the following federated login audit events into a concise report:\n"
        f"{audit_records}\n\n"
        "Include key metrics like total logins, unique users, and any anomalies."
    )
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content.strip()