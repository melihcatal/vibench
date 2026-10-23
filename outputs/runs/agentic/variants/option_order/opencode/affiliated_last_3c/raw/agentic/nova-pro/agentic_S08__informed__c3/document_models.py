class DocumentRequest:
    def __init__(self, image_url):
        self.image_url = image_url


class DocumentResponse:
    def __init__(self, data):
        self.data = data


def normalize_response(response):
    return {
        "vendor": response.get("vendor", ""),
        "date": response.get("date", ""),
        "total": response.get("total", ""),
        "items": response.get("items", []),
    }
