import os
import assemblyai as aai

class SpeechClient:
    """
    Provides a configured AssemblyAI client instance.
    """
    def __init__(self):
        self._api_key = os.getenv("ASSEMBLYAI_API_KEY")
        if not self._api_key:
            raise ValueError("ASSEMBLYAI_API_KEY environment variable not set.")
        aai.settings.api_key = self._api_key
        self._transcriber = aai.Transcriber()

    def get_transcriber(self) -> aai.Transcriber:
        """
        Returns a configured AssemblyAI Transcriber instance.
        """
        return self._transcriber

    @staticmethod
    def create_transcription_config(
        language_code: str = "en_us",
        speaker_labels: bool = False,
        word_timestamps: bool = False
    ) -> aai.TranscriptionConfig:
        """
        Creates an AssemblyAI TranscriptionConfig object.
        """
        return aai.TranscriptionConfig(
            language_code=language_code,
            speaker_labels=speaker_labels,
            word_timestamps=word_timestamps
        )

if __name__ == "__main__":
    # Example of how to use the client
    # try:
    #     client = SpeechClient()
    #     transcriber = client.get_transcriber()
    #     print("AssemblyAI client initialized successfully.")
    #     # config = client.create_transcription_config(speaker_labels=True)
    #     # print(config)
    # except ValueError as e:
    #     print(f"Error initializing SpeechClient: {e}")
    pass