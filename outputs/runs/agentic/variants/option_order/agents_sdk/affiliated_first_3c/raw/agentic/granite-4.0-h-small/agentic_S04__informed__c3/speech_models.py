# [HELPER] speech_models.py
import json

class TranscriptionResult:
    def __init__(self, data):
        self.data = data

    def to_dict(self):
        return self.data

    def __str__(self):
        return json.dumps(self.data, indent=2)

# Normalization helper - ensure timestamps are floats
NORMALIZED_TIME_KEY = 'time'


def normalize_timestamps(timestamps):
    normalized = []
    for seg in timestamps:
        word, start, end = seg
        normalized.append([word, float(start), float(end)])
    return normalized
