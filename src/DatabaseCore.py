import csv
import os
import shutil


class DatabaseCore:
    @staticmethod
    def createDatabase(db_name: str) -> str:
        if not db_name.isalnum():
            return "Error: Database name must be alphanumeric and cannot contain special characters"

        root_path: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_path: str = os.path.join(root_path, f"database/{db_name.lower()}")

        try:
            os.makedirs(db_path, exist_ok=True)
            if os.path.exists(db_path):
                return f"Database {db_name} created successfully at {db_path}"
            else:
                return "Error: Failed to create Database"
        except OSError as e:
            return f"Error: {str(e)}\n"

    @staticmethod
    def createTable(db_name: str, table_name: str, columns: dict) -> str:
        root_path: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_path: str = os.path.join(root_path, f"database/{db_name.lower()}")

        if not os.path.exists(db_path):
            return f"Error: Database '{db_name}' does not exist."

        if not table_name.isalnum():
            return "Error: Table name must be alphanumeric and cannot contain special characters"

        table_path = os.path.join(db_path, table_name.lower() + ".csv")

        if os.path.isfile(table_path):
            return f"Error: Table '{table_name}' already exists in database '{db_name}'"

        columns = {
            col_name.lower(): col_type.lower() for col_name, col_type in columns.items()
        }

        valid_types = [
            "int",
            "float",
            "complex",
            "str",
            "bool",
            "bytes",
            "list",
            "datetime",
        ]
        
        for column_name, column_type in columns.items():
            if not column_name.isalnum():
                return f"Error: Invalid Column name '{column_name}' must be alphanumeric"
            if not column_type.isalpha():
                return f"Error: Invalid Column TypeName '{column_type}' for '{column_name}' must be in {valid_types}"
            if column_type not in valid_types:
                return f"Error: Invalid Column Type '{column_type}' for '{column_name}' must be in {valid_types}"

        try:
            with open(table_path, "w", newline="") as file:
                writer = csv.writer(file)
                header = [
                    f"{col_name}:{col_type}" for col_name, col_type in columns.items()
                ]
                writer.writerow(header)
            return f"Table '{table_name}' created successfully at {db_path}"
        except Exception as e:
            return f"Error:Failed to create table '{table_name}\n{str(e)}\n"

    @staticmethod
    def deleteTable(db_name: str, table_name: str) -> str:
        root_path: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_path: str = os.path.join(root_path, f"database/{db_name.lower()}")

        if not os.path.exists(db_path):
            return f"Error: Database '{db_name}' does not exist."

        if not table_name.isalnum():
            return "Error: Table name must be alphanumeric and cannot contain special characters"

        table_path = os.path.join(db_path, table_name.lower() + ".csv")

        if os.path.isfile(table_path):
            os.remove(table_path)
            return f"Table '{table_name}' deleted successfully at {db_path}"
        else:
            return f"Table '{table_name}' does not exist {db_path}'"
    
    @staticmethod
    def deleteDB(db_name: str) -> str:
        root_path: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_path: str = os.path.join(root_path, f"database/{db_name.lower()}")

        if not os.path.exists(db_path):
            return f"Error: Database '{db_name}' does not exist."

        confirmation = input(f"Are you sure you want to delete the database '{db_name}'? Type '{db_name}' to confirm: ")
        if confirmation != db_name:
            return "Error: Database deletion aborted. The names do not match."

        try:
            shutil.rmtree(db_path)
            return f"Database '{db_name}' and all its contents have been successfully deleted."
        except Exception as e:
            return f"Error: Failed to delete the database '{db_name}'. {str(e)}"
