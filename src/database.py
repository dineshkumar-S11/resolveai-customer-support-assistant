import json
from pathlib import Path

DATA_DIR = Path("data")

CUSTOMERS_FILE = DATA_DIR / "customers.json"
TICKETS_FILE = DATA_DIR / "tickets.json"


def _load_json(path: Path):
    if not path.exists():
        raise FileNotFoundError(
            f"Expected data file not found: {path}"
        )

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


# Load once and cache in memory
_customers = {
    customer["customer_id"]: customer
    for customer in _load_json(CUSTOMERS_FILE)
}

_tickets = {
    ticket["ticket_id"]: ticket
    for ticket in _load_json(TICKETS_FILE)
}


def get_customer(customer_id):
    return _customers.get(customer_id)


def get_ticket(ticket_id):
    return _tickets.get(ticket_id)


def get_tickets_for_customer(customer_id):
    return [
        ticket
        for ticket in _tickets.values()
        if ticket.get("customer_id") == customer_id
    ]