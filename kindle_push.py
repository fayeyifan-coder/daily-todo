import os
import random
import requests

def parse_clippings():
    # 自动扫描常见的划线文件名
    possible_names = [
        "My Clippings.txt", 
        "我的剪贴簿.txt", 
        "My_Clippings.txt", 
        "My Clippings.txt.txt", 
        "我的剪贴簿.txt.txt"
    ]
    
    target_file = None
    for name in possible_names:
        if os.path.exists(name):
            target_file = name
            break
            
    if not target_file:
        print("未找到划线文件！请检查是否已将 My Clippings.txt 上传至仓库根目录。")
        return []
        
    print(f"成功读取文件: {target_file}")
    
    with open(target_file, 'r', encoding='utf-8-sig', errors='ignore') as f:
        content = f.read()
    
    raw_entries = content.split('==========')
    highlights = []
    
    for entry in raw_entries:
        lines = [line.strip() for line in entry.strip().split('\n') if line.strip()]
        if len(lines) >= 3:
            book_title = lines[0]
            text_lines = lines[2:]
            text = "\n".join(text_lines)
            
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
    clippings = parse_clippings()
    if clippings:
        selected = random.choice(clippings)
        print(f"随机抽取到: 《{selected['title']}》 - {selected['text']}")
        push_to_bark(selected['title'], selected['text'])
