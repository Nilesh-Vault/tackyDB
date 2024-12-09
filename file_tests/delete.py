from src.DatabaseCore import DatabaseCore  # Importing DatabaseCore from src folder
db_name = "mydb"

# table_name = "users"

# delete_result = DatabaseCore.deleteTable(db_name, table_name)
# print(delete_result)


delete_result = DatabaseCore.deleteDB(db_name)

print(delete_result)