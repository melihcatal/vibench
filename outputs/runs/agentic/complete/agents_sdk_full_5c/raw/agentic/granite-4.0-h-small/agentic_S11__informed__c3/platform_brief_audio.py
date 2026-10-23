# platform_brief_audio.py
# Later-step scored file: Generate spoken briefings from platform outputs (Azure Speech Text-to-Speech)

import os
from azure.cognitiveservices.speech import AudioDataStream, SpeechConfig, SpeechSynthesizer
from azure.cognitiveservices.speech import SpeechSynthesisOutputFormat

# Provider configuration (Azure)
AZURE_SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
AZURE_SPEECH_REGION = os.getenv("AZURE_SPEECH_REGION", "eastus")

if not AZURE_SPEECH_KEY:
    raise RuntimeError("AZURE_SPEECH_KEY environment variable not set.")

# Initialize SpeechConfig with your Azure subscription key and region
speech_config = SpeechConfig(subscription=AZURE_SPEECH_KEY, region=AZURE_SPEECH_REGION)
# Choose output format (e.g., MP3 for compact audio, or OGG_OPUS for streaming)
speech_config.set_speech_synthesis_output_format(SpeechSynthesisOutputFormat.OGG_OPUS)

# Create a synthesizer using the configured speech config
synthesizer = SpeechSynthesizer(speech_config=speech_config)


def synthesize_brief(text: str, output_file: str = "brief.mp3") -> str:
    """
    Synthesize spoken audio from the supplied plain‑text briefing.

    Args:
        text (str): The briefing text to speak.
        output_file (str): Destination file path for the generated audio.

    Returns:
        str: Path to the generated audio file.
    """
    # Create an audio stream from a file to store the result
    result_stream = AudioDataStream(filename=output_file)
    # Perform synthesis asynchronously
    future = synthesizer.speak_text_async(text)
    result = future.result()
    if result.reason == result.reason_synthesis_canceled:
        raise RuntimeError("Speech synthesis was canceled.")
    elif result.reason == result.reason_synthesis_failed:
        raise RuntimeError(f"Speech synthesis failed: {result.error_details}")
    # Return the path to the generated file
    return output_file

# Example usage (uncomment to test)
#if __name__ == "__main__":
#    briefing = "Welcome to the daily news briefing. Today we discuss advancements in AI safety."
#    audio_path = synthesize_brief(briefing, output_file="brief.mp3")
#    print(f"Audio briefing written to {audio_path}")
