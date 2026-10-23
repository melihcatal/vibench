from speech_models import SpeechRecognitionResult

def handle_partial_results(recognition_result: SpeechRecognitionResult):
    if recognition_result.is_final:
        print(f"Final result: {recognition_result.text}")
    else:
        print(f"Partial result: {recognition_result.text}")

def process_speech_stream(results_generator):
    for result in results_generator:
        if isinstance(result, SpeechRecognitionResult):
            handle_partial_results(result)
        elif isinstance(result, Exception):
            print(f"Error in stream: {result}")
            raise result
