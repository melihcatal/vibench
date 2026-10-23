import pydub
import azure.cognitiveservices.speech as speechsdk
import os

# Azure AI Speech (TTS) setup
# Set environment variables:
# AZURE_SPEECH_KEY, AZURE_SPEECH_REGION


def generate_spoken_brief(text: str, voice_name: str = "en-US-JennyNeural") -> bytes:
    """Convert generated model output to spoken audio using Azure TTS."""
    speech_config = speechsdk.SpeechConfig(
        subscription=os.environ["AZURE_SPEECH_KEY"],
        region=os.environ["AZURE_SPEECH_REGION"],
    )
    speech_config.speech_synthesis_voice_name = voice_name
    audio_config = speechsdk.audio.AudioOutputConfig()
    synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=audio_config
    )
    result = synthesizer.speak_text_async(text).get()
    # result.audio_data contains raw PCM bytes
    return (
        result.audio_data
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted
        else b""
    )


# Example - saving to a WAV file (uncomment to test)
# if __name__ == "__main__":
#     brief = "This is a short spoken brief."
#     wav_bytes = generate_spoken_brief(brief)
#     with open("output.wav", "wb") as f:
#         f.write(wav_bytes)
