from ai.llm import ask_gemini


def analyze_schema(schema: str, relationships: str):
    prompt = f"""
You are an expert Data Analyst.

Below is a database schema.

Your job is to understand the database.

Schema:
{schema}

Relationships:
{relationships}

Return:

1. What this database is about.
2. Meaning of every table.
3. Meaning of important columns.
4. Important business rules.
5. Things an SQL generator should know.

Return only plain text.
"""

    return ask_gemini(prompt)


if __name__ == "__main__":

    from database.schema_reader import get_schema
    from database.relationship_reader import infer_relationships

    schema = get_schema()

    schema_text = ""

    for table, columns in schema.items():
        schema_text += f"\nTable: {table}\n"

        for col in columns:
            schema_text += f"- {col[0]}\n"

    relationships = infer_relationships()

    rel_text = ""

    for r in relationships:
        rel_text += f"{r[0]}.{r[1]} -> {r[2]}.{r[3]}\n"

    context = analyze_schema(schema_text, rel_text)

    with open("cache/schema_context.txt", "w", encoding="utf-8") as f:
        f.write(context)

    print("✅ Schema context saved.")