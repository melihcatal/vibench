# platform_brief_audio.py
"""Generate spoken briefings from platform outputs using Azure AI Speech TTS SDK.
The function receives generated text, an optional locale, and produces an audio file (WAV).
"""

import os
import json
from azure.cognitiveservices.speech import SpeechConfig, AudioConfig, SpeechSynthesizer
from model_models import ProviderInfo, ApiResponse


def synthesize(text: str, locale: str = "en-US", output_file: str = "output.wav") -> Dict[str, Any]:
    """Synthesize speech from text using Azure Speech TTS and return metadata."""
    # Ensure env vars AZURE_SPEECH_KEY and AZURE_SPEECH_REGION are set
    speech_config = SpeechConfig(subscription=os.getenv("AZURE_SPEECH_KEY"),
                                 region=os.getenv("AZURE_SPEECH_REGION"))
    speech_config.speech_synthesis_voice_name = f"{locale}-Female"
    audio_config = AudioConfig(filename=output_file)
    synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    result = synthesizer.speak_text_async(text).get()
    # Azure returns result.reason (e.g., Success) and synthesis details
    return {
        "status": result.reason.name if hasattr(result.reason, "name") else str(result.reason),
        "output_file": output_file,
        "metadata": provider_info.__dict__ if provider_info else {}
    }

if __name__ == "__main__":
    import argparse, json
    parser = argparse.ArgumentParser(description="Create audio brief from model output")
    parser.add_argument("text", help="Generated text to speak")
    parser.add_argument("--locale", default="en-US", help="Locale for voice (default en-US)")
    parser.add_argument("--out", default="output.wav", help="Output WAV file")
    args = parser.parse_args()
    print(json.dumps(synthesize(args.text, args.locale, args.out), indent=2))
