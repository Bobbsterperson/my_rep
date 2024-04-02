import argparse
import unittest
from unittest.mock import patch
from find_and_sort_pick_db_or_txt import parse_arguments


class TestParseArguments(unittest.TestCase):
    

    @patch('argparse.ArgumentParser.parse_args')  #patches parse_args() from ArgumentParser class from argparse module
    def test_db(self, mock_parse_args):


        expected_args = argparse.Namespace(db='-db')  # Nenespace is a placeholder for parsed arguments in terminal
        mock_parse_args.return_value = expected_args
        parsed_args = parse_arguments()
        self.assertEqual(parsed_args, expected_args)
        if parsed_args.db == expected_args.db:
            print("Test for -db: Passed")
        else:
            print("Test for -db: Failed")


    @patch('argparse.ArgumentParser.parse_args')
    def test_t_flag(self, mock_parse_args):
        

        expected_args = argparse.Namespace(t='-t')
        mock_parse_args.return_value = expected_args
        parsed_args = parse_arguments()
        self.assertEqual(parsed_args, expected_args)
        if parsed_args.t == expected_args.t:
            print("Test for -t flag: Passed")
        else:
            print("Test for -t flag: Failed")


    if __name__ == '__main__':
        unittest.main()
