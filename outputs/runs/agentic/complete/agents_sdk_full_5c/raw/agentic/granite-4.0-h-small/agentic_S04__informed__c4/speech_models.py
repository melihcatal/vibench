# This helper module can be expanded to define request/response schemas,
# normalization utilities, and constants for batch speech-to-text tasks.

class TranscriptionResult(dict):
    """Normalized transcription result from various providers.
    Provides convenient access to transcript, timestamps, and speaker labels.
    """
    @staticmethod
def from_assemblyai(response: dict) -> 'TranscriptionResult':
        """Convert AssemblyAI SDK response to normalized format."""
        # AssemblyAI returns a dict with keys: 'id', 'status', 'webhook_status',
        # 'audio_url', 'duration', 'sample_rate', 'format', 'error', 'error_message',
        # 'result' (list of results, each containing 'alternatives').
        result = TranscriptionResult()
        result['transcript'] = ''
        result['timestamps'] = []
        result['speaker_labels'] = []
        for alt in response.get('result', [{}])[0].get('alternatives', []):
            result['transcript'] += alt.get('transcript', '')
            # Timestamps array contains objects: [{"word": "hello", "start": 0.0, "end": 0.5, "confidence": 0.9}]
            for t in alt.get('timestamps', []):
                result['timestamps'].append((t['word'], t['start'], t['end']))
        return result

    def pretty_print(self):
        print('Transcript:\\n' + self.get('transcript', ''))
        if self.get('timestamps'):
            print('\\nWord timestamps:')
            for w, s, e in self.get('timestamps', []):
                print(f\"{w} [{s:.2f}s-{e:.2f}s]\")
        if self.get('speaker_labels'):
            print('\\nSpeaker labels:')
            for label in self.get('speaker_labels', []):
                print(label)
