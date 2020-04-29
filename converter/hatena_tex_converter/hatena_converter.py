"""
はてなブログ用、MarkdownのTeX記法の置換器
=========================================
$$ を [tex: ] に置換する
"""
import re
import sys


class HatenaMarkdown:

    def read(self, path: str):
        with open(path, "r", encoding="utf-8") as f:
            self.md = f.read()
        return self

    def save(self, path: str):
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.md)
        return self

    def add_spaces(self):
        """添字記号にスペースを入れて、はてなブログのパーサーに認識されやすくする"""
        self.md = self.md.replace("^", " ^ ").replace("_", " _ ")
        return self

    def replace_dollar(self):
        """$$ ... $$ を [tex: ... ]に置換する。


        Note
        ----
        数式中に[]が含まれていると失敗するので注意

        """
        self._replace_double_dollar()
        self._replace_dollar()
        return self

    def _replace_dollar(self):
        """$ ... $ を [tex: ... ]に置換する"""
        output: str = ""
        mds: list = self.md.split("$")
        for i in range(len(mds)):
            if i % 2 == 0:
                output += mds[i]
            else:
                output += "[tex: " + mds[i] + "]"
        self.md = output
        return self

    def _replace_double_dollar(self):
        """$$ ... $$ を [tex: ... ]に置換する"""
        output: str = ""
        mds: list = self.md.split("$$")
        for i in range(len(mds)):
            if i % 2 == 0:
                output += mds[i]
            else:
                output += "[tex: " + mds[i] + "]"
        self.md = output
        return self

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage: python hatena_converter.py [file.md]")
    else:
        file_name = sys.argv[1]
        hatena = HatenaMarkdown()
        hatena.read(file_name)
        hatena.replace_dollar()
        hatena.add_spaces()
        print(hatena.md)
        hatena.save(file_name.replace(".md", "") + ".txt")
