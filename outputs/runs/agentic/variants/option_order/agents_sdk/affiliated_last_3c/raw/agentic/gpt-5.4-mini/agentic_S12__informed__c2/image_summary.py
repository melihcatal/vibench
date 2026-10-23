from __future__ import annotations

from openai import OpenAI

from vision_models import safe_text_summary


client = OpenAI()


def summarize_image_analysis(labels, description, text_results):
    model = "gpt-4o-mini"
    prompt = (
        "Summarize these image analysis results in one concise sentence: "
        f"labels={safe_text_summary(str(labels))}; "
        f"description={safe_text_summary(str(description))}; "
        f"text={safe_text_summary(str(text_results))}."
    )
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You summarize visual analysis results briefly."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )
    return completion.choices[0].message.content.strip()
