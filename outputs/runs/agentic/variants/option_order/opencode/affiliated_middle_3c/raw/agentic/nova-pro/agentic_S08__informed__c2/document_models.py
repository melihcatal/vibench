class DocumentRequest:
    def __init__(self, file_path):
        self.file_path = file_path


class DocumentResponse:
    def __init__(self, data):
        self.data = data


def normalize_response(response):
    return {
        "vendor": response.get("vendor", ""),
        "date": response.get("date", ""),
        "total": response.get("total", ""),
        "line_items": response.get("line_items", []),
    }
