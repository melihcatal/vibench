from google.cloud import speech

def get_timestamped_transcript(transcription_result):
    client = speech.SpeechClient()
    response = client.recognize(transcription_result)
    for result in response.results:
        for alternative in result.alternatives:
            words = alternative.words
            for word_info in words:
                start_time = word_info.start_time
                end_time = word_info.end_time
                word = word_info.word
                print(f"Word: {word}, Start Time: {start_time}, End Time: {end_time}")

if __name__ == "__main__":
    # Example usage
    transcription_result = {"config": {}, "results": [{"alternatives": [{"transcript": "Hello world", "words": [{"word": "Hello", "start_time": {"seconds": 0, "nanos": 0}, "end_time": {"seconds": 1, "nanos": 0}}, {"word": "world", "start_time": {"seconds": 1, "nanos": 0}, "end_time": {"seconds": 2, "nanos": 0}}]}]}]}
    get_timestamped_transcript(transcription_result)