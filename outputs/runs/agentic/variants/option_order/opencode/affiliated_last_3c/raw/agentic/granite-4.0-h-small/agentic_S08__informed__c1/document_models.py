from typing import TypedDict, List, Literal

InvoiceItemType = Literal["invoice", "receipt"]


# Normalized expense schema
class NormalizedExpense(TypedDict):
    merchant_or_vendor: str
    date: str
    total: float
    items: List[dict]


# Raw provider response shape (generic)
ProviderResponse = dict

# Example local request payload for generic SDK call
RequestPayload = dict

# Mapping of field confidence requirements
FieldConfidence = dict[str, float]

# Utility helper to merge raw response with a provider‑specific model
ResponseResult = dict
