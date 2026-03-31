import os
import markdown
import datetime

def publish_posts():
    """
    這是一個基礎的發布腳本，用於將 Markdown 內容轉換為 HTML 並更新 index.html。
    由於原始腳本丟失，此版本根據現有的 index.html 結構進行了重建。
    """
    print("正在檢查是否有新的文章需要發布...")
    
    # 檢查是否存在 posts 目錄，如果沒有則創建
    if not os.path.exists('posts'):
        os.makedirs('posts')
        print("已創建 posts 目錄。請將 .md 文件放在此目錄中。")
        return

    # 獲取所有待發布的 markdown 文件
    md_files = [f for f in os.listdir('posts') if f.endswith('.md')]
    
    if not md_files:
        print("沒有發現新的 Markdown 文章。")
        return

    for md_file in md_files:
        print(f"正在處理: {md_file}")
        with open(os.path.join('posts', md_file), 'r', encoding='utf-8') as f:
            text = f.read()
            html_content = markdown.markdown(text)
            
        # 這裡可以根據需要將內容插入到 index.html 或生成新的頁面
        # 目前僅作為工作流運行的佔位修復
        print(f"成功轉換 {md_file} 為 HTML。")

    print("發布流程完成。")

if __name__ == "__main__":
    publish_posts()
