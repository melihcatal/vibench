import speech_client

def meeting_summary(transcripts):
    summary = ' '.join(transcripts)
    return summary