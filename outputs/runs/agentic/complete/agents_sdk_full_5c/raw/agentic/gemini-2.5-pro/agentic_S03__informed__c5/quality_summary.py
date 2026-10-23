import os
from openai import OpenAI

def summarize_quality_issues(source_text: str, translated_text: str, source_lang: str, target_lang: str) -> str:
    """
    Uses an OpenAI model to summarize potential quality issues in a translation.
    
    Expects OPENAI_API_KEY environment variable to be set.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    prompt = f"""
    You are a translation quality expert. Analyze the following translation from {source_lang} to {target_lang}.
    Identify any potential issues such as mistranslation, grammatical errors, awkward phrasing, or loss of nuance.
    Provide a brief summary of the translation's quality. If there are no issues, state that the quality is high.

    Source Text ({source_lang}):
    {source_text}

    Translated Text ({target_lang}):
    {translated_text}

    Quality Summary:
    """
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful translation quality analyst."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=500
    )
    
    summary = response.choices[0].message.content
    return summary.strip() if summary else "Could not generate summary."
