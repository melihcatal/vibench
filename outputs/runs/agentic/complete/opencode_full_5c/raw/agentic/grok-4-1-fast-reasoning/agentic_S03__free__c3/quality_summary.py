import openai
import os


def quality_summary(source_text: str, translated_text: str) -> str:
    """
    Summarize translation quality issues using OpenAI GPT-4o-mini.
    """
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = f"""You are an expert translation quality assessor.
    
Source text: {source_text}
Translated text: {translated_text}

Provide a concise summary of any quality issues (e.g., accuracy, fluency, omissions). If the translation is high quality, state that clearly."""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        max_tokens=300,
    )
    return response.choices[0].message.content.strip()
