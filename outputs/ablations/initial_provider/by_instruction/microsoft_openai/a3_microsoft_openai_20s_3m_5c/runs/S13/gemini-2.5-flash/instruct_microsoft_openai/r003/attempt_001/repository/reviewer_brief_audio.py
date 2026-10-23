from safety_client import get_google_text_to_speech_client
from typing import Tuple

def generate_reviewer_brief_audio(text: str, output_filename: str = "brief.mp3") -> Tuple[bytes, str]:
    client = get_google_text_to_speech_client()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Voice selection for the audio
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary. You can save it to a file.
    with open(output_filename, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "{output_filename}" ')
    
    return response.audio_content, output_filename
