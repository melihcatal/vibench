# This file can be used to define local request/response models or normalization helpers.
# For boto3, direct dictionary usage is common and often sufficient.
# No specific models are defined here for the current Transcribe use case,
# but it serves as a placeholder for future extensions or complex data transformations.


class TranscriptionJobRequest:
    def __init__(
        self,
        job_name: str,
        media_file_uri: str,
        output_bucket_name: str,
        language_code: str = "en-US",
        enable_diarization: bool = False,
        show_speaker_labels: bool = False,
        show_alternatives: bool = False,
        max_speakers: int = 2,
        enable_word_level_timestamps: bool = False,
    ):
        self.job_name = job_name
        self.media_file_uri = media_file_uri
        self.output_bucket_name = output_bucket_name
        self.language_code = language_code
        self.enable_diarization = enable_diarization
        self.show_speaker_labels = show_speaker_labels
        self.show_alternatives = show_alternatives
        self.max_speakers = max_speakers
        self.enable_word_level_timestamps = enable_word_level_timestamps

    def to_start_transcription_job_params(self):
        params = {
            "TranscriptionJobName": self.job_name,
            "LanguageCode": self.language_code,
            "MediaFormat": self.media_file_uri.split(".")[
                -1
            ],  # Infer media format from URI
            "Media": {"MediaFileUri": self.media_file_uri},
            "OutputBucketName": self.output_bucket_name,
        }
        if self.enable_diarization:
            params["Settings"] = {
                "ShowSpeakerLabels": True,
                "MaxSpeakerLabels": self.max_speakers,
            }
        if self.enable_word_level_timestamps:
            if "Settings" not in params:
                params["Settings"] = {}
            params["Settings"]["ShowAlternatives"] = True
            params["Settings"]["MaxAlternatives"] = (
                1  # We only care about the primary transcript
            )
            params["Settings"]["ChannelIdentification"] = (
                False  # Not relevant for word-level timestamps
            )

        return params


class TranscriptionJobResult:
    def __init__(
        self,
        job_status: str,
        transcript_uri: str = None,
        transcript_text: str = None,
        diarized_segments: list = None,
        timestamped_words: list = None,
    ):
        self.job_status = job_status
        self.transcript_uri = transcript_uri
        self.transcript_text = transcript_text
        self.diarized_segments = diarized_segments
        self.timestamped_words = timestamped_words

    @classmethod
    def from_get_transcription_job_response(cls, response: dict):
        job_status = response["TranscriptionJob"]["TranscriptionJobStatus"]
        transcript_uri = None
        if "Transcript" in response["TranscriptionJob"]:
            transcript_uri = response["TranscriptionJob"]["Transcript"][
                "TranscriptFileUri"
            ]

        return cls(job_status=job_status, transcript_uri=transcript_uri)

    def parse_full_transcript_json(self, transcript_json: dict):
        self.transcript_text = transcript_json["results"]["transcripts"][0][
            "transcript"
        ]

        if "speaker_labels" in transcript_json["results"]:
            self.diarized_segments = []
            current_speaker = None
            current_text = ""
            start_time = None

            items = transcript_json["results"]["items"]
            for item in items:
                if item["type"] == "pronunciation":
                    speaker = item["speaker_label"]
                    word_start_time = float(item["start_time"])
                    word_end_time = float(item["end_time"])
                    content = item["alternatives"][0]["content"]

                    if current_speaker is None:
                        current_speaker = speaker
                        start_time = word_start_time
                        current_text = content
                    elif speaker == current_speaker:
                        current_text += " " + content
                    else:
                        self.diarized_segments.append(
                            {
                                "speaker": current_speaker,
                                "start_time": start_time,
                                "end_time": float(
                                    items[items.index(item) - 1]["end_time"]
                                ),  # End of previous speaker's last word
                                "text": current_text.strip(),
                            }
                        )
                        current_speaker = speaker
                        start_time = word_start_time
                        current_text = content

            if current_speaker is not None:
                self.diarized_segments.append(
                    {
                        "speaker": current_speaker,
                        "start_time": start_time,
                        "end_time": float(
                            items[-1]["end_time"]
                        ),  # End of last word in transcript
                        "text": current_text.strip(),
                    }
                )

        if "items" in transcript_json["results"]:
            self.timestamped_words = []
            for item in transcript_json["results"]["items"]:
                if item["type"] == "pronunciation":
                    self.timestamped_words.append(
                        {
                            "word": item["alternatives"][0]["content"],
                            "start_time": float(item["start_time"]),
                            "end_time": float(item["end_time"]),
                        }
                    )
