import os
from mistralai import Mistral


def quality_summary(
    original: str, translated: str, source_lang: str, target_lang: str
) -> str:
    client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))
    response = client.chat(
        model="mistral-large-latest",
        messages=[
            {
                "role": "user",
                "content": f"Summarize translation quality issues between original ({source_lang}): '{original}' and translated ({target_lang}): '{translated}'. Focus on fluency, accuracy, omissions, unnatural phrasing. Output concise bullet points.",
            }
        ],
    )
    return response.choices[0].message.content
