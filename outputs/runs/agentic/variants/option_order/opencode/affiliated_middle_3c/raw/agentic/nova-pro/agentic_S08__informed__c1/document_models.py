from pydantic import BaseModel


class Invoice(BaseModel):
    vendor: str
    date: str
    total: float
    line_items: list


class Receipt(BaseModel):
    merchant: str
    tax: float
    total: float
    items: list
