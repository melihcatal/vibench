import os
from openai import OpenAI


def translate_script(text, target_language, source_language=None, model="gpt-5.4-mini"):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    prompt = [
        {"role": "system", "content": "You translate narration scripts accurately and preserve meaning, tone, formatting, names, numbers, and SSML-like tags if present. Output only the translated text."},
        {"role": "user", "content": f"Translate the following narration script to {target_language}." + (f" Source language: {source_language}." if source_language else "") + f"\n\n{text}"},
    ]
    response = client.chat.completions.create(model=model, messages=prompt)
    return response.choices[0].message.content


def translate_script_response(text, target_language, source_language=None, model="gpt-5.4-mini"):
    translated = translate_script(text, target_language, source_language=source_language, model=model)
    return {"translated_text": translated, "target_language": target_language, "source_language": source_language, "model": model}
