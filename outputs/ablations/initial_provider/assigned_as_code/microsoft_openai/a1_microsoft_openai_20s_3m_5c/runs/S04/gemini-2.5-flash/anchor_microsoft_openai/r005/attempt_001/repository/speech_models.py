class TranscriptionRequest:
    def __init__(self, audio_uri, language_code, display_name="transcription", diarization_enabled=False, word_level_timestamps_enabled=True):
        self.audio_uri = audio_uri
        self.language_code = language_code
        self.display_name = display_name
        self.diarization_enabled = diarization_enabled
        self.word_level_timestamps_enabled = word_level_timestamps_enabled

    def to_json(self):
        return {
            'displayName': self.display_name,
            'locale': self.language_code,
            'contentUrls': [self.audio_uri],
            'properties': {
                'diarizationEnabled': self.diarization_enabled,
                'wordLevelTimestampsEnabled': self.word_level_timestamps_enabled
            }
        }


class TranscriptionResult:
    def __init__(self, raw_result):
        self.raw_result = raw_result
        self.status = raw_result.get('status')
        self.job_id = raw_result.get('self')
        self.display_name = raw_result.get('displayName')
        self.locale = raw_result.get('locale')

    def get_transcript_text(self):
        # This is a simplified example. Actual parsing would be more complex
        # depending on the structure of the Azure Speech-to-Text output JSON.
        # Assuming a structure where 'combinedRecognizedPhrases' is available
        # in the content URL result for a simple text representation.
        # For word-level timestamps and diarization, a more detailed parse would be needed.
        if self.raw_result and 'combinedRecognizedPhrases' in self.raw_result:
            return " ".join([phrase['display'] for phrase in self.raw_result['combinedRecognizedPhrases']])
        return None

    def get_word_timestamps(self):
        # Placeholder for extracting word-level timestamps
        # This would require detailed parsing of the 'segments' or 'recognizedPhrases'
        # arrays from the content URL result if word-level timestamps were enabled.
        if self.raw_result and 'recognizedPhrases' in self.raw_result:
            timestamps = []
            for phrase in self.raw_result['recognizedPhrases']:
                for word in phrase.get('words', []):
                    timestamps.append({
                        'word': word['word'],
                        'offset': word['offset'],
                        'duration': word['duration']
                    })
            return timestamps
        return None

    def get_diarization_speakers(self):
        # Placeholder for extracting speaker diarization information
        # This would involve iterating through segments and their speaker IDs.
        if self.raw_result and 'recognizedPhrases' in self.raw_result:
            speakers = {}
            for phrase in self.raw_result['recognizedPhrases']:
                if 'speaker' in phrase:
                    speaker_id = phrase['speaker']
                    if speaker_id not in speakers:
                        speakers[speaker_id] = []
                    speakers[speaker_id].append(phrase['display'])
            return speakers
        return None
