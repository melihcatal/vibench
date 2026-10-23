from typing import TypedDict, Optional, List, Dict, Any

class PlatformInput(TypedDict):
    text: str
    
class PlatformOutput(TypedDict):
    text: str
    
class PlatformMetadata(TypedDict):
    model_id: str
    response_id: str
    invocation_metrics: Optional[Dict[str, Any]]
    usage: Optional[Dict[str, Any]]

class PlatformResponse(TypedDict):
    text: str
    metadata: Optional[PlatformMetadata]
