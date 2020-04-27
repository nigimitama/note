"""
はてなブログ用、MarkdownのTeX記法の置換器


MathJaxのコード

.. code::

    <script>
    MathJax = {
        tex: {
            inlineMath: [ ['$','$'], ["\\(","\\)"] ],
            displayMath: [ ['$$','$$'], ["\\[","\\]"] ]
        },
        svg: {fontCache: 'global'}
    };
    </script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>

と、Markdown記法のブロック数式を

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

にすることではてなブログでもほぼほぼ元のMarkdownのまま数式が書けることがわかったので、置換する
"""
import re
import sys


md = """# test

## inline math

inline math$Y = f(X) + \\varepsilon$

## display math

$$
\\text{display math}
{\\rm E}[(Y - f(X))^2]
$$

# end

end
"""


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

    def replace_dollar(self):
        """$$ ... $$ を <p>\[ ... \]</p>に置換する"""
        output: str = ""
        mds: list = self.md.split("$$")
        for i in range(len(mds)):
            if i % 2 == 0:
                output += mds[i]
            else:
                output += "<p>\[" + mds[i] + "\]</p>"
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
        print(hatena.md)
        hatena.save(file_name.replace(".md", "") + "_.md")
