from ai.sql_generator import generate_sql
from database.sql_executor import execute_query
from prompts.sql_prompt import build_sql_prompt
from ai.sql_corrector import correct_sql


def ask_database(question):

    sql = generate_sql(question)

    print("\nGenerated SQL:\n")
    print(sql)

    try:

        result = execute_query(sql)

        return result

    except Exception as e:

        print("\nSQL Failed")
        print(e)

        print("\nTrying to fix SQL...\n")

        prompt = build_sql_prompt(question)

        fixed_sql = correct_sql(sql, str(e), prompt)

        print("Corrected SQL:\n")
        print(fixed_sql)

        result = execute_query(fixed_sql)

        return result


if __name__ == "__main__":

    question = input("Ask: ")

    df = ask_database(question)

    print(df)