from openai import OpenAI

from vision_models import normalize_strings


client = OpenAI()


def image_summary(labels, description, detected_text):
    prompt = (
        "Summarize these visual analysis results in one short sentence: "
        f"labels={normalize_strings(labels)}; description={description}; text={normalize_strings(detected_text)}"
    )
    resp = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    return resp.choices[0].message.content or ""
