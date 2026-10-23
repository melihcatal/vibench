from typing import Optional
from azure.cognitiveservices.speech import ResultOutcome, SpeechSynthesizer
from speech_client import get_synthesizer

def save_audio(text: str, filename: str, voice: Optional[str] = None, use_ssml: bool = False) -> None:
    """
    Synthesize and save audio to WAV file using Azure AI Speech TTS save_to_wav_file.
    """
    synthesizer: SpeechSynthesizer = get_synthesizer(voice)
    if use_ssml:
        result = synthesizer.speak_ssml_async(text).get()
    else:
        result = synthesizer.speak_text_async(text).get()
    if result.reason == ResultOutcome.Succeeded:
        synthesizer.save_to_wav_file(result, filename)
    else:
        raise ValueError(f"TTS failed: {result.reason} - {result.description}")
