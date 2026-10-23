import os
import azure.cognitiveservices.speech as speechsdk


def synthesize_ssml(ssml_text, output_format="riff-16khz-16bit-mono-pcm"):
    speech_key = os.environ.get("AZURE_SPEECH_KEY")
    speech_region = os.environ.get("AZURE_SPEECH_REGION")

    if not speech_key or not speech_region:
        raise ValueError(
            "AZURE_SPEECH_KEY and AZURE_SPEECH_REGION environment variables must be set"
        )

    speech_config = speechsdk.SpeechConfig(
        subscription=speech_key, region=speech_region
    )
    speech_config.set_speech_synthesis_output_format(
        speechsdk.SpeechSynthesisOutputFormat[output_format]
    )

    synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=None
    )

    result = synthesizer.speak_ssml_async(ssml_text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        audio_data = result.audio_data
        return audio_data
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        raise Exception(f"SSML synthesis canceled: {cancellation_details.reason}")
    else:
        raise Exception(f"SSML synthesis failed: {result.reason}")


def create_ssml(text, voice_name="en-US-JennyNeural", rate="medium", pitch="medium"):
    ssml = f"""<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">
    <voice name="{voice_name}">
        <prosody rate="{rate}" pitch="{pitch}">
            {text}
        </prosody>
    </voice>
</speak>"""
    return ssml
