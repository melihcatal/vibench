from typing import List, Dict, Union
from speech_client import AssemblyAIClient
from poll_transcription import poll_for_transcript


def get_timestamped_words(audio_url: str) -> List[Dict[str, Union[str, float]]]:
    """
    Submits a job and returns a list of words with their start and end timestamps.

    Args:
        audio_url: The public URL of the audio file.

    Returns:
        A list of dictionaries, each containing a word and its start/end time in milliseconds.
    """
    client = AssemblyAIClient()
    print("Submitting job...")
    # word_details is true by default, but explicitly requested for clarity.
    submit_response = client.submit_transcription(audio_url)

    print(f"Job submitted with ID: {submit_response.id}. Polling for completion...")
    completed_response = poll_for_transcript(submit_response.id)

    if not completed_response.words:
        print("No word-level timestamps found in the response.")
        return []

    timestamps = [
        {"word": word.text, "start_ms": word.start, "end_ms": word.end}
        for word in completed_response.words
    ]
    return timestamps


# Example usage:
# if __name__ == '__main__':
#     AUDIO_URL = "https://storage.googleapis.com/aai-docs-samples/nbc.mp3"
#     word_timestamps = get_timestamped_words(AUDIO_URL)
#     for word_info in word_timestamps[:10]:  # Print first 10 words
#         print(
#             f"Word: \"{word_info['word']}\", "
#             f"Start: {word_info['start_ms']}ms, "
#             f"End: {word_info['end_ms']}ms"
#         )
