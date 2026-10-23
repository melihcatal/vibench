import speech_client

def handle_partial_results(stream):
    for result in stream.iter_results():
        if result.is_final:
            print(f"Final result: {result.transcript}")
        else:
            print(f"Interim result: {result.transcript}")