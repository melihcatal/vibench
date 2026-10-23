import os
from google.cloud import texttospeech
from safety_models import ReviewerBriefRequest, ReviewerBriefAudioResponse

def generate_reviewer_brief_audio(request: ReviewerBriefRequest) -> ReviewerBriefAudioResponse:
    """
    Generates spoken briefs for moderation reviewers using Google Cloud Text-to-Speech.
    """
    # Google Cloud Text-to-Speech client setup
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set for authentication
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=request.summary_text)

    # Select the language and SSML voice type
    # You can choose a different voice name for different accents or genders
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL # Or FEMALE, MALE
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3 # Or LINEAR16, OGG_OPUS
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary. We need to return it as bytes.
    return ReviewerBriefAudioResponse(
        audio_content=response.audio_content,
        content_type="audio/mpeg" # Adjust content type based on audio_encoding
    )
