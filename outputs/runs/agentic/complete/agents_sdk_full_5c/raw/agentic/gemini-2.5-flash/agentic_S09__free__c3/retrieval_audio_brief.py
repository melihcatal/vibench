import openai
from embeddings_client import get_openai_client
from pathlib import Path
from typing import List

def generate_audio_brief(text_brief: str, output_filepath: str = "retrieval_brief.mp3", voice: str = "alloy") -> Path:
    """Generates a spoken audio brief from text using OpenAI's Text-to-speech API.

    Args:
        text_brief: The text content of the brief to convert to speech.
        output_filepath: The path to save the generated audio file (e.g., "brief.mp3").
        voice: The voice to use for the audio. Options include "alloy", "shimmer", etc.

    Returns:
        A Path object pointing to the saved audio file.
    """
    client = get_openai_client()

    speech_file_path = Path(output_filepath)
    response = client.audio.speech.create(
        model="tts-1", # OpenAI's TTS model
        voice=voice,
        input=text_brief
    )

    response.stream_to_file(speech_file_path)

    return speech_file_path

def create_brief_from_results(results: List[str], output_filepath: str = "retrieval_brief.mp3", voice: str = "alloy") -> Path:
    """Combines search results into a brief text and then generates an audio brief.

    Args:
        results: A list of strings, where each string is a retrieved search result or summary.
        output_filepath: The path to save the generated audio file.
        voice: The voice to use for the audio.

    Returns:
        A Path object pointing to the saved audio file.
    """
    if not results:
        text_brief = "No results were found to generate a brief."
    else:
        text_brief = "Here is a brief summary of the retrieved information: "
        for i, res in enumerate(results):
            text_brief += f"Result {i+1}: {res}. "

    return generate_audio_brief(text_brief, output_filepath, voice)

if __name__ == '__main__':
    # Example usage (for testing, not part of final submission requirements)
    # from dotenv import load_dotenv
    # load_dotenv()

    # sample_results = [
    #     "Python is known for its readability and versatility.",
    #     "It is widely used in web development, data science, and AI."
    # ]
    # audio_file = create_brief_from_results(sample_results, "python_brief.mp3")
    # print(f"Audio brief saved to: {audio_file}")

    # single_text_brief = "The project achieved all milestones ahead of schedule."
    # audio_file_single = generate_audio_brief(single_text_brief, "project_status.mp3", voice="shimmer")
    # print(f"Single text audio brief saved to: {audio_file_single}")
    pass
