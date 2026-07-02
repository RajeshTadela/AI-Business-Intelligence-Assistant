import re


def clean_sql(sql: str) -> str:
    """
    Remove markdown, code fences and extra spaces.
    """

    sql = sql.strip()

    # Remove ```sql
    sql = re.sub(r"^```sql", "", sql, flags=re.IGNORECASE)

    # Remove ```
    sql = re.sub(r"```$", "", sql)

    return sql.strip()


def validate_sql(sql: str):
    """
    Validate generated SQL.

    Returns:
        (True, "") if valid
        (False, reason) if invalid
    """

    sql_upper = sql.upper().strip()

    allowed = (
        "SELECT",
        "SHOW",
        "DESCRIBE",
        "WITH"
    )

    if not sql_upper.startswith(allowed):
        return False, "Only SELECT/SHOW/DESCRIBE/WITH queries are allowed."

    blocked_keywords = [
        "DROP",
        "DELETE",
        "UPDATE",
        "INSERT",
        "ALTER",
        "TRUNCATE",
        "CREATE",
        "GRANT",
        "REVOKE"
    ]

    for keyword in blocked_keywords:

        if keyword in sql_upper:

            return False, f"Blocked keyword detected: {keyword}"

    return True, ""