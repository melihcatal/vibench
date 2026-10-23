from typing import Iterator, Dict, Any
from speech_models import SpeechRecognitionResult

def partial_results_handler(results: Iterator[Dict[str, Any]]) -> Iterator[SpeechRecognitionResult]:
    for result in results:
        # Here we can add logic to process partial and final results
        # For example, printing them differently or storing them.
        # The `is_final` flag from the provider's response helps distinguish.
        processed_result = SpeechRecognitionResult(
            text=result.get("text", ""),
            is_final=result.get("is_final", False),
            language_code=result.get("language_code", "en-US")
        )
        yield processed_result
