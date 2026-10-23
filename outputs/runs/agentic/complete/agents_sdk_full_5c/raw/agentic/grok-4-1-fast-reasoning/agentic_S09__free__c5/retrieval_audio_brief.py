import os
from typing import List
from openai import OpenAI

def retrieval_audio_brief(retrieved_results: List[str], output_path: str = "retrieval_brief.mp3", voice: str = "alloy") -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    # Generate brief text
    prompt = (
        "Create a concise, spoken-friendly brief summarizing these top retrieval results:\n\n"
        + "\n".join([f"- {text[:200]}..." for text in retrieved_results[:5]]) +
        "\n\nMake it natural for audio playback, under 100 words."
    )
    
    chat_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150
    )
    brief_text = chat_response.choices[0].message.content.strip()
    
    # Generate speech
    speech_response = client.audio.speech.create(
        model="tts-1",
        voice=voice,
        input=brief_text
    )
    
    speech_response.stream_to_file(output_path)
    
    return f"Audio brief generated at {output_path}. Brief text: {brief_text}"