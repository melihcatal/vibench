import time
import os
from speech_client import SpeechClient
from speech_models import TranscriptionResponse

# Configuration (environment variable or config file)
ASSEMBLYAI_API_KEY = os.getenv('ASSEMBLYAI_API_KEY')

# Utility to check if response can be parsed as TranscriptionResponse

def parse_response(raw: dict) -> TranscriptionResponse | None:
    if raw:
        return TranscriptionResponse(raw)
    return None


def poll_transcription(job_id: str, poll_interval: int = 5, timeout: int = 300) -> str:
    """Poll a transcription job until completion or timeout."""
    client = SpeechClient(api_key=ASSEMBLYAI_API_KEY)
    end_time = time.time() + timeout
    while time.time() < end_time:
        status = client.check_status(job_id)
        # Normalize response
        resp = parse_response(status)
        if resp and resp.job_id:
            if resp.extra.get("status", "") == "completed":
                print("Transcription completed.")
                result = client.download_result(job_id)
                result_obj = parse_response(result)
                if result_obj and result_obj.segments:
                    return result_obj.segments  # return parsed segments list
                else:
                    raise RuntimeError(f"Unexpected result format: {result}")
        print(f"Job {job_id} status: {resp.extra.get('status')}. Retrying in {poll_interval}s...")
        time.sleep(poll_interval)
    raise TimeoutError(f"Transcription job {job_id} did not complete within {timeout}s timeout.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Poll transcription job status and retrieve transcript.")
    parser.add_argument("job_id", help="Job ID returned from submit_transcription.")
    parser.add_argument("--interval", type=int, default=5, help="Polling interval seconds (default 5).")
    parser.add_argument("--timeout", type=int, default=300, help="Timeout in seconds (default 300).")
    args = parser.parse_args()
    try:
        segments = poll_transcription(args.job_id, poll_interval=args.interval, timeout=args.timeout)
        # Simple pretty-print of segments (or extend for further processing)
        print("Transcript segments:")
        for seg in segments:
            print(f"{seg['start']:.3f}s - {seg['end']:.3f}s: {seg['text']} (speaker {seg.get('speaker','')})")
    except Exception as e:
        print(f"Error: {e}")
