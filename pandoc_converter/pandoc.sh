#!/bin/bash
# 数式・画像付きのmarkdownをhtmlに変換 - Qiita
# https://qiita.com/yohm/items/f14f03ccee918d4d7213
pandoc --self-contained -s --mathjax=./dynoload.js -c ./source_han.css ${1} -o "${1}.html"