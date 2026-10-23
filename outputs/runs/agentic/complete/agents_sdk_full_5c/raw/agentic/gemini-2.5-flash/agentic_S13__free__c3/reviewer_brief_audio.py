import os
from google.cloud import texttospeech
from safety_client import get_text_to_speech_client # To ensure provider signal linkage
from safety_models import AudioBriefRequest, AudioBriefResult

def generate_spoken_brief_for_reviewer(request: AudioBriefRequest) -> AudioBriefResult:
    """
    Generates spoken briefs for moderation reviewers using Google Cloud Text-to-Speech API.
    """
    client = get_text_to_speech_client()

    synthesis_input = texttospeech.SynthesisInput(text=request.text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=request.language_code,
        name=request.voice_name
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=request.speaking_rate,
        pitch=request.pitch
    )

    response = client.synthesize_speech(
        request={
            "input": synthesis_input,
            "voice": voice,
            "audio_config": audio_config,
        }
    )

    # The response's audio_content is binary.
    return AudioBriefResult(audio_content=response.audio_content)

if __name__ == '__main__':
    # Example usage:
    # Ensure gcloud authentication is configured.
    # brief_request = AudioBriefRequest(
    #     text="This case involves a user appeal regarding a toxicity moderation decision. "
    #          "The original comment was 'You are stupid.' The user claims it was taken out of context."
    # )
    # audio_brief = generate_spoken_brief_for_reviewer(brief_request)
    #
    # # To save and play the audio:
    # # with open("reviewer_brief.mp3", "wb") as out:
    # #     out.write(audio_brief.audio_content)
    # #     print('Audio content written to file "reviewer_brief.mp3"')
    pass
