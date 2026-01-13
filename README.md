# Doujinstyle-dl 🎶

[中文](#中文说明) | [English](#english-description)

---

## 中文说明

**Doujinstyle-dl** 是一个基于 Python 的全自动链接提取工具。它通过模拟用户行为，从 Doujinstyle 批量抓取网盘下载链接。

> [!TIP]
> **定位说明**：本脚本主要负责“自动化检索与链接提取”。提取出的链接汇总在 `.txt` 文件中，建议配合 **JDownloader 2** 或 **IDM** 等工具进行最终的批量下载。

### 功能特性
- **Session 复用**：支持 TCP 连接复用，在大规模抓取时效率提升 50% 以上。
- **智能重定向**：自动解析并捕获 Mega、Mediafire、Google Drive 等网盘的真实跳转链接。
- **跨平台自适应**：支持 Windows/Linux/MacOS 路径，自动处理非法字符并生成安全文件名。

### 如何使用
1. 安装依赖：`pip install requests beautifulsoup4 lxml`
2. 在 `doujinstyle_downloader.py` 中修改 `RESULT_KEYWORD`（如 `c107%20touhou`）。
3. 运行脚本：`python doujinstyle_downloader.py`
4. **下载**：将生成的 `links_*.txt` 文件内容直接粘贴进 JDownloader 2 的“链接抓取器”即可。

---

## English Description

**Doujinstyle-dl** is a Python-based automated link extractor designed to batch-fetch cloud storage links from Doujinstyle.

> [!IMPORTANT]
> **Note**: This script functions as a "Link Extractor." The links are aggregated into a `.txt` file, which is best used with download managers like **JDownloader 2** or **IDM**.

### Features
- **Session Reuse**: Implements TCP Keep-Alive for a 50%+ speed boost during large requests.
- **Smart Redirection**: Automatically catches `Location` headers for Mega, Mediafire, Google Drive links, etc.
- **Cross-platform**: Handles URL decoding and safe filenames for Windows/Linux/MacOS.

### Usage
1. Install dependencies: `pip install requests beautifulsoup4 lxml`
2. Edit `RESULT_KEYWORD` in `doujinstyle_downloader.py`.
3. Run: `python doujinstyle_downloader.py`
4. **Download**: Copy the contents of the generated `links_*.txt` and paste them into JDownloader 2 's LinkGrabber.
