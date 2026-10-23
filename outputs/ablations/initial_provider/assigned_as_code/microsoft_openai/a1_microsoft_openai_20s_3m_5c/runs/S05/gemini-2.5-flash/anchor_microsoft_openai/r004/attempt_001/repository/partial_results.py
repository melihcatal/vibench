from typing import Generator
from speech_models import SpeechRecognitionResult

def partial_results_handler(results: Generator[SpeechRecognitionResult, None, None]):
    for result in results:
        if result.is_final:
            print(f"Final: {result.text}")
        else:
            print(f"Partial: {result.text}")
