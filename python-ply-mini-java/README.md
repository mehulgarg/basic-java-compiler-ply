# python-ply-mini-java
The goal for this project is to build a mini java compiler, using python's PLY (Python Lex-Yacc) tool, built by <a target="_blank" href="http://www.dabeaz.com/ply/">  David Beazley. </a>
The grammar for the mini java language, can be seen here <a target="_blank" href="http://azapata.com/mini-java/mini-java-grammar.png"> Mini Java Grammar. </a> This project is it's initial stage, so there's a lot more to cover. Will keep this README updated.

There are three phases to this: 

* Lexer: Already built.
* Parser: Almost complete, it has a few bugs, that have to do with the way the language grammer is implemented.
* Abstract Syntax Tree: Under construction, no significant work done.

Directory structure:
```
├── ply/
│   ├── __init__.py
│   ├── lex.py
│   ├── yacc.py
│   ├── ygen.py
├── tests/
├── .gitignore 
├── ast.py
├── lexer.py
├── parser.py
```

### Lexer
- The lexer identifies the accepted tokens for the grammar, and builds the lex object.

### Parser
- The parser checks the sintax of the code thats passed to it, notifying of any syntax errors encountered.
