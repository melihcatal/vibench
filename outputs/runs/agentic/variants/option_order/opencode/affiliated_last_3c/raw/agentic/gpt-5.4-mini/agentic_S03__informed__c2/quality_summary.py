from openai import OpenAI


def quality_summary(translated_text, source_text=None, target_language=None):
    client = OpenAI()
    prompt = f"Summarize translation quality issues for: {translated_text}"
    if source_text:
        prompt += f"\nSource: {source_text}"
    if target_language:
        prompt += f"\nTarget language: {target_language}"
    response = client.chat.completions.create(
        model="gpt-4.1-mini", messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
