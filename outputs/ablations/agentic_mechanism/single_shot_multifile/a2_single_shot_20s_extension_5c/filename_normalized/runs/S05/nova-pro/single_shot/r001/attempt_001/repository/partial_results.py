import speech_client

def handle_partial_results(stream):
    client = speech_client.get_streaming_client()
    for result in stream:
        if result.is_final:
            print(f'Final: {result.transcript}')
        else:
            print(f'Interim: {result.transcript}')
