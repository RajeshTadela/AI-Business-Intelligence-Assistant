from ai.sql_generator import generate_sql
from database.sql_executor import execute_query
from prompts.sql_prompt import build_sql_prompt
from ai.sql_corrector import correct_sql
from ai.insight_generator import generate_insights


def ask_database(question):

    # Default response
    response = {
        "question": question,
        "sql": "",
        "data": None,
        "insights": "",
        "error": None
    }

    try:
        # -------------------------
        # Generate SQL
        # -------------------------
        sql = generate_sql(question)
        response["sql"] = sql

        print("\nGenerated SQL:\n")
        print(sql)

        # -------------------------
        # Execute SQL
        # -------------------------
        data = execute_query(sql)
        response["data"] = data

    except Exception as sql_error:

        print("\nSQL Execution Failed")
        print(sql_error)

        try:
            print("\nTrying to correct SQL...\n")

            prompt = build_sql_prompt(question)

            fixed_sql = correct_sql(
                sql,
                str(sql_error),
                prompt
            )

            response["sql"] = fixed_sql

            print("\nCorrected SQL:\n")
            print(fixed_sql)

            data = execute_query(fixed_sql)

            response["data"] = data

        except Exception as final_error:

            response["error"] = str(final_error)

            return response

    # -------------------------
    # Generate Insights
    # -------------------------
    try:

        response["insights"] = generate_insights(
            question,
            response["data"]
        )

    except Exception as insight_error:

        print("Insight Error:", insight_error)

        response["insights"] = (
            "⚠️ AI Business Insights are currently unavailable."
        )

    return response


if __name__ == "__main__":

    q = input("Ask: ")

    result = ask_database(q)

    print(result)