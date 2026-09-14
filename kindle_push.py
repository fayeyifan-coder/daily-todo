import os
import random
import requests

def parse_clippings(file_path):
    if not os.path.exists(file_path):
        print("未找到 My Clippings.txt 文件！")
        return []
    
    # 读取 Kindle 划线文件（自动兼容 UTF-8 BOM）
    with open(file_path, 'r', encoding='utf-8-sig', errors='ignore') as f:
        content = f.read()
    
    # Kindle 的固定条目分割符
    raw_entries = content.split('==========')
    highlights = []
    
    for entry in raw_entries:
        lines = [line.strip() for line in entry.strip().split('\n') if line.strip()]
        if len(lines) >= 3:
            book_title = lines[0]
            # 第 3 行开始是划线正文内容
            text_lines = lines[2:]
            text = "\n".join(text_lines)
            
            # 过滤无效或纯书签项
            if text and not text.startswith("Bookmark") and not text.startswith("您在位置"):
                highlights.append({
                    "title": book_title,
                    "text": text
                })
    return highlights

def push_to_bark(book_title, highlight_text):
    bark_key = os.environ.get("BARK_KEY")
    if not bark_key:
        print("未设置 BARK_KEY 环境变量！")
        return
    
    url = f"https://api.day.app/{bark_key}"
    payload = {
        "title": f"📖 划线胶囊｜{book_title}",
        "body": highlight_text,
        "group": "Kindle划线",
        "icon": "https://img.icons8.com/emoji/96/open-book-emoji.png"
    }
    
    res = requests.post(url, json=payload)
    print("Bark 推送结果:", res.json())

if __name__ == "__main__":
    clippings = parse_clippings("My Clippings.txt")
    if clippings:
        selected = random.choice(clippings)
        print(f"随机抽取到: 《{selected['title']}》 - {selected['text']}")
        push_to_bark(selected['title'], selected['text'])
    else:
        print("未成功解析到有效划线。")
