import openai
import os

client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def summarize_error_log_findings(error_logs: list[dict]):
    log_texts = [log.get('msg', log.get('message', '')) for log in error_logs]
    context = '\\n\\n'.join(log_texts)
    prompt = f"""Summarize the key findings from these recent error logs for incident review:

{context}

Provide a concise summary, possible root cause, and affected services."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300
    )
    return response.choices[0].message.content.strip()
