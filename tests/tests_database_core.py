import os
import shutil
import unittest
from unittest.mock import patch

from src.DatabaseCore import DatabaseCore


class TestDatabaseCore(unittest.TestCase):
    def setUp(self):
        self.root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.db_path = os.path.join(self.root_path, "database")
        os.makedirs(self.db_path, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.db_path)

    def test_create_database_valid_name(self):
        db_name = "testdb1"
        result = DatabaseCore.createDatabase(db_name)
        self.assertIn("created successfully", result)
        self.assertTrue(os.path.exists(os.path.join(self.db_path, db_name.lower())))

    def test_create_database_invalid_name(self):
        db_name = "test@db"
        result = DatabaseCore.createDatabase(db_name)
        self.assertEqual(
            result,
            "Error: Database name must be alphanumeric and cannot contain special characters",
        )
        self.assertFalse(os.path.exists(os.path.join(self.db_path, db_name.lower())))

    def test_create_database_already_exists(self):
        db_name = "existingdb"
        os.makedirs(os.path.join(self.db_path, db_name.lower()), exist_ok=True)
        result = DatabaseCore.createDatabase(db_name)
        self.assertIn("created successfully", result)
        self.assertTrue(os.path.exists(os.path.join(self.db_path, db_name.lower())))

    def test_create_table_valid(self):
        db_name = "testdb2"
        os.makedirs(os.path.join(self.db_path, db_name.lower()), exist_ok=True)
        table_name = "employees"
        columns = {"id": "int", "name": "str"}
        primary_key = "id"
        result = DatabaseCore.createTable(db_name, table_name, columns, primary_key)
        table_path = os.path.join(
            self.db_path, db_name.lower(), f"{table_name.lower()}.csv"
        )
        self.assertIn("created successfully", result)
        self.assertTrue(os.path.exists(table_path))

    def test_create_table_already_exists(self):
        db_name = "testdb3"
        os.makedirs(os.path.join(self.db_path, db_name.lower()), exist_ok=True)
        table_name = "employees"
        columns = {"id": "int", "name": "str"}
        primary_key = "id"
        # First creation
        DatabaseCore.createTable(db_name, table_name, columns, primary_key)
        # Second creation attempt
        result = DatabaseCore.createTable(db_name, table_name, columns, primary_key)
        self.assertIn("already exists", result)

    def test_create_table_invalid_name(self):
        db_name = "testdb4"
        os.makedirs(os.path.join(self.db_path, db_name.lower()), exist_ok=True)
        table_name = "emp@loyees"
        columns = {"id": "int", "name": "str"}
        primary_key = "id"
        result = DatabaseCore.createTable(db_name, table_name, columns, primary_key)
        self.assertIn(
            "Error: Table name must be alphanumeric and cannot contain special characters",
            result,
        )

    def test_create_table_invalid_column_name(self):
        db_name = "testdb5"
        os.makedirs(os.path.join(self.db_path, db_name.lower()), exist_ok=True)
        table_name = "employees"
        columns = {"id": "int", "na.me": "str"}
        primary_key = "id"
        result = DatabaseCore.createTable(db_name, table_name, columns, primary_key)
        self.assertIn("Invalid Column name 'na.me'", result)

    def test_create_table_invalid_column_type(self):
        db_name = "testdb6"
        os.makedirs(os.path.join(self.db_path, db_name.lower()), exist_ok=True)
        table_name = "employees"
        columns = {"id": "integer", "name": "str"}
        primary_key = "id"
        result = DatabaseCore.createTable(db_name, table_name, columns, primary_key)
        self.assertIn("Invalid Column Type 'integer' for 'id' must be in ['int', 'float', 'complex', 'str', 'bool', 'bytes', 'list', 'date']", result)

    def test_create_table_primary_key_not_in_columns(self):
        db_name = "testdb7"
        os.makedirs(os.path.join(self.db_path, db_name.lower()), exist_ok=True)
        table_name = "employees"
        columns = {"id": "int", "name": "str"}
        primary_key = "age"
        result = DatabaseCore.createTable(db_name, table_name, columns, primary_key)
        self.assertIn("Primary Key 'age' not found", result)

    def test_delete_table_exists(self):
        db_name = "testdb8"
        os.makedirs(os.path.join(self.db_path, db_name.lower()), exist_ok=True)
        table_name = "employees"
        open(
            os.path.join(self.db_path, db_name.lower(), f"{table_name.lower()}.csv"),
            "a",
        ).close()
        result = DatabaseCore.deleteTable(db_name, table_name)
        table_path = os.path.join(
            self.db_path, db_name.lower(), f"{table_name.lower()}.csv"
        )
        self.assertIn("deleted successfully", result)
        self.assertFalse(os.path.exists(table_path))

    def test_delete_table_not_exists(self):
        db_name = "testdb9"
        os.makedirs(os.path.join(self.db_path, db_name.lower()), exist_ok=True)
        table_name = "employees"
        result = DatabaseCore.deleteTable(db_name, table_name)
        self.assertIn("does not exist", result)

    def test_delete_table_invalid_name(self):
        db_name = "testdb10"
        os.makedirs(os.path.join(self.db_path, db_name.lower()), exist_ok=True)
        table_name = "emp@loyees"
        result = DatabaseCore.deleteTable(db_name, table_name)
        self.assertIn(
            "Error: Table name must be alphanumeric and cannot contain special characters",
            result,
        )

    @patch("builtins.input", return_value="confirm_db")
    def test_delete_db_valid(self, mock_input):
        db_name = "confirm_db"
        os.makedirs(os.path.join(self.db_path, db_name.lower()), exist_ok=True)
        result = DatabaseCore.deleteDB(db_name)
        db_path = os.path.join(self.db_path, db_name.lower())
        self.assertIn("successfully deleted", result)
        self.assertFalse(os.path.exists(db_path))

    def test_delete_db_not_exists(self):
        db_name = "non_existent_db"
        result = DatabaseCore.deleteDB(db_name)
        self.assertIn("does not exist", result)

    def test_delete_db_invalid_name(self):
        db_name = "delete@db"
        result = DatabaseCore.deleteDB(db_name)
        self.assertIn("Database name must be alphanumeric and cannot contain special characters", result)

    @patch("builtins.input", return_value="wrong_confirmation")
    def test_delete_db_confirmation_mismatch(self, mock_input):
        db_name = "valid_db"
        os.makedirs(os.path.join(self.db_path, db_name.lower()), exist_ok=True)
        result = DatabaseCore.deleteDB(db_name)
        self.assertIn("Database deletion aborted", result)
        db_path = os.path.join(self.db_path, db_name.lower())
        self.assertTrue(os.path.exists(db_path))


if __name__ == "__main__":
    unittest.main()
