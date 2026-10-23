import json
import urllib.parse
from typing import List, Dict, Any, TypedDict
import speech_client

class WordDetail(TypedDict):
    word: str
    start_time: str
    end_time: str
    speaker_label: str

def download_and_parse_transcribe_json(s3_uri: str) -> Dict[str, Any]:
    s3_client = speech_client.get_s3_client()
    parsed_url = urllib.parse.urlparse(s3_uri)
    bucket_name = parsed_url.netloc
    key = parsed_url.path.lstrip('/')
    
    response = s3_client.get_object(Bucket=bucket_name, Key=key)
    file_content = response['Body'].read().decode('utf-8')
    return json.loads(file_content)

def extract_full_transcript_text(transcribe_json: Dict[str, Any]) -> str:
    return transcribe_json.get("results", {}).get("transcripts", [{}])[0].get("transcript", "")

def extract_word_details(transcribe_json: Dict[str, Any]) -> List[WordDetail]:
    words = []
    items = transcribe_json.get("results", {}).get("items", [])
    current_speaker = None
    
    for item in items:
        if item.get("type") == "pronunciation":
            speaker_label = item.get("speaker_label")
            if speaker_label:
                current_speaker = speaker_label
            
            words.append(
                WordDetail(
                    word=item.get("alternatives", [{}])[0].get("content", ""),
                    start_time=item.get("start_time", ""),
                    end_time=item.get("end_time", ""),
                    speaker_label=current_speaker if current_speaker else "unknown"
                )
            )
    return words