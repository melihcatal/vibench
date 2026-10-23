import os
import json
import requests
from speech_client import get_batch_client
from speech_models import BatchTranscriptionResult

# Required environment variables for Azure Cognitive Services Speech & Translator
# AZURE_SPEECH_BATCH_KEY, AZURE_SPEECH_BATCH_REGION, AZURE_TRANSLATOR_TEXT_KEY, AZURE_TRANSLATOR_LOCATION

def translate_transcript(transcript: BatchTranscriptionResult, target_language: str = "es"):
    """Translates each segment of a batch transcription result to a target language.

    Args:
        transcript (BatchTranscriptionResult): The API response containing \"results\" with \"segments\".
        target_language (str): ISO 639-1 language code, default Spanish.

    Returns:
        dict: A dictionary mapping segment_id to a dict containing translated text and confidence.
    """
    client = get_batch_client()
    endpoint = client.endpoint
    text_key = os.getenv("AZURE_TRANSLATOR_TEXT_KEY")
    location = os.getenv("AZURE_TRANSLATOR_LOCATION")
    if not text_key or not location:
        raise RuntimeError(
            "Set AZURE_TRANSLATOR_TEXT_KEY and AZURE_TRANSLATOR_LOCATION environment variables."
        )

    translator_url = f"https://{location}.api.cognitive.microsofttranslator.com/translate?api-version=3.0&to={target_language}"
    headers = {
        "Ocp-Apim-Subscription-Key": text_key,
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": text_key
    }

    segments = transcript.get("results", [{}])[0].get("segments", [])
    results = {}
    for seg in segments:
        seg_id = seg.get("segment_id")
        speaker = seg.get("speaker_labels", [])
        audio_start = seg.get("audio_start_time_ms")
        audio_start = audio_start / 1000.0 if audio_start else 0.0
        spoken_text = seg.get("content", "")
        # Concatenate spoken text across speaker turns for simplicity
        payload = [{"Text": spoken_text}]
        response = requests.post(translator_url, headers=headers, json=payload)
        response.raise_for_status()
        translation = response.json()[0]["translations"][0]["text"]
        results[seg_id] = {
            "segment_id": seg_id,
            "speaker_labels": speaker,
            "audio_start_sec": audio_start,
            "translated_text": translation,
            "confidence": seg.get("confidence", 0.0)
        }
    return results

if __name__ == "__main__":
    import sys, json
    if len(sys.argv) < 3:
        print("Usage: python translate_transcript.py <job_id> <target_lang> [poll_interval=10] <result_json_file>\n")
        sys.exit(1)
    job_id = sys.argv[1]
    target_lang = sys.argv[2]
    poll_interval = int(sys.argv[3]) if len(sys.argv) > 3 else 10
    result_file = sys.argv[4] if len(sys.argv) > 4 else "transcription_result.json"

    # Example polling block (placeholder) - in real usage poll_transcription.py would be used first
    # result_json = poll_transcription(job_id, poll_interval)
    # For demo, assume result_json loaded from file
    with open(result_file, "r", encoding="utf-8") as f:
        transcript = json.load(f)
    translated = translate_transcript(transcript, target_lang)
    print(json.dumps(translated, ensure_ascii=False, indent=2))
