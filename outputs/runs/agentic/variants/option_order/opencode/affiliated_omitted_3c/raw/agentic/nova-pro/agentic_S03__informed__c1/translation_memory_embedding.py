import ibm_watson


def translation_memory_embedding(text):
    text_service = ibm_watson.TextToSpeechV1(
        iam_apikey="YOUR_API_KEY", url="YOUR_SERVICE_URL"
    )
    with open("output.mp3", "wb") as audio_file:
        audio_file.write(
            text_service.synthesize(
                text, voice="en-US_AllisonV3Voice", accept="audio/mp3"
            )
            .get_result()
            .content
        )
    return "output.mp3"
