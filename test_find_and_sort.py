import argparse
import unittest
from unittest.mock import patch
from find_and_sort_pick_db_or_txt import parse_arguments
from find_and_sort_pick_db_or_txt import list_items
import os
from find_and_sort_pick_db_or_txt import get_directory

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


if __name__ == '__main__':
    unittest.main()
    
    

