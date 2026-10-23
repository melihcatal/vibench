import os
from google.cloud import texttospeech_v1 as texttospeech

def generate_reviewer_brief_audio(brief_text: str, output_filepath: str = "reviewer_brief.mp3") -> dict:
    """
    Generate spoken briefs for moderation reviewers using Google Cloud Text-to-Speech API.

    Args:
        brief_text: The text content of the brief.
        output_filepath: The path where the generated audio file will be saved.

    Returns:
        A dictionary indicating the success of the operation and the output file path.
    """
    # Google Cloud Text-to-Speech API client setup
    tts_client = texttospeech.TextToSpeechClient()

    # Configure the synthesis request
    synthesis_input = texttospeech.SynthesisInput(text=brief_text)

    # Select the voice parameters
    # You can choose different voices (e.g., 'en-US-Standard-C', 'en-US-Wavenet-F')
    # and gender. Ensure the chosen voice is available.
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL # Or MALE/FEMALE
    )

    # Select the audio file type
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request
    response = tts_client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    # Write the audio content to a file
    try:
        with open(output_filepath, "wb") as out:
            out.write(response.audio_content)
        return {
            "status": "success",
            "message": f"Audio content written to {output_filepath}",
            "output_filepath": output_filepath,
            "source": "Google Cloud Text-to-Speech API"
        }
    except IOError as e:
        return {
            "status": "error",
            "message": f"Could not write audio file: {e}",
            "source": "Google Cloud Text-to-Speech API"
        }

if __name__ == "__main__":
    brief = "Reviewer brief: A batch of messages contained high toxicity and hate speech. Some messages were also flagged for sexually explicit content. Please prioritize these cases for manual review and consider escalation for repeat offenders."
    result = generate_reviewer_brief_audio(brief, "moderation_brief.mp3")
    print(result)

    brief_spanish = "Resumen para el revisor: Se detectó contenido peligroso en un envío reciente. Por favor, revise cuidadosamente."
    # For different languages, change the `language_code` in `VoiceSelectionParams`.
    # For simplicity, this example keeps 'en-US' for the main function, but in a real app,
    # you'd pass language as a parameter or infer it.
    # result_es = generate_reviewer_brief_audio(brief_spanish, "moderation_brief_es.mp3")
    # print(result_es)
