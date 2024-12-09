import csv
import os
import tabulate
from typing import Union, List

class Storage:
    @staticmethod
    def validation(db_name: str, table_name: str) -> str:
        root_path: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_path: str = os.path.join(root_path, f"database/{db_name.lower()}")

        if not os.path.exists(db_path):
            return f"Error: Database '{db_name}' does not exist."

        if not table_name.isalnum():
            return "Error: Table name must be alphanumeric and cannot contain special characters"

        table_path: str = os.path.join(db_path, table_name.lower() + ".csv")

        if not os.path.isfile(table_path):
            return f"Error: Table '{table_name}' does not exist in the database '{db_name}'"

        return table_path
    
    @staticmethod
    def get_column_details(db_name: str, table_name: str) -> Union[List[str], str]:
   
        validation_res: str = Storage.validation(db_name, table_name)
    
        if validation_res.startswith("Error"):
            return validation_res
        
        table_path: str = validation_res
        table_name = table_name.lower() + ".csv"

        try:
            with open(table_path, mode="r") as table:
                csv_reader = csv.reader(table)
                col_details = next(csv_reader)
                return col_details  
        except Exception as e:
            return f"Error: An unexpected error occurred - {str(e)}"

    @staticmethod
    def desc_table(db_name: str, table_name: str) -> str:
        description: Union[List[str] , str] =  Storage.get_column_details(db_name, table_name)

        if isinstance(description, str):
            return description
        
        description = tabulate(description, tablefmt="plsql")
        return description

    
    @staticmethod
    def get_all_rows(db_name: str, table_name: str) -> None:
        validation_res: str = Storage.validation(db_name, table_name)

        if validation_res.startswith("Error"):
            return validation_res
        
        table_path: str = validation_res
        table_name = table_name.lower() + ".csv"

        try:
            with open(table_path, mode="r") as table:
                csv_reader = csv.reader(table)
                rows = list(csv_reader)

                if not rows:
                    return "Error: Table is empty"
                
                tabular_output = tabulate(rows, header="firstrow", tablefmt="plsql")

                return tabular_output
        except Exception as e:
            return f"Error: An unexpected error occured - {str(e)}"


    @staticmethod
    def insert_data(db_name: str, table_name: str) -> str:
        pass

       
