import ibm_watson

IBM_TTS_APIKEY = "your-ibm-tts-apikey"
IBM_TTS_URL = "your-ibm-tts-url"


def platform_brief_audio(text):
    tts = ibm_watson.TextToSpeechV1(iam_apikey=IBM_TTS_APIKEY, url=IBM_TTS_URL)
    with open("output.wav", "wb") as audio_file:
        audio_file.write(
            tts.synthesize(text, voice="en-US_AllisonV3Voice", accept="audio/wav")
            .get_result()
            .content
        )
