# Kenny Fryar-Ludwig
# A01284981
# CS 4700

import re
import os
import datetime

# https://regex101.com/r/vitR4W/1

RE_ASSINGMENT = ""
RE_LITERAL_ASSGN = "(?P<assign>[\w]+\s*=\s*)?(?P<lit>[-]?[0-9]+)"
RE_OP_DELIM = ""
RE_INPUT_END = ""
RE_BLOCK_COMMENT_START = "(?P<comment>/\*.*$)"
RE_BLOCK_COMMENT_END = "(?P<comment>^.*\*/$)"


RE_KEYWORD = "\W(?P<keyword>public|private|protected|static|return|System\.[\w.]+|class|else\s+if|if|else)\W"
RE_LITERAL = "(?P<lit>([-]?[0-9]+|[\'\"][\w\s]+[\'\"])"

RE_COMPARATOR = "(?P<compar>[=<>]=)"
RE_PUNCT = "(?P<punct>[=<>?]+)"
RE_CLASS_DECL = re.compile("(?P<access>public|private|protected(\s+static)?)\s+class\s+(?P<name>[a-zA-Z]\w+)")
RE_FUNCTION_DECL = re.compile("(?P<access>(public|private|protected)(\s+static)?)\s+(?P<ret_type>\w+)\s+(?P<name>\w+)\((?P<params>.*)\)")
RE_IDENTIFIER = re.compile("(?P<access>(protected|private|public)(\s+static)?)\s+(?P<type>[a-zA-Z][\w\[\]]*)\s+(?P<name>[a-zA-Z]\w*)(\s*=\s*(?P<value>[\"'\w]+))?\s*;")
RE_FUNC_PARAMS = re.compile("((?P<type>[a-zA-Z][\w\[\]]+)\s+(?P<name>\w+)\s*(=\s*(?P<value>[\w'\"]+))?(,\s*)?)")
RE_SANITIZE_LINES = re.compile("(?P<comment>[/]{2}.*$)|(^\s+|\s+$)")

# TEST_FILE = "HelloWorld.java"
TEST_FILE = "test_input.java"

def nest(level):
    return "".ljust((1 + level) * 4)

def output_error(error_text):
    print 'ERROR - "{}"'.format(error_text)

class Expression:
    def __init__(self, expr_type, value):
        self.type = expr_type
        self.value = value

    def __str__(self):
        return '{} {}'.format(self.type.upper(), self.value)

class FileStructure:
    def __init__(self, file_name):
        self.classes = {}
        self.global_functions = {}
        self.global_variables = {}
        self.lines = []
        self.file_name = file_name
        self.is_valid = self.input_file(file_name)

        self.expressions = []

    def input_file(self, file_name):
        if os.path.exists(file_name):
            user_file = open(file_name, mode='r')
            temp_lines = user_file.readlines()
            for line in temp_lines:
                cleaned_line = RE_SANITIZE_LINES.sub('', line)
                if len(cleaned_line) > 0:
                    self.lines.append(cleaned_line)
            return True
        else:
            self.lines = []
            output_error("File could not be read, check the file path, read permissions, and/or contents")
            return False

    def determine_type(self, line):
        if RE_FUNCTION_DECL.match(line) is not None:
            return "function", Function(RE_FUNCTION_DECL.match(line).groupdict())
        if RE_CLASS_DECL.match(line) is not None:
            return "class", Class(RE_CLASS_DECL.match(line).groupdict())
        if RE_IDENTIFIER.match(line) is not None:
            return "variable", Var(RE_IDENTIFIER.match(line).groupdict())
        return "None", None

    def parse_file(self):
        line_count = len(self.lines)
        line_number = 0
        while line_number < line_count:
            line_type, mystery_object = self.determine_type(self.lines[line_number])
            if line_type == "class":
                self.classes[mystery_object.name] = mystery_object
                line_number = self.parse_class(line_number, mystery_object)
            elif line_type == "function":
                self.global_functions[mystery_object.name] = mystery_object
                line_number = self.parse_function(line_number, mystery_object)
            elif line_type == "variable":
                self.global_variables[mystery_object.name] = mystery_object
            else:
                output_error("Line could not be processed:\n{}".format(self.lines[line_number]))
            line_number += 1
        return str(self)

    def get_variable(self, line):
        temp_obj = None
        regex_results = RE_IDENTIFIER.match(line)
        if regex_results is not None:
            temp_obj = Var(regex_results.groupdict())
        return temp_obj

    def parse_class(self, line_number, class_obj):
        current_line = line_number
        class_scope = 0
        while current_line < len(self.lines):
            line = self.lines[current_line]
            line_type, mystery_object = self.determine_type(line)
            class_scope += line.count('{') - line.count('}')

            if class_scope <= 0:
                break

            if line_type == 'function':
                class_obj.functions[mystery_object.name] = mystery_object
                current_line = self.parse_function(current_line, mystery_object)
            elif line_type == 'variable':
                current_line += 1
                class_obj.variables[mystery_object.name] = mystery_object
            else:
                current_line += 1
        return current_line

    def parse_function(self, line_number, func_obj):
        current_line = line_number
        func_scope = 0
        while current_line < len(self.lines):
            line = self.lines[current_line]
            line_type, mystery_object = self.determine_type(line)
            func_scope += line.count('{') - line.count('}')
            if func_scope <= 0:
                break
            temp_variable = self.get_variable(line)
            if temp_variable is not None:
                func_obj.variables[temp_variable.name] = temp_variable
            current_line += 1
        return current_line

    def __str__(self):
        result_str = "File: {}".format(self.file_name)
        result_str += "\nClasses contained: "
        for key in self.classes.keys():
            result_str += "\n{}".format(self.classes[key])
        if len(self.global_functions.keys()) > 0:
            result_str += "\nGlobal functions contained: "
            for key in self.global_functions.keys():
                result_str += "\n{}{}".format(nest(1), self.global_functions[key])
        if len(self.global_variables.keys()) > 0:
            result_str += "\nGlobal variables contained: "
            for key in self.global_variables.keys():
                result_str += "\n{}{}".format(nest(1), self.global_variables[key])
        return result_str

    def print_lines(self):
        for line in self.lines:
            print line

class Var():
    def __init__(self, val_dict):
        self.name = val_dict['name'] if 'name' in val_dict else "N/A"
        self.access = val_dict['access'] if 'access' in val_dict else "Local"
        self.type = val_dict['type'] if 'type' in val_dict else "N/A"
        self.value = val_dict['value'] if 'value' in val_dict else "N/A"

    def __str__(self):
        return "Type: {}, Name: {}, Value: {}, Access: {}".format(self.type, self.name, self.value, self.access)

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
        result_str = "Name: {}, Access: {}, Returns: {} ".format(self.name, self.access, self.return_type)
        if self.params is not None and len(self.params) > 0:
            for var in self.params:
                result_str += "\n{}Parameter: {}".format(nest(3), var)
        if len(self.variables) > 0:
            for key in self.variables.keys():
                result_str += "\n{}Local Variable: {}".format(nest(3), self.variables[key])
        return result_str


class Class():
    def __init__(self, val_dict):
        self.name = val_dict['name'] if 'name' in val_dict else "N/A"
        self.access = val_dict['access'] if 'access' in val_dict else "N/A"
        self.static = False
        self.functions = {}
        self.variables = {}

    def emit_expressions(self):
        result_str = "{}Class: {}, access: {}".format(nest(0), self.name, self.access)
        if len(self.variables) > 0:
            result_str +=  "\n{}Member Variables: ".format(nest(1))
            for key in self.variables.keys():
                result_str += "\n{}Variable: {}".format(nest(2), self.variables[key])
        if len(self.functions) > 0:
            result_str +=  "\n{}Member Functions:".format(nest(1))
            for key in self.functions.keys():
                result_str += "\n{}Function: {}".format(nest(2), self.functions[key])
        return result_str

    def __str__(self):
        result_str = "{}Class: {}, access: {}".format(nest(0), self.name, self.access)
        if len(self.variables) > 0:
            result_str +=  "\n{}Member Variables: ".format(nest(1))
            for key in self.variables.keys():
                result_str += "\n{}Variable: {}".format(nest(2), self.variables[key])
        if len(self.functions) > 0:
            result_str +=  "\n{}Member Functions:".format(nest(1))
            for key in self.functions.keys():
                result_str += "\n{}Function: {}".format(nest(2), self.functions[key])
        return result_str

def main_loop():
    input_file = FileStructure(TEST_FILE)
    if input_file.is_valid:
        print 'Starting file operations at {}'.format(datetime.datetime.now().strftime("%I:%M:%S %p"))
        print input_file.parse_file()
        print 'Processing completed at {}'.format(datetime.datetime.now().strftime("%I:%M:%S %p"))
    else:
        print "Error: Empty or non-existent file"

main_loop()

# Kenny Fryar-Ludwig
# A01284981
# CS 4700
