from typing import Dict, Any, List, Optional

Document = Dict[str, Any]
Documents = List[Document]
FetchResponse = Optional[Document]
UpsertResponse = Dict[str, str]
UpdateResponse = Dict[str, str | str]
QueryResponse = Documents
