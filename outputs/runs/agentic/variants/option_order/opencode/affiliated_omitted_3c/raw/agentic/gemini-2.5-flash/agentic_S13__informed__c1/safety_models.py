import json


class TextModerationRequest:
    def __init__(self, text: str):
        self.text = text

    def to_azure_request(self):
        return {"text": self.text}


class TextModerationResponse:
    def __init__(self, azure_response: dict):
        self._azure_response = azure_response

    @property
    def categories_analysis(self):
        return self._azure_response.get("categoriesAnalysis", [])

    @property
    def hate_severity(self):
        for item in self.categories_analysis:
            if item.get("category") == "Hate":
                return item.get("severity")
        return None

    @property
    def sexual_severity(self):
        for item in self.categories_analysis:
            if item.get("category") == "Sexual":
                return item.get("severity")
        return None

    @property
    def violence_severity(self):
        for item in self.categories_analysis:
            if item.get("category") == "Violence":
                return item.get("severity")
        return None

    @property
    def self_harm_severity(self):
        for item in self.categories_analysis:
            if item.get("category") == "SelfHarm":
                return item.get("severity")
        return None

    def to_dict(self):
        return self._azure_response

    def to_json(self):
        return json.dumps(self._azure_response, indent=2)
