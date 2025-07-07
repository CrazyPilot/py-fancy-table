import unittest
from colorama import Fore
from fancy_table import FancyTable
from fancy_table.fancy_table import visible_len, center_text


class TestHelperFunctions(unittest.TestCase):
    # Test cases for visible_len and center_text functions 2
    def test_visible_len(self):
        self.assertEqual(visible_len("Hello"), 5)
        self.assertEqual(visible_len(""), 0)
        self.assertEqual(visible_len(f"{Fore.RED}Hello{Fore.RESET}"), 5)
        self.assertEqual(visible_len(f"{Fore.GREEN}Test{Fore.RESET}{Fore.BLUE}String{Fore.RESET}"), 10)
        self.assertEqual(visible_len(123), 3)
        self.assertEqual(visible_len(None), 4)
    
    def test_center_text(self):
        self.assertEqual(center_text("Hi", 6), "  Hi  ")
        self.assertEqual(center_text("Hello", 5), "Hello")
        self.assertEqual(center_text("Hi", 7), "  Hi   ")
        self.assertEqual(center_text("Text", 2), "Text")
        self.assertEqual(center_text(f"{Fore.RED}Hi{Fore.RESET}", 6), f"  {Fore.RED}Hi{Fore.RESET}  ")


class TestFancyTable(unittest.TestCase):
    def setUp(self):
        self.columns = ['Name', 'Age', 'City']
        self.table = FancyTable(self.columns)
    
    def test_table_initialization(self):
        self.assertEqual(self.table.columns, self.columns)
        self.assertEqual(self.table.rows, [])
        self.assertEqual(self.table.widths, [4, 3, 4])
        self.assertIsNone(self.table.caption)
        
        table_with_caption = FancyTable(self.columns, 'Test Table')
        self.assertEqual(table_with_caption.caption, 'Test Table')
    
    def test_add_row(self):
        row = ['Alice', 25, 'NYC']
        self.table.add_row(row)
        
        self.assertEqual(len(self.table.rows), 1)
        self.assertEqual(self.table.rows[0].row, row)
        self.assertIsNone(self.table.rows[0].color)
        self.assertEqual(self.table.widths, [5, 3, 4])
    
    def test_add_row_with_color(self):
        row = ['Bob', 30, 'LA']
        self.table.add_row(row, Fore.GREEN)
        
        self.assertEqual(self.table.rows[0].color, Fore.GREEN)
    
    def test_add_rows(self):
        rows = [
            ['Alice', 25, 'NYC'],
            ['Bob', 30, 'Los Angeles'],
            ['Charlie', 35, 'Chicago']
        ]
        self.table.add_rows(rows)
        
        self.assertEqual(len(self.table.rows), 3)
        self.assertEqual(self.table.widths, [7, 3, 11])
    
    def test_add_section(self):
        self.table.add_section('Section 1')
        self.assertEqual(len(self.table.rows), 1)
        self.assertEqual(self.table.rows[0].name, 'Section 1')
    
    def test_table_with_mixed_content(self):
        self.table.add_row(['Alice', 25, 'NYC'])
        self.table.add_section('West Coast')
        self.table.add_row(['Bob', 30, 'LA'])
        self.table.add_row(['Charlie', 35, 'SF'])
        
        self.assertEqual(len(self.table.rows), 4)
    
    def test_table_string_output(self):
        self.table.add_row(['Alice', 25, 'NYC'])
        output = str(self.table)
        
        self.assertIn('Name', output)
        self.assertIn('Age', output)
        self.assertIn('City', output)
        self.assertIn('Alice', output)
        self.assertIn('25', output)
        self.assertIn('NYC', output)
        self.assertIn('┏', output)
        self.assertIn('┗', output)
    
    def test_table_with_caption_output(self):
        table = FancyTable(['Col1', 'Col2'], 'My Caption')
        table.add_row(['A', 'B'])
        output = table.to_string()
        
        self.assertIn('My Caption', output)
    
    def test_colors_disabled(self):
        table = FancyTable(['Name', 'Age'])
        table.add_row(['Alice', 25], Fore.RED)
        
        colored_output = table.to_string(colors_enabled=True)
        plain_output = table.to_string(colors_enabled=False)
        
        self.assertIn(Fore.RED, colored_output)
        self.assertNotIn(Fore.RED, plain_output)
    
    def test_border_color(self):
        table = FancyTable(['Name', 'Age'])
        table.border_color = Fore.BLUE
        table.add_row(['Alice', 25])
        
        output = table.to_string()
        self.assertIn(Fore.BLUE, output)
    
    def test_ansi_in_cell_content(self):
        table = FancyTable(['Name', 'Status'])
        table.add_row([f"{Fore.GREEN}Alice{Fore.RESET}", f"{Fore.RED}Offline{Fore.RESET}"])
        
        output = table.to_string()
        self.assertIn('Alice', output)
        self.assertIn('Offline', output)
        self.assertEqual(table.widths, [5, 7])
    
    def test_numeric_values(self):
        table = FancyTable(['ID', 'Value'])
        table.add_row([1, 3.14159])
        table.add_row([1000, 2.5])
        
        output = table.to_string()
        self.assertIn('1', output)
        self.assertIn('3.14159', output)
        self.assertEqual(table.widths, [4, 7])
    
    def test_empty_table(self):
        table = FancyTable(['Col1', 'Col2', 'Col3'])
        output = table.to_string()
        
        self.assertIn('Col1', output)
        self.assertIn('Col2', output)
        self.assertIn('Col3', output)
        lines = output.split('\n')
        self.assertEqual(len(lines), 3)
    
    def test_section_only_table(self):
        table = FancyTable(['Name', 'Age'])
        table.add_section('Section 1')
        table.add_section('Section 2')
        
        output = table.to_string()
        self.assertIn('Section 1', output)
        self.assertIn('Section 2', output)
    
    def test_row_assertion_error(self):
        with self.assertRaises(AssertionError):
            self.table.add_row(['Alice', 25])
        
        with self.assertRaises(AssertionError):
            self.table.add_row(['Alice', 25, 'NYC', 'Extra'])


class TestEdgeCases(unittest.TestCase):
    def test_very_long_content(self):
        table = FancyTable(['Name', 'Description'])
        long_text = 'A' * 100
        table.add_row(['Item', long_text])
        
        output = table.to_string()
        self.assertIn(long_text, output)
        self.assertEqual(table.widths[1], 100)
    
    def test_unicode_content(self):
        table = FancyTable(['Name', 'Symbol'])
        table.add_row(['Heart', '❤️'])
        table.add_row(['Star', '⭐'])
        table.add_row(['Smiley', '😊'])
        
        output = table.to_string()
        self.assertIn('❤️', output)
        self.assertIn('⭐', output)
        self.assertIn('😊', output)
    
    def test_none_values(self):
        table = FancyTable(['Col1', 'Col2'])
        table.add_row([None, 'Value'])
        table.add_row(['Value', None])
        
        output = table.to_string()
        self.assertIn('None', output)
    
    def test_single_column_table(self):
        table = FancyTable(['Single'])
        table.add_row(['Value1'])
        table.add_row(['Value2'])
        
        output = table.to_string()
        self.assertIn('Single', output)
        self.assertIn('Value1', output)
        self.assertIn('Value2', output)
    
    def test_consecutive_sections(self):
        table = FancyTable(['Name', 'Value'])
        table.add_section('Section 1')
        table.add_section('Section 2')
        table.add_row(['Data', 'Value'])
        table.add_section('Section 3')
        
        output = table.to_string()
        lines = output.split('\n')
        self.assertGreater(len(lines), 10)


if __name__ == '__main__':
    unittest.main()