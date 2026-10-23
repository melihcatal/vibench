import json
import time
import urllib.request

import boto3


def diarized_transcript(job_id, config=None):
    config = config or {}
    client = boto3.client("transcribe", region_name=config.get("region"))
    while True:
        response = client.get_transcription_job(TranscriptionJobName=job_id)
        job_status = response["TranscriptionJob"]["TranscriptionJobStatus"]
        if job_status == "COMPLETED":
            transcript_uri = response["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]
            with urllib.request.urlopen(transcript_uri) as f:
                transcript_json = json.loads(f.read().decode("utf-8"))
            
            diarized_segments = []
            items = transcript_json["results"]["items"]
            
            current_speaker = None
            current_segment_text = ""
            current_start_time = None
            current_end_time = None

            for item in items:
                if item["type"] == "pronunciation":
                    speaker_label = item.get("speaker_label")
                    if speaker_label and speaker_label != current_speaker:
                        if current_segment_text:
                            diarized_segments.append({
                                "speaker": current_speaker,
                                "text": current_segment_text.strip(),
                                "start_time": current_start_time,
                                "end_time": current_end_time
                            })
                        current_speaker = speaker_label
                        current_segment_text = item["alternatives"][0]["content"]
                        current_start_time = item["start_time"]
                        current_end_time = item["end_time"]
                    else:
                        current_segment_text += " " + item["alternatives"][0]["content"]
                        current_end_time = item["end_time"]
                elif item["type"] == "punctuation":
                    current_segment_text += item["alternatives"][0]["content"]
                    
            if current_segment_text:
                diarized_segments.append({
                    "speaker": current_speaker,
                    "text": current_segment_text.strip(),
                    "start_time": current_start_time,
                    "end_time": current_end_time
                })
            
            return diarized_segments
            
        elif job_status == "FAILED":
            raise Exception(f"Transcription job {job_id} failed.")
        time.sleep(5)
