import os
import markdown
import datetime
from bs4 import BeautifulSoup

def publish_posts():
    """
    讀取 posts 目錄下的所有 .md 文件，將其轉換為 HTML 並更新 index.html。
    """
    print("正在檢查是否有新的文章需要發布...")
    
    if not os.path.exists('posts'):
        os.makedirs('posts')
        print("已創建 posts 目錄。")
        return

    md_files = [f for f in os.listdir('posts') if f.endswith('.md')]
    
    if not md_files:
        print("沒有發現新的 Markdown 文章。")
        return

    # 讀取現有的 index.html
    if not os.path.exists('index.html'):
        print("錯誤: 找不到 index.html")
        return

    with open('index.html', 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    main_content = soup.find('main').find('article')
    toc_list = soup.find('aside', class_='toc-sidebar').find('ul')

    for md_file in md_files:
        post_id = md_file.replace('.md', '')
        print(f"正在處理: {md_file}")
        
        with open(os.path.join('posts', md_file), 'r', encoding='utf-8') as f:
            text = f.read()
            # 獲取第一行作為標題
            lines = text.split('\n')
            title = lines[0].replace('# ', '').strip() if lines[0].startswith('# ') else post_id
            content = markdown.markdown('\n'.join(lines[1:]))
            
        # 檢查是否已經存在該文章
        if soup.find('section', id=post_id):
            print(f"文章 {post_id} 已存在，正在更新內容...")
            section = soup.find('section', id=post_id)
            section.clear()
            
            h2 = soup.new_tag('h2')
            h2.string = title
            section.append(h2)
            
            content_soup = BeautifulSoup(content, 'html.parser')
            for element in content_soup.contents:
                section.append(element)
        else:
            print(f"正在添加新文章: {post_id}")
            # 添加到 TOC
            new_toc_item = soup.new_tag('li')
            new_toc_link = soup.new_tag('a', href=f'#{post_id}')
            new_toc_link.string = title
            new_toc_item.append(new_toc_link)
            toc_list.append(new_toc_item)
            
            # 添加到 Main Content
            new_section = soup.new_tag('section', id=post_id)
            h2 = soup.new_tag('h2')
            h2.string = title
            new_section.append(h2)
            
            content_soup = BeautifulSoup(content, 'html.parser')
            for element in content_soup.contents:
                new_section.append(element)
            
            main_content.append(new_section)

    # 保存更新後的 index.html
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(soup.prettify())

    print("發布流程完成，index.html 已更新。")

if __name__ == "__main__":
    publish_posts()
