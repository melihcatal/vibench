import os
from anthropic import Anthropic

def embedding_job_summary(payload, config=None):
    config = config or {}
    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    job_results = payload["job_results"]
    summary_prompt = "Summarize the following embedding job results in a concise manner:\n\n"
    for result in job_results:
        summary_prompt += f"- Task: {result.get("task", "N/A")}, Status: {result.get("status", "N/A")}, Details: {result.get("details", "N/A")}\n"

    response = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=200,
        messages=[
            {"role": "user", "content": summary_prompt}
        ]
    )
    return {"summary": response.content[0].text}
