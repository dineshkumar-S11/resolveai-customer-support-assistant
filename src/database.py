import json

CUSTOMERS_FILE = "data/customers.json"
TICKETS_FILE = "data/tickets.json"


def load_customers():
    with open(CUSTOMERS_FILE, "r") as file:
        return json.load(file)


def load_tickets():
    with open(TICKETS_FILE, "r") as file:
        return json.load(file)


def get_customer(customer_id):
    customers = load_customers()

    for customer in customers:
        if customer["customer_id"] == customer_id:
            return customer

    return None


def get_ticket(ticket_id):
    tickets = load_tickets()

    for ticket in tickets:
        if ticket["ticket_id"] == ticket_id:
            return ticket

    return None