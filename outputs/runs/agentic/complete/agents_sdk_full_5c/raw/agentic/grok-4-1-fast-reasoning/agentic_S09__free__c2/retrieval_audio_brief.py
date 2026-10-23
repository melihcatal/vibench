from typing import List, Dict, Any
from embeddings_client import get_embeddings_client

SUMMARY_MODEL = "gpt-4o-mini"
TTS_MODEL = "tts-1"
TTS_VOICE = "alloy"

def retrieval_audio_brief(results: List[Dict[str, Any]], output_file: str = "brief.mp3") -> str:
    client = get_embeddings_client()
    context = "\n---\n".join([f"{r.get('title', 'Result')}: {r.get('text', '')[:250]} (score: {r.get('score', 'N/A')})" for r in results[:4]])
    summary_prompt = f"Create a concise audio brief (under 90 seconds when spoken) summarizing these search results:\n\n{context}"
    summary_resp = client.chat.completions.create(
        model=SUMMARY_MODEL,
        messages=[{"role": "user", "content": summary_prompt}],
        max_tokens=200,
        temperature=0.5
    )
    brief_text = summary_resp.choices[0].message.content.strip()
    speech_resp = client.audio.speech.create(
        model=TTS_MODEL,
        voice=TTS_VOICE,
        input=brief_text
    )
    speech_resp.stream_to_file(output_file)
    return output_file