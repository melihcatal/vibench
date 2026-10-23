from ibm_watson import SpeechToTextV1


def submit_transcription(audio_file_path):
    with open(audio_file_path, "rb") as audio_file:
        response = speech_to_text.create_job(audio=audio_file, content_type="audio/mp3")
        return response.get_result()
