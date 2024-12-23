import re
import sys
import toml

class ConfigTranslator:
    def __init__(self, input_text):
        self.input_text = input_text
        self.constants = {}

    def remove_comments(self):
        no_single_line = re.sub(r"--.*", "", self.input_text)
        no_multiline = re.sub(r"#\|.*?\|#", "", no_single_line, flags=re.DOTALL)
        return no_multiline

    def parse_constants(self, text):
        matches = re.findall(r"(\d+|'[^']*')\s*->\s*([a-z][a-z0-9_]*)", text)
        for value, name in matches:
            self.constants[name] = eval(value)
        return re.sub(r"(\d+|'[^']*')\s*->\s*[a-z][a-z0-9_]*", "", text)

    def replace_constants(self, text):
        return re.sub(r"!\[([a-z][a-z0-9_]*)\]", lambda m: str(self.constants.get(m.group(1), "undefined")), text)

    def parse_to_toml(self, text):
        arrays = re.findall(r"array\((.*?)\)", text)
        for array in arrays:
            elements = [eval(el.strip()) for el in array.split(",")]
            text = text.replace(f"array({array})", str(elements))

        dictionaries = re.findall(r"\{(.*?)\}", text)
        for dictionary in dictionaries:
            items = {k.strip(): eval(v.strip()) for k, v in [pair.split("=") for pair in dictionary.split(",")]}
            text = text.replace(f"{{{dictionary}}}", str(items))

        return toml.dumps(eval(text))

    def translate(self):
        text = self.remove_comments()
        text = self.parse_constants(text)
        text = self.replace_constants(text)
        return self.parse_to_toml(text)

if __name__ == "__main__":
    input_text = sys.stdin.read()
    translator = ConfigTranslator(input_text)
    print(translator.translate())
