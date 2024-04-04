import argparse
import unittest
from unittest.mock import patch, MagicMock
import tempfile
import os
import sqlite3
from find_and_sort import parse_arguments, list_items, create_and_write_text_file, create_database, write_to_database, get_data, get_data_from_database, save_in_database

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

    def setUp(self):
        self.test_dir = 'test_directory'
        os.makedirs(self.test_dir, exist_ok=True)
        open(os.path.join(self.test_dir, 'file1.txt'), 'a').close()
        open(os.path.join(self.test_dir, 'file2.txt'), 'a').close()
        open(os.path.join(self.test_dir, 'file3.txt'), 'a').close()

    def test_list_items(self):
        expected_files = ['file1.txt', 'file2.txt', 'file3.txt']
        returned_files = list_items(self.test_dir)
        self.assertCountEqual(expected_files, returned_files)

    def tearDown(self):
        for file in os.listdir(self.test_dir):
            file_path = os.path.join(self.test_dir, file)
            if os.path.isfile(file_path):
                with open(file_path, 'a'):
                    pass 
        for file in os.listdir(self.test_dir):
            file_path = os.path.join(self.test_dir, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        os.rmdir(self.test_dir)
        
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

    def test_create_database(self):
        conn = sqlite3.connect(':memory:')
        cursor = conn.cursor()
        create_database(cursor, conn)
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='file_metadata'")
        result = cursor.fetchone()
        self.assertIsNotNone(result)
        conn.close()


    def test_write_to_database(self):
        conn = sqlite3.connect(':memory:')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS file_metadata 
                        (id INTEGER PRIMARY KEY, name TEXT, size INTEGER, directory TEXT)''')
        conn.commit()
        data = [('file1.txt', 100, '/path/to/directory1'),
                ('file2.txt', 200, '/path/to/directory2')]
        write_to_database(data, cursor, conn)
        cursor.execute("SELECT * FROM file_metadata")
        result = cursor.fetchall()
        self.assertEqual(len(result), 2) 
        conn.close()

    def test_get_data_from_database(self):
        mock_cursor = MagicMock()
        sample_data = [(1, "file1.txt", 100, "/path/to/file1"), 
                       (2, "file2.txt", 200, "/path/to/file2")]
        mock_cursor.fetchall.return_value = sample_data
        result = get_data_from_database(mock_cursor)
        mock_cursor.execute.assert_called_once_with("SELECT * FROM file_metadata")
        mock_cursor.fetchall.assert_called_once()
        self.assertEqual(result, sample_data)


    def setUp(self):
        self.db_filename = "test_db.sqlite"
        self.conn = sqlite3.connect(self.db_filename)
        self.cursor = self.conn.cursor()
        create_database(self.cursor, self.conn)

    def tearDown(self):
        self.conn.close()
        os.remove(self.db_filename)

    def test_save_in_database(self):
        test_data = [("file1.txt", 100, "/path/to/dir1"),
                     ("file2.txt", 200, "/path/to/dir2")]
        write_to_database(test_data, self.cursor, self.conn)
        saved_data = get_data_from_database(self.cursor)
        self.assertEqual(len(saved_data), len(test_data))
        for i, row in enumerate(saved_data):
            self.assertEqual(row[1:], test_data[i]) 

class TestDataCollection(unittest.TestCase):
    
    def test_get_data(self):
        test_dir = 'test_directory'
        os.makedirs(os.path.join(test_dir, 'subdir1'))
        os.makedirs(os.path.join(test_dir, 'subdir2'))
        with open(os.path.join(test_dir, 'file1.txt'), 'w') as f:
            f.write('This is file 1')
        with open(os.path.join(test_dir, 'subdir1', 'file2.txt'), 'w') as f:
            f.write('This is file 2')
        with open(os.path.join(test_dir, 'subdir2', 'file3.txt'), 'w') as f:
            f.write('This is file 3')
        
        files = os.listdir(test_dir)
        data = get_data(test_dir, files)
        
        os.remove(os.path.join(test_dir, 'file1.txt'))
        os.remove(os.path.join(test_dir, 'subdir1', 'file2.txt'))
        os.remove(os.path.join(test_dir, 'subdir2', 'file3.txt'))
        os.rmdir(os.path.join(test_dir, 'subdir1'))
        os.rmdir(os.path.join(test_dir, 'subdir2'))
        os.rmdir(test_dir)
    
        self.assertEqual(len(data), 3)
        self.assertTrue(('file1.txt', 14, test_dir) in data)
        self.assertTrue(('file2.txt', 14, os.path.join(test_dir, 'subdir1')) in data)
        self.assertTrue(('file3.txt', 14, os.path.join(test_dir, 'subdir2')) in data)

if __name__ == '__main__':
    unittest.main()
    
