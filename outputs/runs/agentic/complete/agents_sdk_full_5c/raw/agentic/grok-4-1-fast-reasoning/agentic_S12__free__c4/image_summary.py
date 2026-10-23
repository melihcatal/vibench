from openai import OpenAI
from vision_client import OPENAI_API_KEY
from vision_models import Summary
from typing import Dict, Any

def image_summary(analysis_results: Dict[str, Any]) -> Summary:
    client = OpenAI(api_key=OPENAI_API_KEY)
    prompt = "Provide a concise summary of these image analysis results:\\n" + str(analysis_results)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
    )
    summary_text = response.choices[0].message.content.strip()
    return Summary(summary=summary_text)