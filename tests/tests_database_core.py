# AI generated tests for checking my function
import os
import unittest

from src.DatabaseCore import DatabaseCore  # Correct import for DatabaseCore


class TestDatabaseCore(unittest.TestCase):
    def setUp(self):
        # Set up test database and table names
        self.db_name = "testdb"
        self.table_name = "testtable"
        self.columns = {"name": "str", "age": "int", "birthdate": "datetime"}
        self.root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.db_path = os.path.join(self.root_path, f"database/{self.db_name.lower()}")
        self.table_path = os.path.join(self.db_path, f"{self.table_name.lower()}.csv")

    def tearDown(self):
        # Clean up: remove test files and directories after tests
        if os.path.exists(self.db_path):
            if os.path.isfile(self.table_path):
                os.remove(self.table_path)
            os.rmdir(self.db_path)  # Remove the database directory if empty

    # Tests for Database Creation
    def test_create_database_success(self):
        result = DatabaseCore.createDatabase(self.db_name)
        self.assertIn("created successfully", result)
        self.assertTrue(os.path.exists(self.db_path))

    def test_create_database_failure_alphanumeric(self):
        result = DatabaseCore.createDatabase("Invalid@DB")
        self.assertEqual(
            result,
            "Error: Database name must be alphanumeric and cannot contain special characters",
        )

    # Tests for Table Creation
    def test_create_table_success(self):
        DatabaseCore.createDatabase(self.db_name)
        result = DatabaseCore.createTable(self.db_name, self.table_name, self.columns)
        self.assertIn("created successfully", result)
        self.assertTrue(os.path.isfile(self.table_path))

    def test_create_table_failure_table_exists(self):
        DatabaseCore.createDatabase(self.db_name)
        DatabaseCore.createTable(self.db_name, self.table_name, self.columns)
        result = DatabaseCore.createTable(self.db_name, self.table_name, self.columns)
        self.assertEqual(
            result,
            f"Error: Table '{self.table_name}' already exists in database '{self.db_name}'",
        )

    def test_create_table_failure_invalid_table_name(self):
        DatabaseCore.createDatabase(self.db_name)
        result = DatabaseCore.createTable(self.db_name, "invalid@table", self.columns)
        self.assertEqual(
            result,
            "Error: Table name must be alphanumeric and cannot contain special characters",
        )

    def test_create_table_failure_invalid_column_name(self):
        DatabaseCore.createDatabase(self.db_name)
        invalid_columns = {
            "name": "str",
            "age!": "int",  # Invalid column name with a special character
        }
        result = DatabaseCore.createTable(
            self.db_name, self.table_name, invalid_columns
        )
        self.assertEqual(
            result, "Error: Invalid Column name 'age!' must be alphanumeric"
        )

    def test_create_table_failure_invalid_column_type(self):
        DatabaseCore.createDatabase(self.db_name)
        invalid_columns = {
            "name": "str",
            "age": "integer",  # Invalid type, should be 'int'
        }
        result = DatabaseCore.createTable(
            self.db_name, self.table_name, invalid_columns
        )
        self.assertEqual(
            result,
            "Error: Invalid Column Type 'integer' for 'age' must be in ['int', 'float', 'complex', 'str', 'bool', 'bytes', 'list', 'datetime']",
        )

    def test_create_table_failure_invalid_column_type_non_alpha(self):
        DatabaseCore.createDatabase(self.db_name)
        invalid_columns = {
            "name": "str",
            "age": "12345",  # Invalid column type, non-alphabetic
        }
        result = DatabaseCore.createTable(
            self.db_name, self.table_name, invalid_columns
        )
        self.assertEqual(
            result,
            "Error: Invalid Column TypeName '12345' for 'age' must be in ['int', 'float', 'complex', 'str', 'bool', 'bytes', 'list', 'datetime']",
        )

    # Tests for Table Deletion
    def test_delete_table_success(self):
        DatabaseCore.createDatabase(self.db_name)
        DatabaseCore.createTable(self.db_name, self.table_name, self.columns)
        result = DatabaseCore.deleteTable(self.db_name, self.table_name)
        self.assertIn("deleted successfully", result)
        self.assertFalse(os.path.isfile(self.table_path))  # Table should be deleted

    def test_delete_table_failure_table_not_found(self):
        DatabaseCore.createDatabase(self.db_name)
        result = DatabaseCore.deleteTable(self.db_name, self.table_name)
        self.assertEqual(
            result, f"Table '{self.table_name}' does not exist {self.db_path}'"
        )

    def test_delete_table_failure_database_not_found(self):
        result = DatabaseCore.deleteTable("nonexistent_db", self.table_name)
        self.assertEqual(result, "Error: Database 'nonexistent_db' does not exist.")

    def test_delete_table_failure_invalid_table_name(self):
        DatabaseCore.createDatabase(self.db_name)
        DatabaseCore.createTable(self.db_name, self.table_name, self.columns)
        result = DatabaseCore.deleteTable(self.db_name, "invalid@table")
        self.assertEqual(
            result,
            "Error: Table name must be alphanumeric and cannot contain special characters",
        )


if __name__ == "__main__":
    unittest.main()
