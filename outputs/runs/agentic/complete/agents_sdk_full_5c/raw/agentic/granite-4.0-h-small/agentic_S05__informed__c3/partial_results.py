import json

def parse_partial_results(response):
    """Extract interim transcripts from partial results returned by the streaming API."""
    # The response format varies by provider; this example assumes a generic JSON structure.
    try:
        data = json.loads(response)
        # Example for Google Speech Streamingrecognize: results contains alternates with transcript
        if 'results' in data:
            for result in data['results']:
                if result.get('is_final') is False:
                    interim = result.get('alternatives', [{}])[0].get('transcript', '')
                    print('Interim:', interim)
        # Example for Deepgram: interim results under 'results' with 'alternatives' and 'is_final'
        if 'results' in data and 'alternatives' in data:
            for result in data['results']:
                if not result.get('is_final'):
                    interim = result['alternatives'][0].get('value', '')
                    print('Interim:', interim)
    except json.JSONDecodeError:
        print('Failed to decode response:', response)
    return

# Helper to extract final transcript when final flag is set
final_transcript_cache = {}

def extract_final_transcript(result):
    # Cache final transcripts by id if needed
    if result.get('is_final'):
        id_ = result.get('result_id') or result.get('id')
        final_transcript_cache[id_] = result.get('alternatives', [{}])[0].get('transcript', '')
    return final_transcript_cache

if __name__ == "__main__":
    # Simulated response handling
    sample_response = json.dumps({
        "results": [
            {"alternatives": [{"transcript": "Hello world"}], "is_final": False},
            {"alternatives": [{"transcript": "Hello there."}], "is_final": True}
        ]
    })
    parse_partial_results(sample_response)
