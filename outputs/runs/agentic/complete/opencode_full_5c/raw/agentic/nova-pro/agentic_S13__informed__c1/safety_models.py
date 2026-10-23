class SafetyRequest:
    def __init__(self, text):
        self.text = text


class SafetyResponse:
    def __init__(self, toxic_content_items):
        self.toxic_content_items = toxic_content_items


def normalize_response(response):
    toxic_content_items = response["ToxicContentItems"]
    return SafetyResponse(toxic_content_items)
