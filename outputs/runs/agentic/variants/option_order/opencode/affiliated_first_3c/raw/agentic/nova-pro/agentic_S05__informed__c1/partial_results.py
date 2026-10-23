import speech_client


def partial_results():
    # Simulate partial results
    results = [{"Transcript": "Hello"}, {"Transcript": "world"}]
    for result in results:
        print(result["Transcript"])
