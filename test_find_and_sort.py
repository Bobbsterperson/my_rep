import argparse
import unittest
from unittest.mock import patch, MagicMock
import tempfile
import os
from find_and_sort_pick_db_or_txt import parse_arguments, list_items, get_directory, sorted_data, create_and_write_text_file, create_database, write_to_database, get_data, get_data_from_database

class TestParseArguments(unittest.TestCase):
    
    @patch('argparse.ArgumentParser.parse_args')
    def test_t(self, mock_parse_args):
        expected_args = argparse.Namespace(text = True,database = False)
        mock_parse_args.return_value = expected_args
        parsed_args = parse_arguments() 
        self.assertEqual(parsed_args, "text")
        
    @patch('argparse.ArgumentParser.parse_args')  
    def test_db(self, mock_parse_args):
        expected_args = argparse.Namespace(database = True,text = False)  
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

class TestTextfile(unittest.TestCase):

    def test_create_and_write_text_file(self):
        data = [("file1", 100, "dir1"), ("file2", 200, "dir2"), ("file3", 300, "dir3")]
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            temp_filename = temp_file.name    
        try:
            create_and_write_text_file(data, filename=temp_filename)
            with open(temp_filename, 'r') as file:
                content = file.read()
            expected_output = "Directory: dir1 - Name: file1 - Size: 100 bytes\n" \
                              "Directory: dir2 - Name: file2 - Size: 200 bytes\n" \
                              "Directory: dir3 - Name: file3 - Size: 300 bytes\n\n"
            self.assertEqual(content, expected_output)
        finally:
            import os
            os.unlink(temp_filename)

class TestDatabase(unittest.TestCase):

    @patch('sqlite3.connect')
    def test_create_database(self, mock_connect):
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        cursor = create_database()
        mock_cursor.execute.assert_called_once_with('''CREATE TABLE IF NOT EXISTS file_metadata 
                          (id INTEGER PRIMARY KEY, name TEXT, size INTEGER, directory TEXT)''')
        mock_connect.return_value.commit.assert_called_once()
        self.assertEqual(cursor, mock_cursor)

    def test_write_to_database(self):
        mock_cursor = MagicMock()
        data = [("file1.txt", 100, "/path/to/file1"), ("file2.txt", 200, "/path/to/file2")]
        write_to_database(data, mock_cursor)
        mock_cursor.execute.assert_any_call('''INSERT INTO file_metadata (name, size, directory) 
                              VALUES (?, ?, ?)''', ("file1.txt", 100, "/path/to/file1"))
        mock_cursor.execute.assert_any_call('''INSERT INTO file_metadata (name, size, directory) 
                              VALUES (?, ?, ?)''', ("file2.txt", 200, "/path/to/file2"))
        mock_cursor.connection.commit.assert_called_once()

    def test_get_data_from_database(self):
        mock_cursor = MagicMock()
        sample_data = [(1, "file1.txt", 100, "/path/to/file1"), 
                       (2, "file2.txt", 200, "/path/to/file2")]
        mock_cursor.fetchall.return_value = sample_data
        result = get_data_from_database(mock_cursor)
        mock_cursor.execute.assert_called_once_with("SELECT * FROM file_metadata")
        mock_cursor.fetchall.assert_called_once()
        self.assertEqual(result, sample_data)

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
    
