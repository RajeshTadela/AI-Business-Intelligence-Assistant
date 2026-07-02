from ai.llm import ask_gemini
from prompts.sql_prompt import build_sql_prompt


def generate_sql(user_question: str) -> str:
    """
    Generate SQL from a natural language question.
    """

    prompt = build_sql_prompt(user_question)

    from ai.sql_utils import clean_sql, validate_sql

    sql = ask_gemini(prompt)

    sql = clean_sql(sql)

    valid, message = validate_sql(sql)

    if not valid:
        raise ValueError(message)

    return sql


if __name__ == "__main__":

    question = input("Ask a question: ")

    sql = generate_sql(question)

    print("\nGenerated SQL:\n")
    print(sql)