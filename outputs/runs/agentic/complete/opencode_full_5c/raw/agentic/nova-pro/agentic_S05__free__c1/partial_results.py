import os
from google.cloud import speech_v1p1beta1 as speech


def partial_results(responses):
    for response in responses:
        for result in response.results:
            if not result.is_final:
                print("Interim:", result.alternatives[0].transcript)
            else:
                print("Final:", result.alternatives[0].transcript)
