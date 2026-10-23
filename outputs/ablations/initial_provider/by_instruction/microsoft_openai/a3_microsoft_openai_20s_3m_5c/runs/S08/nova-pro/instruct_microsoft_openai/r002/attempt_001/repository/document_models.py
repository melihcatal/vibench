from dataclasses import dataclass

@dataclass
class Expense:
    vendor: str
    date: str
    total: float
    items: list

    def to_json(self):
        return {
            "vendor": self.vendor,
            "date": self.date,
            "total": self.total,
            "items": self.items
        }