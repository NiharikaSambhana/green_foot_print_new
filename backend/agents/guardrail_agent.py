# backend/agents/guardrail_agent.py

import re

ALLOWED_TOPICS = {
    "carbon",
    "co2",
    "co2e",
    "sustainability",
    "green ai",
    "emission",
    "emissions",
    "energy",
    "llm",
    "token",
    "power consumption",
    "carbon footprint",
    "climate",
    "net zero"
}

BLOCKED_PATTERNS = [
    "ignore previous instructions",
    "reveal system prompt",
    "show api key",
    "developer instructions",
    "jailbreak",
    "bypass"
]



def normalize_query(query):

    return re.sub(
        r"\s+",
        " ",
        query.lower()
    ).strip()



def is_allowed_query(query):

    if not query or not query.strip():
        return False

    query = normalize_query(query)

    for pattern in BLOCKED_PATTERNS:

        if pattern in query:
            return False

    return any(
        topic in query
        for topic in ALLOWED_TOPICS
    )



def rejection_message():

    return """
This chatbot only supports:

• Carbon Footprint Analysis
• Sustainability Analytics
• Green AI
• CO2e Emission Analysis
• Energy Consumption

Please ask sustainability-related questions.
"""