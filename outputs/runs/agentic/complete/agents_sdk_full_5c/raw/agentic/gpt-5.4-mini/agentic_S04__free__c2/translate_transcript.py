from speech_client import get_client


def translate_transcript(text: str, target_language: str = "Spanish"):
    client = get_client()
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Translate transcript segments faithfully and preserve meaning."},
            {"role": "user", "content": f"Translate the following transcript to {target_language}:\n\n{text}"},
        ],
        temperature=0.2,
    )
    translated = completion.choices[0].message.content or ""
    return {"text": translated, "raw": completion.model_dump()}
