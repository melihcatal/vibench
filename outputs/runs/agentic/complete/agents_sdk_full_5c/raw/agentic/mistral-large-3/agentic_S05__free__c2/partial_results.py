from speech_models import PartialResult, FinalResult

def handle_partial_result(response):
    for result in response.results:
        alternatives = result.alternatives
        if not alternatives:
            continue
        transcript = alternatives[0].transcript
        is_final = result.is_final
        confidence = alternatives[0].confidence if hasattr(alternatives[0], "confidence") else 0.0

        if is_final:
            final_result = FinalResult(transcript=transcript, confidence=confidence)
            print(f"Final: {final_result.transcript} (Confidence: {final_result.confidence:.2f})")
            yield final_result
        else:
            partial_result = PartialResult(transcript=transcript)
            print(f"Partial: {partial_result.transcript}")
            yield partial_result