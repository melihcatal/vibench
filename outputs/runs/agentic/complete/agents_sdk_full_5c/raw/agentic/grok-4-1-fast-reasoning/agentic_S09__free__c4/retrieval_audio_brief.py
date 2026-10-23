from embeddings_client import get_client
from typing import List, Dict, Any

def retrieval_audio_brief(retrieved_results: List[Dict[str, Any]], output_path: str):
    client = get_client()
    docs_text = "\\n".join([result.get("text", result.get("doc", str(result)))[:300] for result in retrieved_results])
    brief_prompt = f"Generate a short spoken brief (max 150 words) summarizing these top search results:\\n{docs_text}"
    brief_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": brief_prompt}],
        max_tokens=150
    )
    brief_text = brief_response.choices[0].message.content
    speech_response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=brief_text
    )
    speech_response.stream_to_file(output_path)