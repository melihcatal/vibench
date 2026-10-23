from openai import OpenAI


def summarize(log_findings: str) -> str:
    client = OpenAI()
    response = client.responses.create(model="gpt-5.4-mini", input=[{"role": "system", "content": "Summarize these incident findings for review."}, {"role": "user", "content": log_findings}])
    return response.output_text
