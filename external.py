"""Modules:"""
import sys


class Colors:
    def __init__(self, style, text_color, bg_color, data):
        self.style = style
        self.text_color = text_color
        self.bg_color = bg_color
        self.data = data

    def make(self):
        if self.bg_color == "":
            color = f'\x1b[;{self.style};{self.text_color}m {self.data}'
            return color

        color = f'\x1b[;{self.style};{self.text_color};{self.bg_color}m {self.data}'
        return color


class Output(Colors):
    def __init__(self, **options):
        self.style = options["style"]
        self.text_color = options["text_color"]
        self.bg_color = options["bg_color"]
        self.data = options["data"]

        super().__init__(self.style, self.text_color, self.bg_color, self.data)

    def printData(self):
        sys.stdout.write(Colors(self.style, self.text_color, self.bg_color, f'\r{self.data}\n').make())
        sys.stdout.flush()

    @staticmethod
    def reset():
        sys.stdout.flush()
        sys.stdout.write("\033[38;2;255;255;255m")


def handler(style, text_color, bg_color, flag, data):
    run = Output(style=style, text_color=text_color, bg_color=bg_color, data=data)
    if flag == "reset":
        run.reset()
    else:
        run.printData()