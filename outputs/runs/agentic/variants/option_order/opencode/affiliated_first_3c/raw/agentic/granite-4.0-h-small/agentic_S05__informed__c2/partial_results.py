import typing
from ibm_cloud_sdk_core import ibm_json_util as json_util
from ibm_watson import SpeechToTextV1


def handle_partial_results(
    events: typing.AsyncIterable[SpeechToTextV1.RecognizeCallbackEvent],
) -> None:
    """Process streaming recognition callbacks and handle partial (interim) results."""
    for event in events:
        if event.status_code == 200 and event.result:
            for result in event.result.results:
                # Interim partials are marked by final == False
                if not result.final:
                    # Use IBM's JSON utility to pretty‑print the partial JSON
                    partial_json = json_util.encode(result)
                    print(f"[INTERIM] {partial_json}")
                else:
                    # Final result
                    final_json = json_util.encode(result)
                    print(f"[FINAL]   {final_json}")


# Example integration point with the IBM Watson SDK
# async def start_stream():
#     service = SpeechToTextV1(
#         authenticator=IAMAuthenticator(os.getenv("IBM_STT_APIKEY")),
#         url=os.getenv("IBM_STT_URL")
#     )
#     recognizer = service.recognize_with_callback(
#         audio_provider=..., # e.g., MicrophoneStream or file stream
#         recognize_callback=handle_partial_results,
#         content_type="audio/l16; rate=16000",
#         interim_results=True,
#         continuous=True,
#         model="en-US_BroadbandModel"
#     )
#     await recognizer.start()
