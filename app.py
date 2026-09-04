import logging

from src.database import get_ticket, get_customer
from src.rag import search_articles
from src.escalation import should_escalate
from src.gemini_service import generate_resolution

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MIN_RELEVANCE_SCORE = 0.65


def process_ticket(ticket_id):
    logger.info("Processing ticket %s", ticket_id)

    # Get ticket
    ticket = get_ticket(ticket_id)
    if not ticket:
        return {"error": "Ticket not found"}

    # Get customer
    customer = get_customer(ticket["customer_id"])
    if not customer:
        return {"error": "Customer not found"}

    # Search support articles
    try:
        related_articles = search_articles(ticket["issue"])
    except Exception:
        logger.exception(
            "Article retrieval failed for ticket %s",
            ticket_id
        )
        related_articles = []

    # Rule-based escalation
    try:
        rule_escalate = should_escalate(
            ticket["issue"],
            ticket["priority"]
        )
    except Exception:
        logger.exception(
            "Escalation check failed for ticket %s",
            ticket_id
        )
        rule_escalate = True

    # Retrieval confidence check
    weak_or_no_match = (
        not related_articles
        or all(
            article.get("score", 0)
            < MIN_RELEVANCE_SCORE
            for article in related_articles
        )
    )

    escalate = rule_escalate or weak_or_no_match

    logger.info(
        "Ticket %s | Articles=%d | Escalate=%s",
        ticket_id,
        len(related_articles),
        escalate
    )

    # Generate AI response
    try:
        result = generate_resolution(
            customer=customer,
            ticket=ticket,
            related_articles=related_articles,
            escalate=escalate
        )
    except Exception:
        logger.exception(
            "Resolution generation failed for ticket %s",
            ticket_id
        )

        return {
            "problem_summary": "System error",
            "resolution_or_handoff":
                "Unable to generate resolution.",
            "citations": [],
            "escalate": True
        }

    return result


if __name__ == "__main__":
    test_tickets = [
        1001,
        1002
    ]

    for ticket_id in test_tickets:
        print(
            f"\n========== RESOLVEAI RESULT "
            f"(ticket {ticket_id}) ==========\n"
        )

        result = process_ticket(ticket_id)

        print(result)