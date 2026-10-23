from openai import OpenAI


def quality_summary(segments: list[str], source_language: str, target_language: str) -> str:
    client = OpenAI()
    response = client.responses.create(model="gpt-4.1-mini", input=f"Summarize translation quality issues for {source_language} to {target_language}: {segments}")
    return response.output_text if hasattr(response, "output_text") else ""
