import os
from openai import OpenAI

def quality_summary(original: str, translated: str, source_lang: str, target_lang: str) -> str:
    \"\"\"
    Summarize translation quality issues using OpenAI GPT-4o-mini.
    \"\"\"
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    if not client.api_key:
        raise ValueError('OPENAI_API_KEY environment variable is required.')
    prompt = f\"Analyze and summarize quality issues in this translation from {source_lang} to {target_lang}:\\nOriginal: {{original}}\\nTranslated: {{translated}}\\n\\nFocus on accuracy, fluency, and cultural appropriateness.\"
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{'role': 'user', 'content': prompt.format(original=original, translated=translated)}],
        temperature=0.1,
        max_tokens=300
    )
    return response.choices[0].message.content