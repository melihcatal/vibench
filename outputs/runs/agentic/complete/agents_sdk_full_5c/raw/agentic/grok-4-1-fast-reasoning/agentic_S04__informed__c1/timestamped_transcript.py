import assemblyai as aai
from speech_client import configure_assemblyai

def timestamped_transcript(job_id):
    configure_assemblyai()
    transcriber = aai.Transcriber()
    transcript = transcriber.get_transcript(job_id)
    if not transcript.words:
        raise ValueError("No word timestamps available in transcript")
    timestamps = [
        {
            'start': word.start / 1000.0,
            'end': word.end / 1000.0,
            'text': word.text
        }
        for word in transcript.words
    ]
    return timestamps