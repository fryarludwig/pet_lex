
2.     Every source code file needs to have your name and student number at the top and the bottom in comments.
3.     The program should output one expression per line for each token in the input.
4.     There are five kinds of expressions you can emit:
    1.     (ID name) -- for an identifier.
    2.     (LIT value) -- for a literal value.
    3.     (KEYWORD symbol) -- for an keyword.
    4.     (PUNCT text) -- for operators and delimiters.
    5.     (ENDMARKER) -- for the end of the input.

Kenny Fryar-Ludwig
"Lexerizer"
Lexer Implementation - CS 4700 - Fall 2017

Dependencies:
    Python 2.7.X
        Packages datetime, os, re

Overview:
    Fully Functional:
        Properly ignores duplicate whitespace
        Properly ignores single-line comments

    Partially functional:
        Parameters in function declarations are given access level "Local"
            This is true, yes, but... not needed.

    Not functional:
        Cannot parse classes within classes
        Cannot parse classes within functions
        Cannot handle multi-line comments
