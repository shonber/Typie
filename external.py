"""Modules:"""
import sys
import json


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


def save_stats(stats):
    try:
        with open("./stats.json", "r", encoding='utf-8') as ReadFile:
            lines = ReadFile.read()

        loaded_stats = json.loads(lines)
        loaded_stats[len(loaded_stats) + 1] = "test"
        load = json.dumps(loaded_stats, indent=2, ensure_ascii=False)

        with open("./stats.json", "w", encoding='utf-8') as WriteFile:
            WriteFile.writelines(load)

    except FileNotFoundError:
        with open("./stats.json", "w") as WriteFile:
            new_stats = {
                0: stats
            }

            load = json.dumps(new_stats, indent=2, ensure_ascii=False)
            WriteFile.writelines(load)


def load_stats():
    try:
        with open("./stats.json", "r", encoding='utf-8') as ReadFile:
            lines = ReadFile.read()

        loaded_stats = json.loads(lines)
        loaded_stats = json.dumps(loaded_stats, indent=2, ensure_ascii=False)
        return loaded_stats

    except FileNotFoundError:
        with open("./stats.json", "w") as WriteFile:
            WriteFile.write("")