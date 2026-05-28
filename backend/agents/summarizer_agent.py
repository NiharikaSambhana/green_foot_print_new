# backend/agents/summarizer_agent.py


def summarize_response(
    response,
    evaluation,
    sources
):

    recommendations = [
        "Reduce token usage",
        "Enable response caching",
        "Use efficient LLM models"
    ]

    formatted_sources = "\n".join([
        f"• {source}"
        for source in sources
    ])

    return f"""
SUSTAINABILITY ANALYSIS REPORT

Summary:
{response}

Confidence Metrics:

• Accuracy: {evaluation.get('accuracy')}/10
• Relevance: {evaluation.get('relevance')}/10
• Groundedness: {evaluation.get('groundedness')}/10
• Hallucination Detected: {evaluation.get('hallucination_detected')}

Recommendations:

{chr(10).join([f'• {r}' for r in recommendations])}

Sources:

{formatted_sources}
"""