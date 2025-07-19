# Blogger Word Cloud Generator 📝☁️

Blogger（Blogspot）で運営されているブログの記事を分析し、単語の頻出度をランキング表示して、ワードクラウド画像を生成するPythonスクリプトです。

あなたのブログがどんな「言葉」でできているか、可視化してみましょう！

---

## ✨ 主な機能

* **Bloggerブログ対応:** 公開されているBloggerブログであれば、どのブログでも分析可能です。
* **期間指定:** 「直近30日間」「1年間（365日）」など、分析したい期間を自由に指定できます。
* **外部ファイルによる除外ワード指定:** `stopwords.txt` を編集するだけで、分析から除外したい単語を簡単に管理できます。
* **2つの実行方法:** Webブラウザだけ（Google Colab）で動かす方法と、自分のPC（ローカル環境）で動かす方法に対応しています。

---

## 🚀 使い方

### 方法1：ブラウザで簡単に実行 (Google Colab)

PCへの環境構築は不要です。以下のボタンをクリックするだけで、スマホやPCのブラウザから直接ワードクラウドを生成できます。

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/amufaamo/blog-to-tagcloud/blob/main/wordcloud_notebook.ipynb)

**実行手順:**
1. 上の「Open In Colab」ボタンをクリックします。
2. 表示されたページで、あなたのブログURLとGitHubリポジトリURL、分析したい日数を入力します。
3. フォームの下にあるコードの左側にある**再生（▶）ボタン**をクリックします。
4. しばらく待つと、単語ランキングとワードクラウド画像が表示されます。

---

### 方法2：自分のPCで実行 (ローカル環境)

1.  **リポジトリをクローン**
    ```bash
    git clone [https://github.com/amufaamo/blog-to-tagcloud.git](https://github.com/amufaamo/blog-to-tagcloud.git)
    cd blog-to-tagcloud
    ```

2.  **ライブラリをインストール**
    ```bash
    pip install requests beautifulsoup4 janome wordcloud matplotlib
    ```

3.  **スクリプトを実行**
    ターミナルで `create_wordcloud_local.py` を実行します。`--url`と`--font`の指定は必須です。

    **macOS の場合:**
    ```bash
    python create_wordcloud_local.py --url https://あなたのブログURL/ --days 365 --font "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc"
    ```

    **Windows の場合:**
    ```bash
    python create_wordcloud_local.py --url https://あなたのブログURL/ --days 365 --font "C:/Windows/Fonts/YuGothM.ttc"
    ```

---

## 🔧 除外ワードのカスタマイズ

分析結果から除外したい単語は、`stopwords.txt` ファイルを編集することで、自由に管理できます。

1. リポジトリにある `stopwords.txt` を開きます。
2. 除外したい単語を1行に1つずつ追記・編集します。
3. ファイルを保存し、GitHubにプッシュします。

Colab版、ローカル版ともに、次回の実行時からこのファイルが参照され、リスト内の単語が自動で分析から除外されます。
