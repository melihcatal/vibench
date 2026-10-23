from typing import Dict, Any, Optional, List

Document = Dict[str, Any]
Documents = List[Document]

def prepare_upsert_item(identifier: str, document: Dict[str, Any]) -> Dict[str, Any]:
    item = document.copy()
    item['id'] = identifier
    if 'version' not in item:
        item['version'] = 0
    return item

def parse_fetched_item(item: Optional[Dict[str, Any]]) -> Optional[Document]:
    return item