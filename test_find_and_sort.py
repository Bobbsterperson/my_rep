import argparse
import unittest
from unittest.mock import patch
from find_and_sort_pick_db_or_txt import parse_arguments
from find_and_sort_pick_db_or_txt import list_items
import os
from find_and_sort_pick_db_or_txt import get_directory
from find_and_sort_pick_db_or_txt import sorted_data
from find_and_sort_pick_db_or_txt import create_and_write_text_file
from find_and_sort_pick_db_or_txt import create_and_write_to_database
import sqlite3
from unittest.mock import patch, MagicMock
from find_and_sort_pick_db_or_txt import get_data

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
        expected_result = get_directory(),os.listdir # if i put this line after = in ("") it still works...
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

        print(content)

        self.assertIn("Directory: /path/to/directory1 - Name: file1.txt - Size: 100 bytes", content)
        self.assertIn("Directory: /path/to/directory2 - Name: file2.txt - Size: 200 bytes", content)
        self.assertIn("Directory: /path/to/directory3 - Name: file3.txt - Size: 300 bytes", content)


class TestDatabase(unittest.TestCase):

    
    def setUp(self):       
        self.conn = sqlite3.connect(":memory:")  # Use in-memory database
        self.cursor = self.conn.cursor()

    def tearDown(self):
        self.cursor.close()
        self.conn.close()

    # def test_data_insertion(self):
    #     test_data = [("file1.txt", 100, "/path/to/dir1"),
    #                  ("file2.txt", 200, "/path/to/dir2")]

    #     create_and_write_to_database(test_data)

    #     self.cursor.execute("SELECT * FROM file_metadata")
    #     result = self.cursor.fetchall()

    #     self.assertEqual(len(result), len(test_data))

    #     for item in test_data:
    #         self.assertIn(item, result)


    def test_schema_creation(self):

        create_and_write_to_database([])  # No data is needed for this test

        self.cursor.execute("PRAGMA table_info(file_metadata)")
        schema = self.cursor.fetchall()

        expected_columns = [("id", "INTEGER", 0, None, 1),
                            ("name", "TEXT", 0, None, 0),
                            ("size", "INTEGER", 0, None, 0),
                            ("directory", "TEXT", 0, None, 0)]


        for expected_column, actual_column in zip(expected_columns, schema):
            self.assertEqual(expected_column, actual_column[:4])


class TestGetData(unittest.TestCase):

    @patch("find_and_sort_pick_db_or_txt.os")
    def test_get_data(self, mock_os):
        self.mock_os = mock_os
        self.setup_mock_os()
        directory = "/path/to/directory"
        files = ["file1.txt", "file2.txt", "dir1", "dir2"]
        result = get_data(directory, files)
        expected_result = [
            ("file1.txt", 100, "/path/to/directory"),
            ("file2.txt", 200, "/path/to/directory")
        ]
        self.assertEqual(result, expected_result)

    def setup_mock_os(self):
        self.mock_os.path.join.side_effect = self.fake_path_join
        self.mock_os.path.isdir.side_effect = self.fake_isdir
        self.mock_os.stat.side_effect = self.fake_stat

    def fake_path_join(self, *args):
        return "/".join(args)
    
    def fake_isdir(self, path):
        return path.endswith("dir1") or path.endswith("dir2")
    
    def fake_stat(self, *args, **kwargs):
        if len(args) == 1:  
            return MagicMock(st_size=100) if args[0].endswith("file1.txt") else MagicMock(st_size=200)
        return MagicMock()  


if __name__ == '__main__':
    unittest.main()
    