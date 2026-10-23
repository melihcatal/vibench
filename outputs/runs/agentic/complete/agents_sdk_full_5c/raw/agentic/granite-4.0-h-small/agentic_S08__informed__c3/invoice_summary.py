from document_models import NormalizedExpense

def summarize_invoice(expense: NormalizedExpense) -> dict:
    summary = {
        "vendor": expense.vendor,
        "total": expense.total,
        "date": expense.date,
        "category": infer_category(expense.line_items),
        "line_items_count": len(expense.line_items)
    }
    return summary

# Simple heuristic-based categorization
CATEGORIES = {
    "food": ["restaurant", "cafe", "dinner", "meal"],
    "office_supplies": ["supply", "paper", "pen"],
    "travel": ["airfare", "hotel", "taxi", "transport"],
    "misc": []
}

def infer_category(items: List[dict]) -> str:
    tags = [item.get("description", "").lower() for item in items]
    for category, keywords in CATEGORIES.items():
        if any(k in tag for k in keywords for tag in tags):
            return category
    return CATEGORIES["misc"]
