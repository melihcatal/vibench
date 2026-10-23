from speech_models import normalize_partial_result, normalize_final_result

def handle_partial_results(response):
    for result in response.results:
        if result.is_partial:
            transcript = normalize_partial_result(result)
            print(f"Partial: {transcript}")
        else:
            transcript = normalize_final_result(result)
            print(f"Final: {transcript}")