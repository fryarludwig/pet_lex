import re
import os

# https://regex101.com/r/vitR4W/1

RE_ASSINGMENT = ""
RE_LITERAL = "(?P<lit>[-]?[0-9]+)"
RE_LITERAL_ASSGN = "(?P<assign>[\w]+\s*=\s*)?(?P<lit>[-]?[0-9]+)"
RE_KEYWORD = ""
RE_OP_DELIM = ""
RE_INPUT_END = ""
RE_BLOCK_COMMENT_START = "(?P<comment>/\*.*$)"
RE_BLOCK_COMMENT_END = "(?P<comment>^.*\*/$)"

RE_COMPARATOR = "(?P<compar>[=<>]=)"
RE_PUNCT = "(?P<punct>[=<>?]+)"

# RE_ENDMARKER = ""

RE_CLASS_DECL = re.compile("(?P<access>public|private|protected(\s+static)?)\s+class\s+(?P<name>[a-zA-Z]\w+)")
RE_FUNCTION_DECL = re.compile("(?P<access>(public|private|protected)(\s+static)?)\s+(?P<ret_type>\w+)\s+(?P<name>\w+)\((?P<params>.*)\)")
RE_IDENTIFIER = re.compile("(?P<type>[a-zA-Z]\w+)\s{1,}(?P<name>[a-zA-Z]\w*)(\s*=\s*(?P<value>[\"'\w]+))?\s*;")
RE_FUNC_PARAMS = re.compile("((?P<type>[a-zA-Z][\w\[\]]+)\s+(?P<name>\w+)\s*(=\s*(?P<value>[\w'\"]+))?(,\s*)?)")

RE_SANITIZE_LINES = re.compile("((?P<comment>[/]{2}.*$)|(^\s+)|(\s+$))")

# TEST_FILE = "HelloWorld.java"
TEST_FILE = "test_input.java"

"""

    Are we starting a class?
    Are we starting a function?
    Are we creating a variable?
        Is it initialized?
    Are we returning a value?
    Are we comparing values?
    Are we performing if/else?
    Is the function over?

"""

def nest(level):
    return "".ljust(level * 4)

class FileStructure:
    def __init__(self, file_name):
        self.classes = {}
        self.functions = {}
        self.variables = {}
        self.lines = []
        self.file_name = file_name
        self.is_valid = self.input_file(file_name)

    def input_file(self, file_name):
        if os.path.exists(file_name):
            user_file = open(file_name, mode='r')
            temp_lines = user_file.readlines()
            for line in temp_lines:
                cleaned_line = RE_SANITIZE_LINES.sub('', line)
                # cleaned_line = line.strip()
                if len(cleaned_line) > 0:
                    self.lines.append(cleaned_line)
            return True
        else:
            self.lines = []
            return False

    def parse_file(self):
        line_count = len(self.lines)
        line_number = 0

        while line_number < line_count:
            print line_number
            line = self.lines[line_number]
            parsed_class = self.get_class(line)
            if parsed_class is not None:
                self.classes[parsed_class.name] = parsed_class
                line_number = self.parse_class(line_number, parsed_class)
                continue

            temp_obj = self.get_function(line)
            if temp_obj is not None:
                self.functions[temp_obj.name] = temp_obj
                # function_nest.append(temp_obj)
                continue

            temp_obj = self.get_variable(line)
            if temp_obj is not None:
                self.variables[temp_obj.name] = temp_obj
                # function_nest.append(temp_obj)
                continue
            print line_number
            line_number += 1

        return str(self)

    def get_function(self, line):
        temp_obj = None
        regex_results = RE_FUNCTION_DECL.match(line)
        if regex_results is not None:
            temp_obj = Function(regex_results.groupdict())
        return temp_obj

    def get_class(self, line):
        temp_obj = None
        regex_results = RE_CLASS_DECL.match(line)
        if regex_results is not None:
            temp_obj = Class(regex_results.groupdict())
        return temp_obj

    def get_variable(self, line):
        temp_obj = None
        regex_results = RE_IDENTIFIER.match(line)
        if regex_results is not None:
            temp_obj = Var(regex_results.groupdict())
        return temp_obj

    def parse_class(self, line_number, class_obj):
        current_line = line_number
        class_scope = 0

        while current_line < len(self.lines) and class_scope >= 0:
            line = self.lines[current_line]

            if '{' in line:
                class_scope += 1
            if '}' in line:
                class_scope -= 1

            current_line += 1

            # temp_obj = self.get_class(line)
            # if temp_obj is not None:
            #     # self.classes[temp_obj.name] = temp_obj
            #     continue

            temp_obj = self.get_function(line)
            if temp_obj is not None:
                self.functions[temp_obj.name] = temp_obj
                continue

            temp_obj = self.get_variable(line)
            if temp_obj is not None:
                self.variables[temp_obj.name] = temp_obj
                continue

        return current_line



    def __str__(self):
        result_str = "File: {}".format(self.file_name)
        result_str += "\nClasses contained: "
        for key in self.classes.keys():
            result_str += "\n{}{}".format(nest(1), self.classes[key])
        if len(self.functions) > 0:
            result_str += "\nFunctions: "
            for key in self.functions.keys():
                result_str += "\n{}{}".format(nest(1), self.functions[key])
        # if len(self.variables) > 0:
        #     result_str += "\nGlobal Variables: "
        #     for key in self.variables.keys():
        #         result_str += "\n{}{}".format(nest(1), self.variables[key])
        return result_str

    def print_lines(self):
        for line in self.lines:
            print line

class Var():
    def __init__(self, val_dict):
        self.name = val_dict['name'] if 'name' in val_dict else "N/A"
        self.type = val_dict['type'] if 'type' in val_dict else "N/A"
        self.value = val_dict['value'] if 'value' in val_dict else "N/A"

    def __str__(self):
        return "Type: {}, Name: {}, Value: {}".format(self.type, self.name, self.value)

class Function():
    def __init__(self, val_dict):
        self.name = val_dict['name'] if 'name' in val_dict else "N/A"
        self.access = val_dict['access'] if 'access' in val_dict else "N/A"
        self.return_type = val_dict['ret_type'] if 'ret_type' in val_dict else "N/A"
        param_string = val_dict['params'] if 'params' in val_dict else "N/A"
        self.params = self.parse_params(param_string)
        self.variables = {}

    def parse_params(self, params):
        var_list = []
        all_matches = [result for result in RE_FUNC_PARAMS.finditer(params) if result is not None]
        for match in all_matches:
            temp_var = Var(match.groupdict())
            if temp_var is not None:
                var_list.append(temp_var)
        return var_list

    def __str__(self):
        result_str = "{}{} - Function: {}, Returns: {} ".format(nest(1), self.access, self.name, self.return_type)
        if self.params is not None and len(self.params) > 0:
            result_str += "\n{}Parameters: ".format(nest(2))
            for var in self.params:
                result_str += "\n{}{}".format(nest(3), var)
        if len(self.variables) > 0:
            result_str += "\n{}Variables".format(nest(2))
            for var in self.variables.items():
                result_str += "\n{} Local Variable: {}".format(nest(3), var)

        return result_str


class Class():
    def __init__(self, val_dict):
        self.name = val_dict['name'] if 'name' in val_dict else "N/A"
        self.access = val_dict['access'] if 'access' in val_dict else "N/A"
        self.static = False
        self.functions = {}
        self.variables = {}

    def __str__(self):
        result_str = "{}Class: {}, access: {}".format(nest(1), self.name, self.access)
        if len(self.variables) > 0:
            print "\n{}Member Variables: ".format(nest(1))
            for key in self.variables.keys():
                result_str += "\n{}Variable: {}".format(nest(2), self.variables[key])
        if len(self.functions) > 0:
            print "\n{}Member Functions:".format(nest(1))
            for key in self.functions.keys():
                result_str += "\n{}Function: {}".format(nest(2), self.functions[key])
        return result_str

def main_loop():
    input_file = FileStructure(TEST_FILE)
    if input_file.is_valid:
        print input_file.parse_file()
    else:
        print "Error: Empty or non-existent file"


main_loop()

"""
    Alright, per line:
        Is the line empty or just whitespace?
            Skip
        Is the line one char?
            Open or closing bracket?
                Open - Let's mark that as a new scope
                Close - Close off the most recent scope
        Is it a class?

        Is it a function?

        Is it an assignment or declaration?

        Does it have literal?
"""

