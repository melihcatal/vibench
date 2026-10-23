import os
import ibm_watson

IBM_TTS_APIKEY = os.getenv("IBM_TTS_APIKEY")
IBM_TTS_URL = os.getenv("IBM_TTS_URL")


def reviewer_brief_audio(text):
    tts = ibm_watson.TextToSpeechV1(iam_apikey=IBM_TTS_APIKEY, url=IBM_TTS_URL)
    with open("reviewer_brief.mp3", "wb") as audio_file:
        audio_file.write(
            tts.synthesize(text, voice="en-US_AllisonV3Voice", accept="audio/mp3")
            .get_result()
            .content
        )
