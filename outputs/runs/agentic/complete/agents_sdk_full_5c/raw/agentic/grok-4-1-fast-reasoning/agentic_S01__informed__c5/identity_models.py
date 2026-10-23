from dataclasses import dataclass
from typing import Optional

@dataclass
class UserTokens:
    access_token: str
    refresh_token: Optional[str] = None
    id_token: Optional[str] = None

@dataclass
class CodeDelivery:
    destination: str
    attribute_name: str
    delivery_medium: str
    supplier_name: Optional[str] = None