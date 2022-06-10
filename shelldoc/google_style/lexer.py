import re


class Token:
    def __init__(self, name, value, line, column):
        self.name = name
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"({self.name}, {self.value}, {self.line}, {self.column})"


# BLOCK


class BashLexer:

    RULES = {
        "SHEBANG": re.compile(r"^#!.*"),
        "FUNCTION": re.compile(r"^\s*function\s*(\w+)\s*\(\w*\)\s*\{"),
        "GLOBALS": re.compile(r"^[Gg]lobals?\s*:?"),
        "ARGUMENTS": re.compile(r"^[Aa]rguments?\s*:?"),
        "OUTPUTS": re.compile(r"^[Oo]utputs?\s*:?"),
        "RETURNS": re.compile(r"^[Rr]eturns?\s*:?"),
        "SEE": re.compile(r"^[Ss]ee(\s*Also)?\s*:?"),
        "RAISES": re.compile(r"^[Rr]aises?\s*:?"),
        "TODO": re.compile(r"^TODO(\(\w*\))?\s*:?\s*(.*)"),
        "WS": re.compile(r"^\s+"),
        "EMPTY_LINE": re.compile(r"^\s*$"),
        "EMPTY_COMMENT": re.compile(r"^\s*$"),
        "START_WITH_SHARP": re.compile(r"^#"),
        "BLOCK_DOC_BEG": re.compile(r"^##.*"),
        "STRING": re.compile(r"^(.*)"),
    }

    def __init__(self, lines):
        self.lines = lines
        self.pos = 0
        self.line_no = 1
        self.current_line = self.lines[self.line_no - 1]
        self.sharp = False

    def next_token(self):
        tok = None
        while self.line_no < len(self.lines) and self.pos <= len(self.lines[self.line_no - 1]):
            self.current_line = self.lines[self.line_no - 1]

            if self.sharp is True:
                tok = self.sharp_token()
                break

            elif self.RULES["SHEBANG"].match(self.current_line):
                value = self.RULES["SHEBANG"].match(self.current_line).group(0)
                tok = Token("SHEBANG", value, self.line_no, self.pos)
                self.pos = 0
                self.line_no += 1
                break

            elif self.RULES["BLOCK_DOC_BEG"].match(self.current_line):
                value = self.RULES["BLOCK_DOC_BEG"].match(self.current_line).group(0)
                tok = Token("BLOCK_DOC_BEG", value, self.line_no, self.pos)
                self.pos = 0
                self.line_no += 1
                break

            elif self.RULES["START_WITH_SHARP"].match(self.current_line):
                self.pos += len(self.RULES["START_WITH_SHARP"].match(self.current_line).group(0))
                self.sharp = True

            elif self.RULES["FUNCTION"].match(self.current_line):
                value = self.RULES["FUNCTION"].match(self.current_line).group(1)
                tok = Token("FUNCTION", value, self.line_no, self.pos)
                self.pos += len(value)
                self.line_no += 1
                break

            elif self.RULES["EMPTY_LINE"].match(self.current_line):
                tok = Token("EMPTY_LINE", None, self.line_no, self.pos)
                self.pos = 0
                self.line_no += 1
                break
            else:
                tok = Token("BASH_TEXT", None, self.line_no, self.pos)
                self.pos = 0
                self.line_no += 1
                break
        return tok

    def ignore_whitespace(self):
        while self.pos < len(self.current_line) and self.current_line[self.pos] in [
            " ",
            "\t",
            "\n",
        ]:
            self.pos += 1

    def sharp_token(self):
        line_no = self.line_no
        if self.RULES["EMPTY_COMMENT"].match(self.current_line[self.pos :]):
            tok = Token("EMPTY_COMMENT", None, self.line_no, self.pos)
            self.line_no += 1
            self.pos = 0

        elif self.RULES["GLOBALS"].match(self.current_line[self.pos :]):
            tok = Token("GLOBALS", "Globals", self.line_no, self.pos)
            self.pos = 0
            self.line_no += 1

        elif self.RULES["ARGUMENTS"].match(self.current_line[self.pos :]):
            tok = Token("ARGUMENTS", "Arguments", self.line_no, self.pos)
            self.pos = 0
            self.line_no += 1

        elif self.RULES["OUTPUTS"].match(self.current_line[self.pos :]):
            tok = Token("OUTPUTS", "Outputs", self.line_no, self.pos)
            self.pos = 0
            self.line_no += 1

        elif self.RULES["RETURNS"].match(self.current_line[self.pos :]):
            tok = Token("RETURNS", "Returns", self.line_no, self.pos)
            self.pos = 0
            self.line_no += 1

        elif self.RULES["SEE"].match(self.current_line[self.pos :]):
            tok = Token("SEE", "See", self.line_no, self.pos)
            self.pos = 0
            self.line_no += 1

        elif self.RULES["RAISES"].match(self.current_line[self.pos :]):
            tok = Token("RAISES", "Raises", self.line_no, self.pos)
            self.pos = 0
            self.line_no += 1

        elif self.RULES["TODO"].match(self.current_line[self.pos :]):
            value = self.RULES["TODO"].match(self.current_line[self.pos :]).group(2)
            tok = Token("TODO", value, self.line_no, self.pos)
            self.pos = 0
            self.line_no += 1

        elif self.RULES["WS"].match(self.current_line[self.pos :]):
            value = self.RULES["WS"].match(self.current_line[self.pos :]).group(0)
            tok = Token("WS", len(value), self.line_no, self.pos)
            self.pos += len(value)

        elif self.RULES["STRING"].match(self.current_line[self.pos :]):
            value = self.RULES["STRING"].match(self.current_line[self.pos :]).group(0)
            tok = Token("STRING", value, self.line_no, self.pos)
            self.line_no += 1
            self.pos = 0

        if self.line_no > line_no:
            self.sharp = False

        return tok
