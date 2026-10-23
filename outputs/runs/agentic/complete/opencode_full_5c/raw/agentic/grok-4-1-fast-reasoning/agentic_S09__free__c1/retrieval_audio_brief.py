import os
from typing import List
from openai import OpenAI


def retrieval_audio_brief(retrieved_results: List[str], output_path: str):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    summary_prompt = (
        "Create a concise spoken brief summarizing these top search results:\\n\\n"
        + "\\n".join(retrieved_results[:3])
    )
    chat_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": summary_prompt}],
        max_tokens=150,
    )
    brief_text = chat_response.choices[0].message.content
    speech_response = client.audio.speech.create(
        model="tts-1", voice="alloy", input=brief_text
    )
    speech_response.stream_to_file(output_path)
