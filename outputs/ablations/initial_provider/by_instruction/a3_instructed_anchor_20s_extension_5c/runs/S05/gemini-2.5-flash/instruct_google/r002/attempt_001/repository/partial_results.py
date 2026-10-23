def handle_partial_and_final_results(responses):
    for response in responses:
        if not response.results:
            continue

        result = response.results[0]
        if not result.alternatives:
            continue

        transcript = result.alternatives[0].transcript

        if result.is_final:
            print(f"Final: {transcript}")
        else:
            print(f"Partial: {transcript}")
