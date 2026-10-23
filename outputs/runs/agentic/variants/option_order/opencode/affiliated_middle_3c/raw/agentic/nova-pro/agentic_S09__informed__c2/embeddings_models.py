from typing import List


def create_request(texts: List[str]):
    return {"model": "text-embedding-v1", "input": texts}


def parse_response(response):
    return [item.embedding for item in response.data]
