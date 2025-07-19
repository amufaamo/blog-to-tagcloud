import requests
from bs4 import BeautifulSoup
from janome.tokenizer import Tokenizer
from collections import Counter
import re
from datetime import datetime, timedelta, timezone
import argparse
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# --- ▼▼▼ ここが新しいポイント！ ▼▼▼ ---
# 除外したい単語をこのリストに追加してください
CUSTOM_STOP_WORDS = {
    # ユーザーが指定した単語
    'する', 'いる', 
    
    # その他、一般的すぎる可能性のある単語の例
    'ある', 'ない', '思う', 'こと', 'もの',
    'なる', 'よう', 'みたい', 'いう', 'これ',
    'それ', 'いい', 'さん', 'ちゃん', 'くん'
}
# --- ▲▲▲ ここまで ▲▲▲ ---


def analyze_blog(base_url, days_to_check):
    """ブログ記事を収集・解析して単語の頻出度を返す"""
    all_text = ""
    jst = timezone(timedelta(hours=9))
    start_date = datetime.now(jst) - timedelta(days=days_to_check)
    current_url = base_url
    page_num = 1
    
    print(f"ブログの分析を開始します。対象期間: {days_to_check}日間")
    print(f"分析開始日: {start_date.strftime('%Y-%m-%d')}")

    while current_url:
        print(f"\nページ {page_num} を取得中...: {current_url}")
        try:
            response = requests.get(current_url)
            response.encoding = response.apparent_encoding
            soup = BeautifulSoup(response.text, 'html.parser')
        except requests.exceptions.RequestException as e:
            print(f"エラー: ページにアクセスできませんでした。 {e}")
            break
        
        posts = soup.find_all('article', class_='post-outer-container')
        if not posts and page_num == 1:
            return None

        page_contains_valid_posts = False
        for post in posts:
            time_tag = post.find('time', class_='published')
            body_tag = post.find('div', class_='post-body')

            if not time_tag or not body_tag:
                continue
            
            post_date = datetime.fromisoformat(time_tag['datetime'])
            
            if post_date >= start_date:
                page_contains_valid_posts = True
                all_text += body_tag.get_text() + "\n"
        
        if not page_contains_valid_posts and page_num > 1:
            break

        older_posts_link = soup.find('a', class_='blog-pager-older-link')
        if older_posts_link and older_posts_link.has_attr('href'):
            current_url = older_posts_link['href']
            page_num += 1
        else:
            current_url = None
    
    if not all_text:
        print("エラー: 分析対象となるテキストがありませんでした。")
        return None

    print("\n収集したすべてのテキストを解析中...")
    t = Tokenizer()
    words = []
    for token in t.tokenize(all_text):
        word = token.surface
        part_of_speech = token.part_of_speech.split(',')[0]
        
        # ✅ 条件を追加：除外ワードリストに含まれていない単語のみをカウント
        if word not in CUSTOM_STOP_WORDS and \
           part_of_speech in ['名詞', '動詞', '形容詞'] and \
           len(word) > 1 and \
           not re.match(r'^[0-9]+$', word):
            words.append(word)
    
    return Counter(words)

def create_word_cloud(counter, font_path):
    """単語の頻度情報からワードクラウド画像を生成して保存する"""
    if not font_path:
        print("\n⚠️  エラー: --font オプションで日本語フォントのパスを指定してください。")
        return

    print("\nワードクラウド画像を生成中...")
    
    try:
        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color='white',
            font_path=font_path,
            max_words=150,
            colormap='viridis'
        ).generate_from_frequencies(counter)

        output_filename = "blog_wordcloud.png"
        wordcloud.to_file(output_filename)
        print(f"\n🎉 完成！ '{output_filename}' という名前で画像を保存しました！")

    except Exception as e:
         print(f"エラー: ワードクラウドの生成に失敗しました。: {e}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Bloggerの単語頻度を分析し、ワードクラウドを生成します。')
    parser.add_argument('--url', type=str, required=True, help='分析したいBloggerのURL')
    parser.add_argument('--days', type=int, default=30, help='分析対象とする日数')
    parser.add_argument('--font', type=str, help='(重要)日本語表示のためのフォントファイルのパス')
    
    args = parser.parse_args()
    
    word_counter = analyze_blog(args.url, args.days)
    
    if word_counter:
        print("\n--- ✅最終結果: 単語の頻度ランキング TOP 50 ---")
        for word, count in word_counter.most_common(50):
            print(f"{word}: {count}回")
        
        create_word_cloud(word_counter, args.font)
