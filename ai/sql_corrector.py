from ai.llm import ask_gemini


def correct_sql(original_sql: str, error_message: str, schema_prompt: str) -> str:
    """
    Ask Gemini to fix an invalid SQL query.
    """

    prompt = f"""
You are an expert MySQL developer.

The following SQL query failed.

Database Schema:

{schema_prompt}

Original SQL:

{original_sql}

Database Error:

{error_message}

Instructions:
1. Fix the SQL.
2. Return ONLY valid MySQL SQL.
3. Do not explain.
4. Do not use markdown.
"""

    return ask_gemini(prompt).strip()