from speech_client import speech_to_text


def partial_results():
    with speech_to_text.get_websocket(content_type="audio/l16;rate=44100") as websocket:
        while websocket.is_open():
            result = websocket.receive()
            if result["results"][0]["is_final"]:
                print(
                    "Final result: ",
                    result["results"][0]["alternatives"][0]["transcript"],
                )
            else:
                print(
                    "Partial result: ",
                    result["results"][0]["alternatives"][0]["transcript"],
                )
