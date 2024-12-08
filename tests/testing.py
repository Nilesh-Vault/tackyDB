from src.DatabaseCore import DatabaseCore  # Importing DatabaseCore from src folder

# Create a new database
db_name = "mydb"
db_creation_result = DatabaseCore.createDatabase(db_name)
print(db_creation_result)  # Should print success or error message

# Create a new table with columns
table_name = "users"
columns = {
    "name": "str",
    "age": "int",
    "gen": "list",
    "doorkey": "bytes",
    "date": "datetime"
}
table_creation_result = DatabaseCore.createTable(db_name, table_name, columns)
print(table_creation_result)  # Should print success or error message
