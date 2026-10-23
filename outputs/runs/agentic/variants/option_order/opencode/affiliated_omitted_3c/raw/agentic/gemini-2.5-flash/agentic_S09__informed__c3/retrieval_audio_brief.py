import os
import azure.cognitiveservices.speech as speechsdk


def generate_spoken_brief(text: str, output_filepath: str = "brief.mp3") -> str:
    speech_key = os.environ.get("AZURE_SPEECH_KEY")
    service_region = os.environ.get("AZURE_SPEECH_REGION")

    if not speech_key or not service_region:
        raise ValueError("AZURE_SPEECH_KEY and AZURE_SPEECH_REGION must be set.")

    # Azure AI Speech TTS specific configuration
    speech_config = speechsdk.SpeechConfig(
        subscription=speech_key, region=service_region
    )
    speech_config.speech_synthesis_voice_name = "en-US-JennyNeural"  # Example voice

    audio_config = speechsdk.audio.AudioOutputConfig(filename=output_filepath)

    speech_synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=audio_config
    )

    result = speech_synthesizer.speak_text_async(text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        return f"Audio brief successfully generated and saved to {output_filepath}"
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        return f"Speech synthesis canceled: {cancellation_details.reason}. Error details: {cancellation_details.error_details}"
    return "Unknown error during speech synthesis."


if __name__ == "__main__":
    os.environ["AZURE_SPEECH_KEY"] = "YOUR_AZURE_SPEECH_KEY"  # Placeholder
    os.environ["AZURE_SPEECH_REGION"] = "YOUR_AZURE_SPEECH_REGION"  # E.g., "westus2"

    brief_text = "Here is a brief summary of the retrieved search results. The main topics include artificial intelligence, machine learning applications, and ethical considerations in AI development."
    status = generate_spoken_brief(brief_text, "search_brief.mp3")
    # print(status)
