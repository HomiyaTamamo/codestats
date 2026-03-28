#!/usr/bin/env python3
"""命令行入口"""

import argparse
import sys
from pathlib import Path

from .core import count_lines_in_directory
from .utils import format_output


def main():
    parser = argparse.ArgumentParser(
        description="统计代码仓库中的行数信息"
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="要统计的目录路径 (默认: 当前目录)"
    )
    parser.add_argument(
        "-e", "--ext",
        nargs="+",
        default=[".py"],
        help="要统计的文件扩展名 (默认: .py)"
    )
    parser.add_argument(
        "-x", "--exclude",
        nargs="+",
        default=[".git", "__pycache__", "venv", "env", ".idea"],
        help="要排除的目录名 (默认: .git, __pycache__, venv, env, .idea)"
    )
    parser.add_argument(
        "-o", "--output",
        choices=["table", "json"],
        default="table",
        help="输出格式 (默认: table)"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="显示详细统计信息 (每个文件)"
    )
    args = parser.parse_args()

    root_path = Path(args.path).resolve()
    if not root_path.is_dir():
        print(f"错误: {root_path} 不是一个有效的目录", file=sys.stderr)
        sys.exit(1)

    try:
        stats, file_stats = count_lines_in_directory(
            root_path,
            extensions=args.ext,
            exclude_dirs=args.exclude,
            verbose=args.verbose
        )
    except Exception as e:
        print(f"统计过程中出错: {e}", file=sys.stderr)
        sys.exit(1)

    output = format_output(stats, file_stats, args.output, args.verbose)
    print(output)


if __name__ == "__main__":
    main()
