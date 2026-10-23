from typing import NamedTuple

class OcrResponse(NamedTuple):
    job_id: str
    status: str

class LayoutResponse(NamedTuple):
    job_id: str
    status: str

class TableResponse(NamedTuple):
    job_id: str
    status: str

class KeyValueCollection(NamedTuple):
    pairs: list[tuple[str, str]]
