# 予測誤差のバイアスーバリアンス分解

予測誤差や推定量の推定の誤差は、バイアス（bias）とバリアンス（variance）という2つの構成要因に分けることができます。分けることで、誤差を削減する方法について議論しやすくなります。



推定量のバイアスーバリアンス分解については以前の記事で書いたことがあります

[「統計的に有意」だけでは足りないワケ：バイアス－バリアンス分解のはなし - 盆暗の学習記録](https://nigimitama.hatenablog.jp/entry/2018/11/24/062732)

が、今回は目的変数を$Y=f(X) + \varepsilon$として、予測可能な部分$f(X)$と予測不能な部分$\varepsilon$があるものに対する予測誤差の分解について、**どういう式の展開があった結果そうなったのか**についてメモしておきます。



# 概要

特徴量ベクトルを$X$とし、目的変数は$Y=f(X) + \varepsilon$であると仮定します。

$f(X)$は$Y$の予測可能な部分で、$\varepsilon$は予測不能なノイズで、${\rm E}[\varepsilon]=0,\ {\rm Var}[\varepsilon]=\sigma^2_{\varepsilon}$とします。

議論を簡潔にするため、データにおける$x_i$の値は決定論的に決められているとします。

学習データセット$\mathcal{D}$で学習した予測器を$\hat{f}(x; \mathcal{D})$とします。

様々な学習データセット$\mathcal{D}$にわたっての期待値をとる操作を${\rm E}_{\mathcal{D}}$と表します。



平均2乗誤差の下での、$X=x_0$における期待予測誤差（expected prediction error）もしくは汎化誤差（generalization error）と呼ばれるものは、
$$
{\rm EPE} (x_0) = {\rm E}_{\mathcal{D}}[(Y - \hat{f}(x_0; \mathcal{D}))^2 | X = x_0]
$$

これを分解すると
$$
\begin{align}{\rm EPE}(x_0)&={\rm E}_{\mathcal{D}}[(Y-\hat{f}(x_0; \mathcal{D}))^2|X=x_0]\\&= \sigma^2_{\varepsilon} + ({\rm E}_{\mathcal{D}}[\hat{f}(x_0; \mathcal{D})]- f(x_0))^2+ {\rm E}_{\mathcal{D}}[(\hat{f}(x_0; \mathcal{D}) - {\rm E}_{\mathcal{D}}[\hat{f}(x_0; \mathcal{D})])^2]\\&= \sigma^2_{\varepsilon} + {\rm Bias}(\hat{f}(x_0; \mathcal{D}))^2 + {\rm Var}_{\mathcal{D}}(\hat{f}(x_0; \mathcal{D}))\\&= {\rm 削減不能な誤差} + {\rm バイアス}^2 + {\rm バリアンス（分散）}\end{align}
$$
と分解できることが知られています。



# 展開

この分解の過程を以下で整理していく。ただし、記号を以下のように簡略化します。
$$
\begin{align}f &:= f(x_0)\\\hat{f} &:= \hat{f}(x_0; \mathcal{D})\\{\rm E} &:= {\rm E}_{\mathcal{D}}\\{\rm Var} &:= {\rm Var}_{\mathcal{D}}\\\end{align}
$$

$$
\begin{align}{\rm EPE}(x_0)&={\rm E}[(Y-\hat{f})^2]\\&={\rm E}[(Y - {\rm E}[\hat{f}] + {\rm E}[\hat{f}] - \hat{f})^2]\\&={\rm E}[(Y - {\rm E}[\hat{f}])^2 + 2(Y - {\rm E}[\hat{f}])({\rm E}[\hat{f}] - \hat{f}) + ({\rm E}[\hat{f}] - \hat{f})^2]\\&={\rm E}[(Y - {\rm E}[\hat{f}])^2]+ {\rm E}[2(Y - {\rm E}[\hat{f}])({\rm E}[\hat{f}] - \hat{f})]+ {\rm E}[({\rm E}[\hat{f}] - \hat{f})^2] \tag{1}\end{align}
$$

ここで式$(1)$の第1項は
$$
\begin{align}&{\rm E}[(Y - {\rm E}[\hat{f}])^2]\\&= {\rm E}[Y^2 - 2Y{\rm E}[\hat{f}] + {\rm E}[\hat{f}]^2]\\&= {\rm E}[(f+\varepsilon)^2 - 2(f + \varepsilon){\rm E}[\hat{f}]+ {\rm E}[\hat{f}]^2]\\&={\rm E}[(f^2 + 2f\varepsilon + \varepsilon^2)- (2f{\rm E}[\hat{f}] + 2\varepsilon{\rm E}[\hat{f}])- {\rm E}[\hat{f}]^2]\tag{2}\end{align}
$$
と分解でき、ここで${\rm E}[\varepsilon]=0$と期待値の線形性$c{\rm E}[X] = {\rm E}[cX]$から、$\varepsilon$が含まれる項はゼロが掛かってゼロになるので式$(2)$は
$$
\begin{align}&{\rm E}[(f^2 + 2f\varepsilon + \varepsilon^2)- (2f{\rm E}[\hat{f}] + 2\varepsilon{\rm E}[\hat{f}])+ {\rm E}[\hat{f}]^2]\tag{2}\\&= {\rm E}[\varepsilon^2]+ {\rm E}[f^2 - 2f{\rm E}[\hat{f}] +{\rm E}[\hat{f}]^2]\\&= {\rm E}[\varepsilon^2]+ {\rm E}[(f - {\rm E}[\hat{f}])^2]\end{align}
$$
です。

式$(1)$の第2項は、${\rm E}[\hat{f}]$が定数であることと、期待値と定数の関係${\rm E}[X - c] = {\rm E}[X]-c$から、
$$
{\rm E}[{\rm E}[\hat{f}] - \hat{f}]= {\rm E}[\hat{f}] - {\rm E}[\hat{f}] = 0
$$
なので、第2項はゼロになります。

ゆえに式$(1)$は
$$
\begin{align}&{\rm E}[(Y - {\rm E}[\hat{f}])^2]+ {\rm E}[2(Y - {\rm E}[\hat{f}])({\rm E}[\hat{f}] - \hat{f})]+ {\rm E}[({\rm E}[\hat{f}] - \hat{f})^2] \tag{1}\\&= {\rm E}[\varepsilon^2] + {\rm E}[(f - {\rm E}[\hat{f}])^2]+ {\rm E}[({\rm E}[\hat{f}] - \hat{f})^2]\tag{3}\end{align}
$$
となる。

式$(3)$の第1項は、
$$
\begin{align}{\rm Var}[\varepsilon]&= {\rm E}[(\varepsilon - {\rm E}[\varepsilon])^2]\\&= {\rm E}[\varepsilon^2 -2\varepsilon {\rm E}[\varepsilon] + {\rm E}[\varepsilon]^2]\\&= {\rm E}[\varepsilon^2 -2\varepsilon \cdot 0 + 0^2]\\&= {\rm E}[\varepsilon^2]\end{align}
$$
なので、ノイズ$\varepsilon$の分散に等しい。

式$(3)$の第2項は、$f$と${\rm E}[\hat{f}]$が定数であるため
$$
\begin{align}&{\rm E}[(f - {\rm E}[\hat{f}])^2]\\&=(f - {\rm E}[\hat{f}])^2\\\end{align}
$$
で、これは真の関数$f$と予測値の期待値${\rm E}[\hat{f}]$の差（バイアス）の2乗です。

式$(3)$の第3項は、予測値$\hat{f}$の分散（バリアンス）です。

よって、
$$
\begin{align}& {\rm E}[\varepsilon^2] + {\rm E}[(f - {\rm E}[\hat{f}])^2]+ {\rm E}[({\rm E}[\hat{f}] - \hat{f})^2]\tag{3}\\&= \sigma_\varepsilon^2+ (f - {\rm E}[\hat{f}])^2+ {\rm E}[({\rm E}[\hat{f}] - \hat{f})^2]\\&= \sigma^2_{\varepsilon} + {\rm Bias}(\hat{f})^2 + {\rm Var}(\hat{f})\\&= {\rm 削減不能な誤差} + {\rm バイアス}^2 + {\rm バリアンス（分散）}\end{align}
$$
です。

最初からの展開をまとめると
$$
\begin{align}
{\rm EPE}(x_0)
&={\rm E}[(Y-\hat{f})^2]\\&={\rm E}[(Y - {\rm E}[\hat{f}] + {\rm E}[\hat{f}] - \hat{f})^2]\\&={\rm E}[(Y - {\rm E}[\hat{f}])^2 + 2(Y - {\rm E}[\hat{f}])({\rm E}[\hat{f}] - \hat{f}) + ({\rm E}[\hat{f}] - \hat{f})^2]\\
&={\rm E}[(Y - {\rm E}[\hat{f}])^2]+ {\rm E}[2(Y - {\rm E}[\hat{f}])({\rm E}[\hat{f}] - \hat{f})]+ {\rm E}[({\rm E}[\hat{f}] - \hat{f})^2] \tag{1}\\
&={\rm E}[(Y - {\rm E}[\hat{f}])^2]
+ 2(Y - {\rm E}[\hat{f}])
\underbrace{{\rm E}[({\rm E}[\hat{f}] - \hat{f})]}_{=0}
+ {\rm E}[({\rm E}[\hat{f}]- \hat{f})^2]\\
&= {\rm E}[\varepsilon^2] + {\rm E}[(f - {\rm E}[\hat{f}])^2]+ {\rm E}[({\rm E}[\hat{f}] - \hat{f})^2]\tag{3}\\
&= \sigma_\varepsilon^2+ (f - {\rm E}[\hat{f}])^2+ {\rm E}[({\rm E}[\hat{f}] - \hat{f})^2]\\&= \sigma^2_{\varepsilon} + {\rm Bias}(\hat{f})^2 + {\rm Var}(\hat{f})\\&= {\rm 削減不能な誤差} + {\rm バイアス}^2 + {\rm バリアンス（分散）}\\
\end{align}
$$
となります。

# 各項の意味

## 削減不能な誤差（irreducible error）

$$
{\rm Var}_{\mathcal{D}}[\varepsilon] = \sigma^2_{\varepsilon}
$$

$Y$の分散であり、ノイズの分散。

データの測定誤差などに由来します。

削減できないので、予測誤差のバイアスーバリアンス分解を議論するときに、この項を省くために、$Y$と$\hat{f}$の誤差ではなく$f$と$\hat{f}$の誤差を分解して
$$
\begin{align}&{\rm E}[(f - \hat{f})^2]\\&= {\rm E}[(f - {\rm E}[\hat{f}] + {\rm E}[\hat{f}] - \hat{f})^2]\\&= {\rm E}[(f - {\rm E}[\hat{f}])^2]+ 2(f - {\rm E}[\hat{f}])\underbrace{{\rm E}[({\rm E}[\hat{f}] - \hat{f})]}_{=0}+ {\rm E}[({\rm E}[\hat{f}] - \hat{f})^2]\\&= (f - {\rm E}[\hat{f}])^2+ {\rm E}[({\rm E}[\hat{f}] - \hat{f})^2]\\&= {\rm Bias}(\hat{f})^2 + {\rm Var}(\hat{f})\end{align}
$$
とする場合もあります。



## バイアス（Bias）

$$
{\rm Bias}(\hat{f}(x_0; \mathcal{D}))= {\rm E}_{\mathcal{D}}[\hat{f}(x_0; \mathcal{D})]- f(x_0)
$$



予測値の平均と真の値との差。

多くの場合、より複雑なモデルを用いて予測すると、それだけバイアスは減少し、代わりにバリアンスが増加します。

## バリアンス（Variance）

$$
{\rm Var}_{\mathcal{D}}(\hat{f}(x_0; \mathcal{D}))= {\rm E}_{\mathcal{D}}[(\hat{f}(x_0; \mathcal{D}) - {\rm E}_{\mathcal{D}}[\hat{f}(x_0; \mathcal{D})])^2]
$$

（学習データセットを変えていったときの）予測値の分散。

学習データセットを変えるたびに予測値がばらつく、ということは、学習・予測の安定性が低いということ。すなわち、単一の学習データセットに過学習していることに由来すると考えられます。



# 参考文献

[バイアス-バリアンス - 機械学習の「朱鷺の杜Wiki」](http://ibisforest.org/index.php?%E3%83%90%E3%82%A4%E3%82%A2%E3%82%B9-%E3%83%90%E3%83%AA%E3%82%A2%E3%83%B3%E3%82%B9)

[偏りと分散 - Wikipedia](https://ja.wikipedia.org/wiki/%E5%81%8F%E3%82%8A%E3%81%A8%E5%88%86%E6%95%A3)

Hastie, T., Tibshirani, R., & Friedman, J. (2009). *The elements of statistical learning: data mining, inference, and prediction*. Springer Science & Business Media.

