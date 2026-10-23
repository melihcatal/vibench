from enum import Enum

class TranscriptionModel(Enum):
    """Supported Transcription Models for batch jobs."""
    GENERAL = 'general'  # Default model
    MEDICAL = 'medical'
    VIDEO = 'video'
    CLEANED = 'cleaned'

    @classmethod
    def get_model_name(cls, model: str):
        """Return the provider-specific model ID."""
        mapping = {
            'general': 'general',
            'medical': 'medical',
            'video': 'video',
            'cleaned': 'cleaned',
        }
        return mapping.get(model.lower(), cls.GENERAL.value)
