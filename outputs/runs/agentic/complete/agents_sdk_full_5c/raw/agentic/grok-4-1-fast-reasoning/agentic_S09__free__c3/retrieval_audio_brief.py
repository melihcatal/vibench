import os
from typing import List
from openai import OpenAI

def retrieval_audio_brief(retrieved_texts: List[str]) -> bytes:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY required")
    client = OpenAI(api_key=api_key)
    context = "\n---\n".join(retrieved_texts[:8])
    summary_prompt = f"""Create a short spoken brief (100-150 words) from these search results:
{context}"""
    chat_resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": summary_prompt}],
        max_tokens=150,
        temperature=0.5
    )
    brief_text = chat_resp.choices[0].message.content.strip()
    speech_resp = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=brief_text
    )
    return speech_resp.content