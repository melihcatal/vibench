from typing import List, Dict
from google.cloud import translate_v2 as translate
import os


class LogMessageTranslator:
    def __init__(self):
        self.client = translate.Client()

    def translate_logs(self, log_messages: List[str], target_language: str = "es") -> List[Dict[str, str]]:
        results = []
        for message in log_messages:
            result = self.client.translate(message, target_language=target_language)
            results.append({
                "original": message,
                "translated": result["translatedText"],
                "detected_language": result["detectedSourceLanguage"],
            })
        return results


if __name__ == "__main__":
    translator = LogMessageTranslator()
    sample_logs = ["Database connection failed", "User login successful"]
    print(translator.translate_logs(sample_logs))