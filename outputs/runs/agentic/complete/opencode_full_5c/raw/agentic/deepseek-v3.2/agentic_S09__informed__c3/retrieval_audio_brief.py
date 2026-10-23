import os
import azure.cognitiveservices.speech as speechsdk
from typing import List


def generate_audio_brief(
    search_results: List[str], output_file: str = "brief.mp3"
) -> str:
    """Generate a spoken brief from retrieved search results using Azure Speech TTS."""
    speech_key = os.getenv("AZURE_SPEECH_KEY")
    speech_region = os.getenv("AZURE_SPEECH_REGION")

    if not speech_key or not speech_region:
        raise ValueError(
            "AZURE_SPEECH_KEY and AZURE_SPEECH_REGION environment variables are required"
        )

    speech_config = speechsdk.SpeechConfig(
        subscription=speech_key, region=speech_region
    )
    speech_config.speech_synthesis_voice_name = "en-US-JennyNeural"

    audio_config = speechsdk.audio.AudioOutputConfig(filename=output_file)

    synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=audio_config
    )

    # Create brief from search results
    if not search_results:
        brief_text = "No search results found."
    else:
        brief_text = f"Found {len(search_results)} relevant documents. "
        brief_text += "Here are the key findings: "

        for i, result in enumerate(search_results[:3], 1):
            summary = result[:100] + "..." if len(result) > 100 else result
            brief_text += f"Result {i}: {summary}. "

        if len(search_results) > 3:
            brief_text += f"And {len(search_results) - 3} more results."

    result = synthesizer.speak_text_async(brief_text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        return output_file
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        raise Exception(
            f"Speech synthesis canceled: {cancellation_details.reason}. Error details: {cancellation_details.error_details}"
        )
    else:
        raise Exception(f"Speech synthesis failed: {result.reason}")


def list_available_voices() -> List[str]:
    """List available Azure Speech TTS voices."""
    speech_key = os.getenv("AZURE_SPEECH_KEY")
    speech_region = os.getenv("AZURE_SPEECH_REGION")

    if not speech_key or not speech_region:
        raise ValueError(
            "AZURE_SPEECH_KEY and AZURE_SPEECH_REGION environment variables are required"
        )

    speech_config = speechsdk.SpeechConfig(
        subscription=speech_key, region=speech_region
    )
    synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=None
    )

    result = synthesizer.get_voices_async().get()

    if result.reason == speechsdk.ResultReason.VoicesListRetrieved:
        return [voice.short_name for voice in result.voices]
    else:
        raise Exception(f"Failed to retrieve voices: {result.reason}")
