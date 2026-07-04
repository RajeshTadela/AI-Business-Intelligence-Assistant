from ai.llm import ask_gemini


def generate_insights(question, dataframe):

    prompt = f"""
You are a Business Intelligence Assistant.

Question:
{question}

Result:
{dataframe.to_markdown(index=False)}

Return ONLY 3 concise bullet points.

Rules:
- Maximum 3 bullets.
- Maximum 12 words per bullet.
- No recommendations.
- No future suggestions.
- No generic advice.
- Only describe the data shown.
- Plain text only.
"""
    try:
        return ask_gemini(prompt)

    except Exception as e:
        print("Insight Generation Error:", e)
        return "⚠️ AI Business Insights are temporarily unavailable."