class DocumentRequest:
    def __init__(self, document):
        self.document = document


class DocumentResponse:
    def __init__(self, response):
        self.response = response


def normalize_response(response):
    normalized_response = {"vendor": "", "date": "", "total": "", "line_items": []}
    for block in response["Blocks"]:
        if block["BlockType"] == "KEY_VALUE_SET":
            if block["Text"] == "Vendor":
                normalized_response["vendor"] = block["ValueDetection"]["Text"]
            elif block["Text"] == "Date":
                normalized_response["date"] = block["ValueDetection"]["Text"]
            elif block["Text"] == "Total":
                normalized_response["total"] = block["ValueDetection"]["Text"]
        elif block["BlockType"] == "TABLE":
            for cell in block["Relationships"][0]["Ids"]:
                cell_block = next(b for b in response["Blocks"] if b["Id"] == cell)
                if cell_block["BlockType"] == "CELL":
                    normalized_response["line_items"].append(cell_block["Text"])
    return normalized_response
