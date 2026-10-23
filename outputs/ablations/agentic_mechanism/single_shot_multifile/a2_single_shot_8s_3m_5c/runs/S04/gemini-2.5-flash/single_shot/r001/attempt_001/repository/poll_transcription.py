import os
import time
from typing import Optional
from google.cloud import speech_v1p1beta1 as speech

from speech_client import get_speech_client
from speech_models import TranscriptionResult, WordInfo, SegmentInfo

def poll_transcription_job(operation_name: str, timeout: int = 300) -> Optional[TranscriptionResult]:
    client = get_speech_client()
    operation = client.get_operation(operation_name)

    start_time = time.time()
    while not operation.done:
        if time.time() - start_time > timeout:
            return TranscriptionResult(job_id=operation_name, status="TIMEOUT", transcript_text="")
        time.sleep(5)  # Wait for 5 seconds before re-checking the operation status
        operation = client.get_operation(operation_name)

    if operation.error:
        return TranscriptionResult(job_id=operation_name, status="ERROR", transcript_text=str(operation.error))

    # Parse the results
    full_transcript = []
    word_infos = []
    segments = []

    if operation.result and operation.result.results:
        for result in operation.result.results:
            if result.alternatives:
                alternative = result.alternatives[0]
                full_transcript.append(alternative.transcript)

                if alternative.words:
                    current_segment_text = []
                    current_segment_start = None
                    current_segment_end = None
                    current_speaker_tag = None

                    for word in alternative.words:
                        start_s = word.start_time.seconds + word.start_time.nanos * 1e-9
                        end_s = word.end_time.seconds + word.end_time.nanos * 1e-9
                        word_infos.append(WordInfo(word=word.word, start_time_seconds=start_s, end_time_seconds=end_s, speaker_tag=word.speaker_tag))

                        if word.speaker_tag != current_speaker_tag or not current_segment_text:
                            if current_segment_text:
                                segments.append(SegmentInfo(
                                    speaker_tag=current_speaker_tag,
                                    start_time_seconds=current_segment_start,
                                    end_time_seconds=current_segment_end,
                                    text=" ".join(current_segment_text)
                                ))
                            current_segment_text = [word.word]
                            current_segment_start = start_s
                            current_segment_end = end_s
                            current_speaker_tag = word.speaker_tag
                        else:
                            current_segment_text.append(word.word)
                            current_segment_end = end_s

                    if current_segment_text:
                        segments.append(SegmentInfo(
                            speaker_tag=current_speaker_tag,
                            start_time_seconds=current_segment_start,
                            end_time_seconds=current_segment_end,
                            text=" ".join(current_segment_text)
                        ))

    return TranscriptionResult(
        job_id=operation_name,
        status="COMPLETED",
        transcript_text=" ".join(full_transcript),
        word_infos=word_infos,
        segments=segments
    )