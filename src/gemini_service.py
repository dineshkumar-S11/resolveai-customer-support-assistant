from dotenv import load_dotenv
load_dotenv()

import os
import json
import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Safer model choice
model = genai.GenerativeModel("gemini-3.5-flash-lite")


def generate_resolution(customer, ticket, related_articles, escalate=False):

    # No KB match => escalate
    if not related_articles and not escalate:
        escalate = True

    articles_text = "\n\n".join(
        f"Title: {article['title']}\n"
        f"Content: {article['content']}"
        for article in related_articles
    )

    if not articles_text:
        articles_text = "No matching support articles found."

    if escalate:
        task = """
Escalation has already been determined.

Create a concise handoff summary for a human support agent.

Include:
- Customer details
- Issue reported
- Priority level
- Current status
- Relevant findings

Do NOT provide a solution.
"""
    else:
        task = """
Provide a customer support resolution using ONLY the support articles provided.

Rules:
- Do not invent information.
- Cite article titles used.
- If information is missing, explicitly say so.
"""

    prompt = f"""
You are ResolveAI, an AI customer support assistant.

Customer Information:
Name: {customer.get('name')}
Plan: {customer.get('plan')}
Status: {customer.get('status')}
Billing Status: {customer.get('billing_status')}

Ticket Information:
Issue: {ticket.get('issue')}
Priority: {ticket.get('priority')}
Status: {ticket.get('status')}

Relevant Support Articles:
{articles_text}

Task:
{task}

Return ONLY valid JSON.

Required JSON format:

{{
    "problem_summary": "",
    "resolution_or_handoff": "",
    "citations": [],
    "escalate": {str(escalate).lower()}
}}
"""

    try:
        response = model.generate_content(prompt)

    except Exception as e:
        return {
            "problem_summary": "Unable to generate response",
            "resolution_or_handoff": f"Gemini API error: {e}",
            "citations": [],
            "escalate": True
        }

    try:
        return json.loads(response.text)

    except Exception:
        return {
            "problem_summary": "Model returned invalid JSON",
            "resolution_or_handoff": getattr(response, "text", ""),
            "citations": [],
            "escalate": True
        }