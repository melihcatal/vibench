import os


def get_speech_client():
    os.environ["DEEPGRAM_API_KEY"] = "your-deepgram-api-key"
    import deepgram

    return deepgram.Client(os.getenv("DEEPGRAM_API_KEY"))


def get_speech_models():
    # Define local request, response, and normalization helpers here
    pass
