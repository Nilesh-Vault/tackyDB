from src.DatabaseCore import DatabaseCore

db_name = "mydb"
db_creation_result = DatabaseCore.createDatabase(db_name)
print(db_creation_result)  # Should print success or error message

table_name = "users"
columns = {
    "id": "int",
    "name": "str",
    "age": "int",
    "gen": "list",
    "doorkey": "bytes",
    "date": "date",
}
primary_key = "id"

# Assuming createTable method can handle list of column dictionaries
table_creation_result = DatabaseCore.createTable(
    db_name, table_name, columns, primary_key
)
print(table_creation_result)  # Should print success or error message
