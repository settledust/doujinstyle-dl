# Doujinstyle Downloader 🎶

[中文](#中文说明) | [English](#english-description)

---

## 中文说明
一个基于 Python 的全自动 doujinstyle 网盘链接抓取脚本。

### 功能特性
- **Session 复用**：支持 TCP 连接复用，大幅提升抓取速度。
- **智能重定向**：自动捕获 Mega、Mediafire 等网盘的真实下载链接。
- **跨平台适配**：自动处理路径和安全文件名，支持 Windows 和 Linux。

---

## English Description
A Python-based automated crawler for fetching download links from doujinstyle.

### Features
- **Session Reuse**: Implements TCP Keep-Alive for 50%+ speed boost.
- **Smart Redirection**: Automatically catches Location headers for Mega, Mediafire, and Google Drive.
- **Cross-platform**: Handles URL decoding and safe filenames automatically.
