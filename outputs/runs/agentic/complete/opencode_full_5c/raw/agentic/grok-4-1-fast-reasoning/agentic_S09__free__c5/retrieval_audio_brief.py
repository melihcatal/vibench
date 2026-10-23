from typing import List, Dict, Any
from embeddings_client import get_client


def generate_audio_brief(retrieved_results: List[Dict[str, Any]]) -> bytes:
    client = get_client()
    top_texts = [r.get("text", str(r))[:300] for r in retrieved_results[:3]]
    prompt = f"""Write a short spoken brief (20-30 seconds when read) summarizing these top retrieval results:

{"; ".join(top_texts)}"""
    chat_resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150,
    )
    brief_text = chat_resp.choices[0].message.content.strip()
    speech_resp = client.audio.speech.create(
        model="tts-1", voice="alloy", input=brief_text
    )
    return speech_resp.content
