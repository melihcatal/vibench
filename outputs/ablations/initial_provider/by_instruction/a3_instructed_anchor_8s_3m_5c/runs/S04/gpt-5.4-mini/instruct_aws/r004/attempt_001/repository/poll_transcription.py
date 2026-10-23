import sys
import time

from speech_client import load_config
from speech_models import parse_transcribe_result


def poll_transcription(job_name: str, interval: int = 15, timeout: int = 3600):
    client = load_config().transcribe
    deadline = time.time() + timeout
    while True:
        result = client.get_transcription_job(TranscriptionJobName=job_name)
        parsed = parse_transcribe_result(result)
        if parsed["status"] in {"COMPLETED", "FAILED"}:
            return parsed
        if time.time() >= deadline:
            raise TimeoutError(job_name)
        time.sleep(interval)


if __name__ == "__main__":
    print(poll_transcription(sys.argv[1]))
