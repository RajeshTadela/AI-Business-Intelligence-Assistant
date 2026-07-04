from database.schema_reader import get_schema
from database.relationship_reader import infer_relationships
import os


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

    # Read AI-generated business context
    business_context = ""

    if os.path.exists("cache/schema_context.txt"):
        with open("cache/schema_context.txt", "r", encoding="utf-8") as f:
            business_context = f.read()

    prompt = f"""
You are an expert MySQL SQL Engineer specializing in Business Intelligence.

Your job is to convert natural language questions into accurate, optimized, executable MySQL queries.

=========================
DATABASE SCHEMA
=========================

{schema_text}

=========================
TABLE RELATIONSHIPS
=========================

{relationship_text}

=========================
BUSINESS CONTEXT
=========================

{business_context}

=========================
SQL GENERATION RULES
=========================
1. Generate ONLY valid MySQL SQL.
2. Use ONLY the tables and columns listed in the schema.
3. Never invent tables or columns.
4. Use JOIN only when columns from multiple tables are required.
5. If all required columns exist in one table, do NOT use JOIN.
6. Prefer the simplest correct SQL.
7. Use GROUP BY only when aggregate functions are used.
8. Use ORDER BY for ranking requests (top, bottom, highest, lowest, etc.).
9. Use LIMIT when the user specifies a number.
10. Never use SELECT *.
11. Select only the required columns.
12. Return ONLY executable SQL.
13. Never explain the SQL.
14. Never wrap SQL in markdown.
15. If the question cannot be answered from the schema, return CANNOT_GENERATE_SQL.

=========================
USER QUESTION
=========================

{user_question}

Generate the SQL now.
"""

    return prompt


if __name__ == "__main__":
    print(build_sql_prompt("Show top 5 products by revenue."))