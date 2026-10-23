from speech_client import speech_to_text


def stream_with_language(language="en-US", enable_automatic_punctuation=True):
    with speech_to_text.get_websocket(
        content_type="audio/l16;rate=44100",
        language_customization_id=language,
        enable_automatic_punctuation=enable_automatic_punctuation,
    ) as websocket:
        while websocket.is_open():
            result = websocket.receive()
            if result["results"][0]["is_final"]:
                print(result["results"][0]["alternatives"][0]["transcript"])
