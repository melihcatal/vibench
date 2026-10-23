# [SAME-SCENARIO]
# Handle partial and final streaming recognition events from Amazon Transcribe Streaming
# Provider: Amazon Transcribe Streaming (AWS SDK boto3)
import boto3
import json

# Initialize the client (credentials loaded from env vars)
boto_client = boto3.client('transcribe')

# A simple callback framework that third‑party code can register on
# Handles both interim (partial) and complete (final) results.
class PartialResultHandler:
    def __init__(self):
        self.partial_callbacks = []
        self.final_callbacks = []

    def on_partial(self, callback):
        self.partial_callbacks.append(callback)

    def on_final(self, callback):
        self.final_callbacks.append(callback)

    def _dispatch_partial(self, event):
        for cb in self.partial_callbacks:
            cb(event)

    def _dispatch_final(self, event):
        for cb in self.final_callbacks:
            cb(event)

# Create a global instance - callers can import and register handlers
partial_handler = PartialResultHandler()

# Example minimal event processing loop (sync for illustration)
def process_transcription(stream_arn):
    # Start the streaming job (only once per session)
    boto_client.start_stream_transcription(
        LanguageCode='en-US',
        MediaSampleRateHertz=16000,
        MediaEncoding='pcm',
        # Listener for results is supplied below
    )
    print('Listening for results...')

    # Synchronous polling of the stream (in production use AWS EventStreams or a streaming SDK)
    while True:
        # Grab the next result chunk; in real code use the iterable returned by start_stream_transcription
        result = boto_client.get_transcription_result(StreamArn=stream_arn)
        if not result:
            continue

        # Transcribe returns a JSON payload with 'InterimResults' or 'Results'
        payload = json.loads(result['Payload'])
        if 'InterimResults' in payload:
            for interim in payload['InterimResults']:
                alternative = interim.get('Alternatives', [{}])[0]
                transcript = alternative.get('Transcript', '')
                partial_handler._dispatch_partial({'transcript': transcript, 'is_final': False})
        if 'Results' in payload:
            for final in payload['Results']:
                alternative = final.get('Alternatives', [{}])[0]
                transcript = alternative.get('Transcript', '')
                partial_handler._dispatch_final({'transcript': transcript, 'is_final': True})

if __name__ == '__main__':
    # Example usage of the handler
    stream_arn = 'YOUR_STREAM_ARN_HERE'  # obtain from start_stream_transcription response
    partial_handler.on_partial(lambda ev: print('Partial:', ev))
    partial_handler.on_final(lambda ev: print('Final:', ev))
    process_transcription(stream_arn)
