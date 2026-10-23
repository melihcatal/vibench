def get_transcript_info(result):
    if not hasattr(result, "channel") or not result.channel.alternatives:
        return "", False
    transcript = result.channel.alternatives[0].transcript or ""
    is_final = result.speech_final
    return transcript, is_final
