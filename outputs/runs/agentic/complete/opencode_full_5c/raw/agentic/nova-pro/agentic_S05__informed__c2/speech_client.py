import deepgram


def create_client(api_key):
    return deepgram.Client(api_key)


def configure_stream(client, language, punctuation):
    pass
