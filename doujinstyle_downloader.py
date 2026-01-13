# ==============================================================================
#                  ✨ 运行环境要求 (Environment Requirements) ✨
# ==============================================================================
# 1. Python 版本: 3.6+
# 2. 依赖库: pip install requests beautifulsoup4 lxml
# 3. 功能：根据关键词全自动抓取 doujinstyle 网盘链接，支持 Session 复用、跨平台自适应路径与智能命名。
#    Function: Automatically crawl download links from doujinstyle based on keywords, 
#    supporting session reuse, cross-platform path adaptation, and smart naming.
# ==============================================================================

import requests
from bs4 import BeautifulSoup
import re 
import os
import time
import urllib.parse

# ==============================================================================
#                     🚀 自动化提取脚本配置 (用户仅需修改此处) 🚀
#                     🚀 Script Configuration (User just need to edit here) 🚀
# ==============================================================================

# 【目标配置】只需输入 doujinstyle 的展会标签关键字 (对应 URL 中的 result= 参数)。
# [Target Configuration] Just input the exhibition tag keyword (corresponds to result= parameter in URL).
# 
# 示例：春例22为rts22，秋例10为arts10，m3-2024春为m3-53，C104为c104，C106东方Project为c106%20touhou)
# Keyword example: 第二十二回博麗神社例大祭=rts22，第十回博麗神社秋季例大祭=arts10，m3-2024春=m3-53，C104=c104，C106東方Project=c106%20touhou
# 
# 脚本会自动处理 URL 编码（如 %20）并生成对应的文件夹名
# The script automatically handles URL encoding and generates safe filenames.

RESULT_KEYWORD = 'c107%20touhou'

# ==============================================================================
#                      ⚙️ 自动化逻辑处理 (底层核心，无需修改) ⚙️
#                      ⚙️ Logic Processing (Core, no edit needed) ⚙️
# ==============================================================================

# 1. 【路径自适应】获取当前脚本运行的绝对路径。
# [Path Adaptation] Get the absolute path of the current script.
current_dir = os.path.dirname(os.path.abspath(__file__))

# 2. 【动态安全命名】
# [Dynamic Safe Naming]
# urllib.parse.unquote: 将 '%20' 还原为空格 (Restore '%20' to spaces)
decoded_name = urllib.parse.unquote(RESULT_KEYWORD)

# re.sub: 使用正则表达式将 Windows/Linux 不允许的文件名特殊字符替换为下划线
# Replace invalid filename characters for Win/Linux with underscores.
safe_name = re.sub(r'[\\/*?:"<>| ]', '_', decoded_name)
OUTPUT_FILENAME = f"links_{safe_name}.txt"

# txt文件将直接生成在脚本同一目录，跨平台且彻底解决 Windows 桌面路径迁移导致的报错
# TXT file generated in script directory to solve path errors across platforms.
OUTPUT_FILE_PATH = os.path.join(current_dir, OUTPUT_FILENAME)

# 3. 【连接管理】创建 Session 对象。
# [Connection Management] Create Session object.
# Session 的核心作用是实现 TCP 连接复用（Keep-Alive），在大规模请求时能提升 50% 以上的速度
# Sessions implement TCP Keep-Alive, boosting speed by 50%+ during large requests.
session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': "https://doujinstyle.com/", 
})

# 4. 【常量配置】
# [Constants Configuration]
BASE_URL = "https://doujinstyle.com/"
SEARCH_URL_TEMPLATE = "https://doujinstyle.com/?p=search&source=1&type=blanket&result={result_key}&page={page_num}"

# 存储容器：使用 set 确保所有链接天然去重
# Storage: Use a set to ensure unique download links.
all_download_links = set()

# ==============================================================================
#                            ⬇️ 核心功能函数 ⬇️
#                            ⬇️ Core Functions ⬇️
# ==============================================================================

def get_all_file_ids(result_key):
    """
    逻辑说明：
    Logic Description:
    1. 遍历搜索结果的每一页。(Iterate through every search result page.)
    2. 使用 BeautifulSoup 锁定 <mainbar> 标签，从而物理隔离 <sidebar> 中的“热门专辑”。
       (Lock onto <mainbar> to isolate IDs from the "Hot Albums" in the sidebar.)
    3. 当检测到页面不再产生新 ID 或页面内容重复时，自动停止翻页。
       (Stop paging when no new IDs are found or content repeats.)
    """
    unique_ids = set()
    link_pattern = re.compile(r'\?p=page&type=1&id=(\d+)') # 匹配专辑 ID 的正则 (Regex for Album IDs)
    current_page, previous_page_ids, max_duplicate_checks = 0, set(), 2

    print(f"--- 🔍 正在检索结果 (Searching): {urllib.parse.unquote(result_key)} ---")

    while True:
        url = SEARCH_URL_TEMPLATE.format(result_key=result_key, page_num=current_page)
        current_page_ids = set()
        try:
            # 发送 GET 请求获取搜索页面内容 (Send GET request)
            response = session.get(url, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'lxml')
            
            # ✨ 核心策略：精准锁定主体区域。
            # Core Strategy: Target the main content area specifically.
            mainbar = soup.find('mainbar')
            target_area = mainbar if mainbar else soup # 容错处理 (Fallback)
            
            for a_tag in target_area.find_all('a', href=True):
                href = a_tag['href']
                if '?p=page&type=1&id=' in href:
                    match = link_pattern.search(href)
                    if match:
                        current_page_ids.add(match.group(1))

            # 翻页终止判定 (Paging termination logic)
            if not current_page_ids or (current_page > 0 and current_page_ids == previous_page_ids):
                max_duplicate_checks -= 1
                if max_duplicate_checks == 0: break
            
            if current_page_ids:
                unique_ids.update(current_page_ids)
                print(f"  -> 页面 {current_page}: 成功提取 {len(current_page_ids)} 个专辑 ID")
            
            previous_page_ids = current_page_ids
            current_page += 1
            time.sleep(0.3) # 礼貌间歇 (Polite delay)

        except Exception as e:
            print(f"  [Error] 访问第 {current_page} 页时发生异常: {e}"); break
            
    print(f"--- ✅ 检索完成，共找到 {len(unique_ids)} 个结果。 ---")
    return sorted(list(unique_ids))

# ==============================================================================
#                            ⬇️ 脚本主执行流程 ⬇️
#                            ⬇️ Main Execution ⬇️
# ==============================================================================

if __name__ == "__main__":
    start_time = time.time()
    
    # 步骤 1: 获取所有唯一的专辑 ID (Step 1: Get all unique Album IDs)
    FILE_IDS = get_all_file_ids(RESULT_KEYWORD)

    if not FILE_IDS:
        print("未发现任何匹配的 ID，请确认 RESULT_KEYWORD。 (No IDs found, check keyword.)")
    else:
        # 步骤 2: 遍历 ID，模拟点击“Download”按钮获取网盘真实链接
        # Step 2: Traverse IDs, simulate "Download" click to get direct links.
        print(f"--- 📡 正在解析原始下载链接 (解析模式: 连接复用) ---")
        
        for index, file_id in enumerate(FILE_IDS, 1):
            # payload 模拟了点击下载按钮时发送的 POST 数据 (Simulate POST data)
            payload = {'type': '1', 'id': file_id, 'source': '0', 'download_link': 'Download'}
            try:
                # allow_redirects=False 非常重要！网盘链接在 Location 响应头中。
                # Crucial: disable redirects to catch the link in the Location header.
                response = session.post(BASE_URL, data=payload, allow_redirects=False, timeout=20)
                
                # 检查是否发生重定向 (Check for redirects 301-307)
                if response.status_code in [301, 302, 303, 307]:
                    link = response.headers.get('Location')
                    # 过滤逻辑：只保留常见的网盘链接 (Filtering: keep common hosts)
                    if link and any(host in link for host in ['mega.nz', 'mediafire.com', 'drive.google.com']):
                        print(f"  [{index}/{len(FILE_IDS)}] ID {file_id} -> 链接捕获成功")
                        all_download_links.add(link)
                else:
                    print(f"  [{index}/{len(FILE_IDS)}] ID {file_id} -> 未发现重定向链接")
            except Exception: 
                continue

        # 步骤 3: 汇总结果并输出 (Step 3: Summarize and Output)
        if all_download_links:
            # 简单的数据分布统计 (Statistics distribution)
            stats = {
                'Mega': sum(1 for k in all_download_links if 'mega.nz' in k),
                'Mediafire': sum(1 for k in all_download_links if 'mediafire.com' in k),
                'GoogleDrive': sum(1 for k in all_download_links if 'drive.google.com' in k)
            }
            
            # 将 set 转为排序列表并保存 (Sort and save results)
            with open(OUTPUT_FILE_PATH, 'w', encoding='utf-8') as f:
                f.write('\n'.join(sorted(list(all_download_links))))
            
            # 打印任务报告 (Print Task Report)
            print(f"\n" + "="*55)
            print(f"🎉 任务完成 (Success)! 总耗时: {time.time() - start_time:.1f}s")
            print(f"📁 文件名 (File): {OUTPUT_FILENAME}")
            print(f"📊 分布 (Stats): Mega({stats['Mega']}), Mediafire({stats['Mediafire']}), GD({stats['GoogleDrive']})")
            print(f"🔗 有效链接总数 (Total Links): {len(all_download_links)}")
            print("="*55)
        else:
            print("\n❌ 结束，未提取到任何有效的链接。 (End, no valid links found.)")