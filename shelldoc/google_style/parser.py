from shelldoc.google_style.lexer import BashLexer


class Description:
    def __init__(self):
        self.content = ""

    def parse(self, parser):
        while parser.current_token.name == "STRING":
            self.content += f"{parser.current_token.value}\n"
            parser._advance()
            parser._skip_whitespace()
            parser._skip_empty_line()
            parser._skip_empty_comment()
        return self.content


class DocumentationStatement:
    def __init__(self, block_indent):
        self.token = None
        self.elements = []
        self.indent_number = 0
        self.block_indent = block_indent

    def parse(self, parser):
        self.token = parser.current_token.value
        parser._advance()
        while parser.current_token.name in ["STRING", "WS"]:

            if parser.current_token.name == "WS":
                if parser.current_token.value >= 1 and self.indent_number == 0:
                    self.indent_number = parser.current_token.value

                if self.indent_number == self.block_indent:
                    raise ValueError(f"Need indentation at line {parser.current_token.line}.")
                if self.indent_number != parser.current_token.value:
                    if parser.current_token.value == self.block_indent:
                        break
                    else:
                        raise ValueError(
                            f"Indentation mismatch at line {parser.current_token.line}. Expected {self.indent_number} but got {parser.current_token.value}"
                        )

                parser._advance()
            elif self.indent_number == self.block_indent:
                raise ValueError(f"Need indentation at line {parser.current_token.line}.")

            self.elements.append(parser.current_token.value)
            parser._advance()
        return {self.token: self.elements}


class DocumentationBlock:
    def __init__(self):
        self.function = None
        self.block_indent = None
        self.description = None
        self.stmts = []

    def parse(self, parser):
        parser.consume_expected("BLOCK_DOC_BEG")

        if parser.current_token.name == "WS":
            self.block_indent = parser.current_token.value
        else:
            self.block_indent = 0

        parser._skip_whitespace()
        parser._skip_empty_line()
        parser._skip_empty_comment()

        self.description = Description().parse(parser)

        while parser.current_token.name not in [
            "BLOCK_DOC_BEG",
            "FUNCTION",
            "BASH_TEXT",
        ]:
            parser._skip_whitespace()
            parser._skip_empty_line()
            parser._skip_empty_comment()
            doc_stmts = DocumentationStatement(self.block_indent).parse(parser)
            self.stmts.append(doc_stmts)

        parser.consume_expected("BLOCK_DOC_BEG")

        parser._skip_whitespace()
        parser._skip_empty_line()
        parser._skip_empty_comment()

        parser.check("FUNCTION")
        self.function = parser.current_token.value
        parser._advance()

        return {
            "function": self.function,
            "description": self.description,
            "stmts": self.stmts,
        }


class Todos:
    def parse(self, parser):
        todo = parser.current_token.value
        parser._advance()
        return todo


class DocumentationProgram:
    def __init__(self):
        self.description = None
        self.blocks = []
        self.shebang = None
        self.todos = []
        self._did_bash_begin = False

    def parse(self, parser):
        while parser.current_token is not None:

            if parser.current_token.name == "BASH_TEXT" and not self._did_bash_begin:
                self._did_bash_begin = True

            self._description(parser)

            if parser.current_token.name == "SHEBANG":
                self.shebang = parser.current_token.value
                parser._advance()

            elif parser.current_token.name == "BLOCK_DOC_BEG":
                block = DocumentationBlock().parse(parser)
                self.blocks.append(block)
            elif parser.current_token.name == "TODO":
                self.todos.append(Todos().parse(parser))
            else:
                parser._advance()

        return {
            "shebang": self.shebang,
            "description": self.description,
            "blocks": self.blocks,
            "todos": self.todos,
        }

    def _description(self, parser):

        is_str = parser.current_token.name == "STRING"
        is_prev_token = parser.prev_token is not None
        is_beg = is_prev_token and parser.prev_token.name in [
            "SHEBANG",
            "EMPTY_LINE",
            "WS",
            "EMPTY_COMMENT",
        ]

        if self.description is None and not self._did_bash_begin and is_str and is_beg:
            self.description = Description().parse(parser)


class Parser:
    def __init__(self, lines):
        self.l = BashLexer(lines)
        self.current_token = self.l.next_token()
        self.prev_token = None

    def consume_expected(self, name):
        if self.current_token.name == name:
            self._advance()
        else:
            error_msg = f"Expected {name} but got {self.current_token.name} "
            error_msg += f"at position ({self.current_token.line},{self.current_token.column})"
            raise ValueError(f"{error_msg}")

    def check(self, name):
        if self.current_token.name != name:
            error_msg = f"Expected {name} but got {self.current_token.name} "
            error_msg += f"at position ({self.current_token.line},{self.current_token.column})"
            raise ValueError(error_msg)

    def _advance(self):
        self.prev_token = self.current_token
        self.current_token = self.l.next_token()

    def _skip_whitespace(self):
        while self.current_token.name == "WS":
            self._advance()

    def _skip_empty_line(self):
        while self.current_token.name == "EMPTY_LINE":
            self._advance()

    def _skip_empty_comment(self):
        while self.current_token.name == "EMPTY_COMMENT":
            self._advance()

    def parse(self):
        ast = DocumentationProgram().parse(self)
        return ast
