"""
はてなブログ用、MarkdownのTeX記法の置換器
=========================================

数式の有効化
------------
MathJaxを導入することで、``$$`` で囲まれた数式を有効化できる（ ``[tex: ]`` の囲いが不要になる）

MathJaxの導入は、以下のようなコードを文中に入れればよい。

.. code::

    <script>
        MathJax = {
            tex: {inlineMath: [['$', '$'], ['\\(', '\\)']]}
        };
    </script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>


数式の囲い
----------
インライン数式は ``\(\)``にする必要がなく、 ``$$`` で問題なく動作している様子。

しかし、ディスプレイ（ブロック）数式はそのままではうごかなかったので ``\[\]`` で囲うようにする。

具体的には

.. code::

    $$
    y = f(x)
    $$

から

.. code::

    <p>
    \[
        y = f(x) 
    \]
    </p>

に置換する。


数式の記法
----------
普通のHTML + MathJaxでは問題なく表示されるような数式が、はてなブログで表示されないことがある。

例えば添字を使う際に ``x^2`` ではダメで、 ``x ^ 2`` のようにスペースを開ければ動作することがある。


"""
import re
import sys


class HatenaMarkdown:
    """はてなブログ用のMarkdown -> Mathjax変換ツール"""

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
        self._replace_double_dollar()
        self._replace_dollar()
        return self

    def _replace_double_dollar(self):
        """$$ ... $$ を <p class="math display">\[ ... \]</p>に置換する"""
        output: str = ""
        mds: list = self.md.split("$$")
        for i in range(len(mds)):
            if i % 2 == 0:
                output += mds[i]
            else:
                output += '<p class="math display">\[' + mds[i] + '\]</p>'
        self.md = output
        return self

    def _replace_dollar(self):
        """$ ... $ を <span class="math inline">\( ... \)</span>に置換する"""
        output: str = ""
        mds: list = self.md.split("$")
        for i in range(len(mds)):
            if i % 2 == 0:
                output += mds[i]
            else:
                output += '<span class="math inline">\(' + mds[i] + '\)</span>'
        self.md = output
        return self

    def add_mathjax(self):
        mathjax = """
<script>
    MathJax = {
        tex: {inlineMath: [['$', '$'], ['\\(', '\\)']]}
    };
</script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>
"""
        self.md = mathjax + self.md
        return self


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage: python hatena_converter.py [file.md]")
    else:
        file_name = sys.argv[1]
        hatena = HatenaMarkdown()
        hatena.read(file_name)
        hatena.replace_dollar()
        hatena.add_mathjax()
        hatena.add_spaces()
        new_name = file_name.replace(".md", "") + "_.md"
        print(f"Saving {new_name}")
        hatena.save(new_name)
