import argparse
import unittest
import sqlite3
import os
from unittest.mock import patch, MagicMock

from find_and_sort import parse_arguments
from find_and_sort import list_items
from find_and_sort import get_directory
from find_and_sort import sorted_data
from find_and_sort import create_and_write_text_file
from find_and_sort import create_database
from find_and_sort import write_to_database
from find_and_sort import get_data
from find_and_sort import get_data_from_database

class TestParseArguments(unittest.TestCase):
    @patch('argparse.ArgumentParser.parse_args')
    def test_t(self, mock_parse_args):
        expected_args = argparse.Namespace(text = True,database = False)
        mock_parse_args.return_value = expected_args
        parsed_args = parse_arguments() 
        self.assertEqual(parsed_args, "text")

    @patch('argparse.ArgumentParser.parse_args')  #patches parse_args() from ArgumentParser class from argparse module
    def test_db(self, mock_parse_args):
        expected_args = argparse.Namespace(database = True,text = False)  # Nenespace is a placeholder for parsed arguments in terminal
        mock_parse_args.return_value = expected_args
        parsed_args = parse_arguments()
        self.assertEqual(parsed_args, "database")   

    @patch('argparse.ArgumentParser.parse_args')
    def test_no_argument(self, mock_parse_args):
        expected_args = argparse.Namespace(text = False,database = False)
        mock_parse_args.return_value = expected_args
        try:
            parsed_args = parse_arguments() 
        except SystemExit as e:
            self.assertEqual(e.code,2)


class TestListItems(unittest.TestCase):
    @patch('os.listdir')
    def test_lst_itm(self, mock_listdir):
        expected_result = "get_directory(),os.listdir" # if i put this line after = in ("") it still works...
        mock_listdir.return_value = expected_result
        result = list_items(os.listdir)
        self.assertEqual(result, expected_result)

class TestGetDirectory(unittest.TestCase):
    def test_get_directory(self):
        result = get_directory()
        expected_result = os.getcwd()
        self.assertEqual(result, expected_result)

class TestSortedData(unittest.TestCase):
    def test_sorted_data(self):
        unsorted_data = [('txt', 3), ('filename', 2), ('file', 1)]
        result = sorted_data(unsorted_data)
        expected_result = [('file', 1), ('filename', 2), ('txt', 3)]
        self.assertEqual(result, expected_result)

class TestTextfile(unittest.TestCase):
    def test_create_and_write_text_file(self):
        
        test_data = [
            ("file1.txt", 100, "/path/to/directory1"),
            ("file2.txt", 200, "/path/to/directory2"),
            ("file3.txt", 300, "/path/to/directory3")
        ]

        create_and_write_text_file(test_data)

        with open('sorted_metadata.txt', 'r') as file:
            content = file.read()

        self.assertIn("Directory: /path/to/directory1 - Name: file1.txt - Size: 100 bytes", content)
        self.assertIn("Directory: /path/to/directory2 - Name: file2.txt - Size: 200 bytes", content)
        self.assertIn("Directory: /path/to/directory3 - Name: file3.txt - Size: 300 bytes", content)

class TestDatabaseFunctions(unittest.TestCase):
    def setUp(self):
        if os.path.exists("sqlite.db"):
            os.remove("sqlite.db")

    def test_create_database(self):
        cursor = create_database()
        self.assertTrue(os.path.exists("sqlite.db"))
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='file_metadata'")
        result = cursor.fetchone()
        self.assertIsNotNone(result)

    def test_data_insertion(self):
        data = [("file1.txt", 100, "/path/to/directory1"),
                ("file2.txt", 200, "/path/to/directory2")]
        cursor = create_database()
        write_to_database(data, cursor)
        cursor.execute("SELECT * FROM file_metadata")
        result = cursor.fetchall()
        self.assertEqual(len(result), len(data))

    @patch('find_and_sort_pick_db_or_txt.sqlite3.connect')
    def test_data_retrieval(self, mock_connect):
        data = [("file1.txt", 100, "/path/to/directory1"),
                ("file2.txt", 200, "/path/to/directory2")]
        mock_cursor = mock_connect.return_value.cursor.return_value
        mock_cursor.fetchall.return_value = data
        result = get_data_from_database(mock_cursor)
        self.assertEqual(result, data)

class TestGetData(unittest.TestCase):
    @patch("find_and_sort_pick_db_or_txt.os")
    def test_get_data(self, mock_os):
        mock_os.path.join.side_effect = lambda *args: "/".join(args)
        mock_os.path.isdir.side_effect = lambda path: path.endswith("dir1") or path.endswith("dir2")
        mock_os.stat.side_effect = lambda *args, **kwargs: MagicMock(st_size=100) if args[0].endswith("file1.txt") else MagicMock(st_size=200)
        mock_os.path.basename.side_effect = lambda path: path.split("/")[-1]

        directory = "/path/to/directory"
        files = ["file1.txt", "file2.txt", "dir1", "dir2"]
        result = get_data(directory, files)

        expected_result = [
            ("file1.txt", 100, "/path/to/directory"),
            ("file2.txt", 200, "/path/to/directory")
        ]

        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()
    
