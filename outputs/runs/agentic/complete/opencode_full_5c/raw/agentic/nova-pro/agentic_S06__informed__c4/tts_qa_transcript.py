import ibm_watson


def transcribe_audio(audio_file):
    speech_to_text = ibm_watson.SpeechToTextV1(
        iam_apikey=os.getenv("IBM_STT_APIKEY"), url=os.getenv("IBM_STT_URL")
    )
    with open(audio_file, "rb") as audio:
        response = speech_to_text.recognize(
            audio=audio, content_type="audio/wav"
        ).get_result()
    return response["results"][0]["alternatives"][0]["transcript"]
