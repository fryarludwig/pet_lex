1.      Include a README.txt file that contains:
    1.      your name;
    2.     a list of software dependencies necessary to run your assignment;
    3.     a description of what you got working, what's partially working and what's completely broken; and

2.     Every source code file needs to have your name and student number at the top and the bottom in comments.

3.     The program should output one expression per line for each token in the input.

4.     There are five kinds of expressions you can emit:
    1.     (ID name) -- for an identifier.
    2.     (LIT value) -- for a literal value.
    3.     (KEYWORD symbol) -- for an keyword.
    4.     (PUNCT text) -- for operators and delimiters.
    5.     (ENDMARKER) -- for the end of the input.

5. If you encounter a lexical error, print (ERROR "explanation") and continue the processing.
·      You can use a built-in regular expression package.
·      You do not have to handle multiple character-set encodings. Assume the input is ASCII.
·      Do not use a lexer generator for this assignment
