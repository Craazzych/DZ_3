import unittest
from config_translator import ConfigTranslator

class TestConfigTranslator(unittest.TestCase):
    def setUp(self):
        self.input_text = """
        -- Single line comment
        #| Multi-line
        comment |#
        array(1, 2, 3) -> my_array
        {
            key1 = 'value1',
            key2 = 42
        } -> my_dict
        ![my_array]
        ![my_dict]
        """
        self.translator = ConfigTranslator(self.input_text)

    def test_remove_comments(self):
        result = self.translator.remove_comments()
        self.assertNotIn("-- Single line comment", result)
        self.assertNotIn("#| Multi-line\ncomment |#", result)

    def test_translate(self):
        output = self.translator.translate()
        self.assertIn("my_array", output)
        self.assertIn("my_dict", output)

if __name__ == "__main__":
    unittest.main()
