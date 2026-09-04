def should_escalate(issue, priority):
    high_risk_keywords = [
        "outage",
        "service down",
        "no internet",
        "no service",
        "billing dispute",
        "incorrect charge",
        "overcharged",
        "payment failed",
        "payment declined",
        "card declined",
        "unable to pay",
        "cannot pay",
        "fraud",
        "unauthorized charge",
        "data breach",
        "account compromised",
    ]

    issue = (issue or "").lower()
    priority = (priority or "").strip().lower()

    if priority == "critical":
        return True

    return any(keyword in issue for keyword in high_risk_keywords)