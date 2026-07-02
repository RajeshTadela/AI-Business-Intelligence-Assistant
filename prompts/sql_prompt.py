from database.schema_reader import get_schema
from database.relationship_reader import infer_relationships


def build_sql_prompt(user_question: str):
    """
    Build a prompt for generating MySQL SQL.
    """

    schema = get_schema()

    schema_text = ""

    for table, columns in schema.items():

        schema_text += f"\nTable: {table}\n"

        for column_name, data_type in columns:

            schema_text += f"- {column_name} ({data_type})\n"

    # Read relationships
    relationships = infer_relationships()

    relationship_text = ""

    for t1, c1, t2, c2 in relationships:
        relationship_text += f"{t1}.{c1} -> {t2}.{c2}\n"

    prompt = f"""
You are an expert MySQL developer.

Database Schema:

{schema_text}

Relationships:

{relationship_text}

Rules:

1. Generate ONLY valid MySQL SQL.
2. Use ONLY the tables and columns listed above.
3. Use the relationships above whenever a JOIN is needed.
4. Return ONLY SQL.
5. Never explain.
6. Never use markdown.
7. If the question cannot be answered using the schema, reply exactly:
CANNOT_GENERATE_SQL

User Question:

{user_question}
"""

    return prompt


if __name__ == "__main__":
    print(build_sql_prompt("Show top 5 products by revenue."))