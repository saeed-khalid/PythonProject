import unittest
import csv
import io
from Password import (
    add_password,
    get_password,
    update_password,
    delete_password,
    generate_password,
)

class TestPasswordManager(unittest.TestCase):
    def test_get_password(self):
        # Create a test CSV file in memory
        test_csv = io.StringIO()
        writer = csv.writer(test_csv)
        writer.writerow(["service", "username", "password"])
        writer.writerow(["test_service", "test_username", "test_password"])

        # Test getting a password
        self.assertEqual(get_password(test_csv, "test_service"), ["test_username", "test_password"])

    def test_update_password(self):
        # Create a test CSV file in memory
        test_csv = io.StringIO()
        writer = csv.writer(test_csv)
        writer.writerow(["service", "username", "password"])
        writer.writerow(["test_service", "test_username", "test_password"])

        # Test updating a password
        update_password(test_csv, "test_service", "new_username", "new_password")

        # Rewind the file pointer to the beginning of the file
        test_csv.seek(0)

        # Read the contents of the file and compare it to the expected value
        self.assertEqual(test_csv.read().decode(), "service,username,password\ntest_service,new_username,new_password\n")

    def test_delete_password(self):
        # Create a test CSV file in memory
        test_csv = io.StringIO()
        writer = csv.writer(test_csv)
        writer.writerow(["service", "username", "password"])
        writer.writerow(["test_service", "test_username", "test_password"])

        # Test deleting a password
        delete_password(test_csv, "test_service")

        # Rewind the file pointer to the beginning of the file
        test_csv.seek(0)

        # Read the contents of the file and compare it to the expected value
        self.assertEqual(test_csv.read().decode(), "service,username,password\n")

    def test_generate_password(self):
        # Test generating a password
        self.assertTrue(generate_password().isalnum())

if __name__ == "__main__":
    unittest.main()