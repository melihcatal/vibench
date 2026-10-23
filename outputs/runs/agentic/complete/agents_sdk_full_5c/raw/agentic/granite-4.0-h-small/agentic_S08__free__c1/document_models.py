from pydantic import BaseModel, Field, validator

class ExpenseSchema(BaseModel):
    vendor: str = Field(..., description="Name of the vendor or merchant")
    date: str = Field(..., description="Date of the transaction, ISO format or readable")
    total: float = Field(..., gt=0, description="Total amount of the expense")
    items: list[dict] = Field(default_factory=list, description="Line items if available")

    @validator('total')
    def positive_total(cls, v):
        if v <= 0:
            raise ValueError('Total must be greater than zero')
        return v

class NormalizedExpense(BaseModel):
    """
    The single source of truth after extraction and normalization.
    """
    vendor: str = ...
    date: str = ...
    total: float = ...
    line_items: list[dict] = []

    class Config:
        extra = "allow"
