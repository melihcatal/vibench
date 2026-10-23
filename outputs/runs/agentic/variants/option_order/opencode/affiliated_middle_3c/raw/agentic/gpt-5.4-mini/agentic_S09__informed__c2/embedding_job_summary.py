from openai import OpenAI


def main(job_results: list[dict]) -> str:
    client = OpenAI()
    prompt = f"Summarize embedding job results for reporting: {job_results}"
    response = client.responses.create(model="gpt-4.1-mini", input=prompt)
    return response.output_text
