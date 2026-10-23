import openai
import os
from pathlib import Path
from typing import List

def generate_audio_brief(text_to_speak: str, output_filepath: str = "audio_brief.mp3") -> str:
    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    speech_file_path = Path(output_filepath)
    
    response = client.audio.speech.create(
        model="tts-1",  # Using the base TTS model
        voice="alloy",  # A standard voice
        input=text_to_speak
    )
    
    response.stream_to_file(speech_file_path)
    
    return str(speech_file_path)

def retrieval_audio_brief(retrieved_results: List[str], brief_title: str = "Search Results Brief") -> str:
    # Concatenate the retrieved results into a single string for the brief
    brief_content = f"Here is a brief of your {brief_title}.\n\n"
    for i, result in enumerate(retrieved_results):
        brief_content += f"Result {i+1}: {result}\n\n"
        
    output_filename = brief_title.replace(" ", "_").lower() + ".mp3"
    audio_file_path = generate_audio_brief(brief_content, output_filename)
    
    return audio_file_path
