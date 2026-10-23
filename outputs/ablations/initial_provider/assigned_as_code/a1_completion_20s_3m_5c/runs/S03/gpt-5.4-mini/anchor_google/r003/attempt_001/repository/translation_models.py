from dataclasses import dataclass


def normalize_language_code(value):
    return str(value).strip().replace("_", "-").lower()


def normalize_text(value):
    return "" if value is None else str(value)


def normalize_text_list(values):
    return [normalize_text(value) for value in values]


def normalize_mapping_values(data):
    return {key: normalize_text(value) for key, value in data.items()}


@dataclass
class TranslationRequest:
    text: str
    source_language: str
    target_language: str

    def normalized(self):
        return {
            "text": normalize_text(self.text),
            "source_language": normalize_language_code(self.source_language),
            "target_language": normalize_language_code(self.target_language),
        }


@dataclass
class TranslationResponse:
    text: str
    source_language: str
    target_language: str

    def as_dict(self):
        return {
            "text": normalize_text(self.text),
            "source_language": normalize_language_code(self.source_language),
            "target_language": normalize_language_code(self.target_language),
        }
