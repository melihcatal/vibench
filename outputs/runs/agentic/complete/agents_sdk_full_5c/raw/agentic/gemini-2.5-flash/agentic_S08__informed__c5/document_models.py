import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field

@dataclass
class LineItem:
    description: Optional[str] = None
    quantity: Optional[int] = None
    unit_price: Optional[float] = None
    total_price: Optional[float] = None

@dataclass
class NormalizedExpense:
    expense_type: Optional[str] = None  # e.g., "invoice", "receipt"
    date: Optional[str] = None  # YYYY-MM-DD
    vendor_name: Optional[str] = None
    merchant_name: Optional[str] = None
    total_amount: Optional[float] = None
    currency: Optional[str] = None  # e.g., "USD"
    tax_amount: Optional[float] = None
    line_items: List[LineItem] = field(default_factory=list)
    # Add original extracted data for auditing/debugging
    original_extracted_data: Dict[str, Any] = field(default_factory=dict)

    def to_json(self) -> str:
        return json.dumps(self, default=lambda o: o.__dict__, indent=2)

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'NormalizedExpense':
        line_items = [LineItem(**item) for item in data.get("line_items", [])]
        return NormalizedExpense(
            expense_type=data.get("expense_type"),
            date=data.get("date"),
            vendor_name=data.get("vendor_name"),
            merchant_name=data.get("merchant_name"),
            total_amount=data.get("total_amount"),
            currency=data.get("currency"),
            tax_amount=data.get("tax_amount"),
            line_items=line_items,
            original_extracted_data=data.get("original_extracted_data", {})
        )

@dataclass
class ValidationIssue:
    field: str
    issue_type: str
    description: str

@dataclass
class ValidationReport:
    is_valid: bool
    missing_required_fields: List[str] = field(default_factory=list)
    fields_below_min_confidence: List[str] = field(default_factory=list) # Example placeholder
    semantic_validation_issues: List[ValidationIssue] = field(default_factory=list)
    original_data: Dict[str, Any] = field(default_factory=dict)

    def to_json(self) -> str:
        # Custom serialization for list of dataclasses within the main dataclass
        report_dict = self.__dict__.copy()
        report_dict["semantic_validation_issues"] = [issue.__dict__ for issue in self.semantic_validation_issues]
        return json.dumps(report_dict, indent=2)

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'ValidationReport':
        semantic_issues = [ValidationIssue(**item) for item in data.get("semantic_validation_issues", [])]
        return ValidationReport(
            is_valid=data.get("is_valid", False),
            missing_required_fields=data.get("missing_required_fields", []),
            fields_below_min_confidence=data.get("fields_below_min_confidence", []),
            semantic_validation_issues=semantic_issues,
            original_data=data.get("original_data", {})
        )
