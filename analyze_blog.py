import os
import requests
from bs4 import BeautifulSoup
from janome.tokenizer import Tokenizer
from collections import Counter
import re
from datetime import datetime, timedelta, timezone
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import argparse

def load_stopwords(filepath='stopwords.txt'):
    """ファイルから除外ワードを読み込み、セットとして返す"""
    if not os.path.exists(filepath):
        print(f"警告: 除外ワードファイル '{filepath}' が見つかりません。")
        return set()
    with open(filepath, 'r', encoding='utf-8') as f:
        stopwords = {line.strip() for line in f if line.strip()}
    print(f"{len(stopwords)}個の除外ワードを '{filepath}' から読み込みました。")
    return stopwords

def analyze_blog(base_url, days_to_check, stopwords):
    # ... (この関数の内容はColab版と全く同じ) ...
    all_text = ""
    jst = timezone(timedelta(hours=9))
    start_date = datetime.now(jst) - timedelta(days=days_to_check)
    current_url = base_url
    page_num = 1
    print(f"ブログの分析を開始します。対象期間: {days_to_check}日間")
    while current_url:
        print(f"ページ {page_num} を取得中...")
        try:
            response = requests.get(current_url)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')
        except:
            print("エラー: ページにアクセスできませんでした。")
            break
        posts = soup.find_all('article', class_='post-outer-container')
        if not posts and page_num == 1: return None
        page_contains_valid_posts = False
        for post in posts:
            time_tag = post.find('time', class_='published')
            body_tag = post.find('div', class_='post-body')
            if not time_tag or not body_tag: continue
            post_date = datetime.fromisoformat(time_tag['datetime'])
            if post_date >= start_date:
                page_contains_valid_posts = True
                all_text += body_tag.get_text() + "\n"
        if not page_contains_valid_posts and page_num > 1: break
        older_posts_link = soup.find('a', class_='blog-pager-older-link')
        if older_posts_link and older_posts_link.has_attr('href'):
            current_url = older_posts_link['href']
            page_num += 1
        else:
            current_url = None
    if not all_text: return None
    print("\nテキストの解析中...")
    t = Tokenizer()
    words = [token.surface for token in t.tokenize(all_text) 
             if token.surface not in stopwords and 
             token.part_of_speech.startswith(('名詞', '動詞', '形容詞')) and 
             len(token.surface) > 1 and not re.match(r'^[0-9a-zA-Z]+$', token.surface)]
    return Counter(words)

def create_word_cloud(counter, font_path):
    # ... (この関数の内容はColab版と全く同じ) ...
    if not font_path:
        print("\n⚠️  エラー: --font オプションで日本語フォントのパスを指定してください。")
        return
    if not os.path.exists(font_path):
        print(f"\nエラー: 指定されたフォントファイルが見つかりません: {font_path}")
        return
    print("\nワードクラウド画像を生成中...")
    try:
        wordcloud = WordCloud(
            width=1200, height=600, background_color='white',
            font_path=font_path, max_words=150, colormap='viridis'
        ).generate_from_frequencies(counter)
        output_filename = "blog_wordcloud_local.png"
        wordcloud.to_file(output_filename)
        print(f"\n🎉 完成！ '{output_filename}' という名前で画像を保存しました！")
    except Exception as e:
         print(f"エラー: ワードクラウドの生成に失敗しました。: {e}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Bloggerの単語頻度を分析し、ワードクラウドを生成します。')
    parser.add_argument('--url', type=str, required=True, help='分析したいBloggerのURL')
    parser.add_argument('--days', type=int, default=30, help='分析対象とする日数')
    parser.add_argument('--font', type=str, required=True, help='(重要)日本語表示のためのフォントファイルのパス')
    parser.add_argument('--stopwords', type=str, default='stopwords.txt', help='除外ワードリストのファイルパス')
    
    args = parser.parse_args()
    
    custom_stopwords = load_stopwords(args.stopwords)
    word_counter = analyze_blog(args.url, args.days, custom_stopwords)
    
    if word_counter:
        print("\n--- ✅単語の頻度ランキング TOP 50 ---")
        for word, count in word_counter.most_common(50):
            print(f"{word}: {count}回")
        
        create_word_cloud(word_counter, args.font)
