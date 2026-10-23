def normalize_request(audio_file_path, diarization=False, with_timestamps=False):
    return {
        "audio_file_path": audio_file_path,
        "diarization": diarization,
        "with_timestamps": with_timestamps,
    }


def parse_response(response):
    return response
