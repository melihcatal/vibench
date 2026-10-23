from typing import Dict, List


class ToxicContentResponse:
    def __init__(self, toxic_content_list: List[Dict]):
        self.toxic_content_list = toxic_content_list

    def __repr__(self):
        return f"ToxicContentResponse({self.toxic_content_list})"


def normalize_response(response):
    return ToxicContentResponse(response["ResultList"][0]["ToxicContentList"])
