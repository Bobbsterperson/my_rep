import argparse
import unittest
from unittest.mock import patch
from find_and_sort_pick_db_or_txt import parse_arguments
from find_and_sort_pick_db_or_txt import list_items
import os
from find_and_sort_pick_db_or_txt import get_directory
from find_and_sort_pick_db_or_txt import sorted_data
from find_and_sort_pick_db_or_txt import create_and_write_text_file


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
        expected_result = get_directory(),os.listdir
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

    
class testTextfile(unittest.TestCase):


    def write_metadata_to_file(self, file_path, data):
        with open(file_path, 'w') as file:
            for item in data:
                file.write(f"Directory: {item[2]} - Name: {item[0]} - Size: {item[1]} bytes\n")
            file.write("\n")

    test_data = [
    ("file1.txt", 100, "/path/to/directory1"),
    ("file2.txt", 200, "/path/to/directory2"),
    ("file3.txt", 300, "/path/to/directory3")
]

    create_and_write_text_file(test_data)

    with open('sorted_metadata.txt', 'r') as file:
        content = file.read()
        print(content)


if __name__ == '__main__':
    unittest.main()
    