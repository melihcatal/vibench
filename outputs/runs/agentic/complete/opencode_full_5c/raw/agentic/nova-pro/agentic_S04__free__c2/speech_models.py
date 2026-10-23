class TranscriptionJob:
    def __init__(self, job_name, job_status, transcript):
        self.job_name = job_name
        self.job_status = job_status
        self.transcript = transcript


class TranslationResult:
    def __init__(self, translated_text):
        self.translated_text = translated_text


class SummaryResult:
    def __init__(self, summary_text):
        self.summary_text = summary_text


class SentimentResult:
    def __init__(self, sentiment):
        self.sentiment = sentiment
