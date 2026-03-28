# CodeStats – 代码统计工具

CodeStats 是一个轻量级的命令行工具，用于统计代码仓库中的行数信息。它支持递归扫描目录，统计指定扩展名文件的总行数、代码行数、注释行数和空行数，并可以输出为表格或 JSON 格式。

## 功能特点

- 统计指定目录下所有匹配扩展名的文件
- 支持排除特定目录（如 `.git`、`venv`）
- 支持多种输出格式：表格、JSON
- 可显示每个文件的详细统计信息
- 处理 Python 文件时能识别单行注释 (`#`) 和多行注释 (`""" ... """`)

## 安装

### 通过 pip 安装

```bash
pip install git+https://github.com/HomiyaTamamo/codestats.git
