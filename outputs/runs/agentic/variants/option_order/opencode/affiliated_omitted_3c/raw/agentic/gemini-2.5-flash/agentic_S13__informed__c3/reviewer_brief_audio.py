import os
import azure.cognitiveservices.speech as speechsdk
from safety_models import ReviewerBriefAudioRequest, ReviewerBriefAudioResponse

def reviewer_brief_audio(request: ReviewerBriefAudioRequest) -> ReviewerBriefAudioResponse:
    speech_key = os.environ.get("AZURE_SPEECH_KEY")
    speech_region = os.environ.get("AZURE_SPEECH_REGION")

    if not speech_key or not speech_region:
        raise ValueError("AZURE_SPEECH_KEY and AZURE_SPEECH_REGION environment variables must be set.")

    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
    speech_config.speech_synthesis_voice_name = 'en-US-JennyNeural'

    audio_config = speechsdk.audio.AudioOutputConfig(use_ Alber_speaker_output=False, filename="temp_audio_brief.wav")

    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    result = speech_synthesizer.speak_text_async(request.brief_text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        with open("temp_audio_brief.wav", "rb") as audio_file:
            audio_content = audio_file.read()
        os.remove("temp_audio_brief.wav") # Clean up the temporary file
        return ReviewerBriefAudioResponse(audio_content=audio_content)
    else:
        raise Exception(f"Speech synthesis failed: {result.reason}, {result.error_details}")
