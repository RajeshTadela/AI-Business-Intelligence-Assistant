from database.schema_reader import get_schema


def infer_relationships():
    """
    Infer relationships based on matching column names.
    """

    schema = get_schema()

    relationships = []

    tables = list(schema.keys())

    for i in range(len(tables)):
        table1 = tables[i]

        cols1 = [col[0].lower() for col in schema[table1]]

        for j in range(i + 1, len(tables)):
            table2 = tables[j]

            cols2 = [col[0].lower() for col in schema[table2]]

            common = set(cols1) & set(cols2)

            for column in common:

                relationships.append(
                    (table1, column, table2, column)
                )

    return relationships


if __name__ == "__main__":

    relationships = infer_relationships()

    for rel in relationships:
        print(rel)