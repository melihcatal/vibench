import boto3
import requests
import json

def get_timestamped_transcript(transcript_uri: str) -> dict:
    # Download the transcript JSON from the S3 URI
    response = requests.get(transcript_uri)
    response.raise_for_status()  # Raise an exception for HTTP errors
    transcript_data = json.loads(response.text)

    # Extract relevant information including word-level timestamps
    # The exact structure depends on the Transcribe output, which usually includes
    # 'results' and 'items' for detailed word-level data.
    
    # This is a simplified example. A full implementation would parse
    # the 'items' array from the transcript_data['results'] for detailed timestamps.
    
    # For demonstration, we'll return a simplified structure or the raw data.
    
    # Example of extracting items with timestamps:
    word_timestamps = []
    if 'results' in transcript_data and 'items' in transcript_data['results']:
        for item in transcript_data['results']['items']:
            if item['type'] == 'pronunciation':
                word_timestamps.append({
                    'word': item['alternatives'][0]['content'],
                    'start_time': item['start_time'],
                    'end_time': item['end_time']
                })
    
    return {
        "full_transcript": transcript_data['results']['transcripts'][0]['transcript'] if 'results' in transcript_data and 'transcripts' in transcript_data['results'] else "",
        "word_timestamps": word_timestamps
    }

if __name__ == '__main__':
    # Replace with an actual transcript URI from a completed AWS Transcribe job
    example_transcript_uri = "https://s3.us-east-1.amazonaws.com/aws-transcribe-us-east-1-prod/your-job-id/your-job-id.json"
    try:
        transcript_with_timestamps = get_timestamped_transcript(example_transcript_uri)
        print("Full Transcript:")
        print(transcript_with_timestamps["full_transcript"])
        print("\nWord Timestamps:")
        for item in transcript_with_timestamps["word_timestamps"]:
            print(f"  Word: {item['word']}, Start: {item['start_time']}, End: {item['end_time']}")
    except Exception as e:
        print(f"Error retrieving or parsing timestamped transcript: {e}")
