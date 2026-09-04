def should_escalate(issue, priority):
    high_risk_keywords = [
        "outage",
        "billing dispute",
        "payment failed",
        "connection drops",
        "internet not working"
    ]

    issue = issue.lower()

    if priority.lower() == "high":
        return True

    for keyword in high_risk_keywords:
        if keyword in issue:
            return True

    return False