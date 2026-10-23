import os
from openai import OpenAI

SAMPLE_ERROR_LOGS = [
    "ERROR: Database connection timed out after 30s",
    "FATAL: Memory leak detected in module X",
    "WARN: High latency in API call to external service"
]

def generate_incident_summary():
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    logs_str = "\n".join(SAMPLE_ERROR_LOGS)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.1,
        messages=[
            {"role": "system", "content": "You are a DevOps engineer summarizing incidents from logs."},
            {"role": "user", "content": f"Please provide a concise summary of the incident based on these error logs:\n{logs_str}"}
        ]
    )
    summary = response.choices[0].message.content
    print(summary)
    return summary

if __name__ == "__main__":
    generate_incident_summary()