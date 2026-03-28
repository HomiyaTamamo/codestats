"""核心统计逻辑"""

from pathlib import Path
from typing import List, Tuple, Dict, Optional


def count_lines_in_file(file_path: Path) -> Tuple[int, int, int, int]:
    """
    统计单个文件的行数信息
    返回: (总行数, 代码行数, 注释行数, 空行数)
    """
    total = code = comment = blank = 0
    in_multiline_comment = False

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                total += 1
                stripped = line.strip()

                # 空行
                if not stripped:
                    blank += 1
                    continue

                # 多行注释检测 (简单处理，假设用 """ 或 ''')
                # 实际生产环境可能需要更精确的解析，此处做简化
                # 这里只处理 Python 的 triple quotes
                if '"""' in line or "'''" in line:
                    # 如果行内包含多行注释开始或结束
                    count = line.count('"""') + line.count("'''")
                    if count % 2 == 1:
                        in_multiline_comment = not in_multiline_comment
                    # 如果该行既有开始也有结束，且仍在注释中，需调整
                    # 为简化，若行内包含多行注释，则视为注释行
                    comment += 1
                    continue

                if in_multiline_comment:
                    comment += 1
                    continue

                # 单行注释
                if stripped.startswith("#"):
                    comment += 1
                else:
                    code += 1

    except Exception as e:
        # 如果文件无法读取，返回全0并记录警告
        print(f"警告: 无法读取文件 {file_path}: {e}")
        return (0, 0, 0, 0)

    return (total, code, comment, blank)


def count_lines_in_directory(
    root_dir: Path,
    extensions: List[str],
    exclude_dirs: List[str],
    verbose: bool = False
) -> Tuple[Dict[str, int], List[Dict[str, any]]]:
    """
    递归统计目录下所有匹配扩展名的文件
    返回: (总计字典, 文件列表详情)
    """
    total_stats = {"total": 0, "code": 0, "comment": 0, "blank": 0, "files": 0}
    file_details = []

    for path in root_dir.rglob("*"):
        # 跳过排除的目录
        if any(part in exclude_dirs for part in path.parts):
            continue

        if path.is_file() and path.suffix in extensions:
            try:
                t, c, cm, b = count_lines_in_file(path)
                rel_path = path.relative_to(root_dir)
                file_stats = {
                    "file": str(rel_path),
                    "total": t,
                    "code": c,
                    "comment": cm,
                    "blank": b,
                }
                file_details.append(file_stats)

                total_stats["total"] += t
                total_stats["code"] += c
                total_stats["comment"] += cm
                total_stats["blank"] += b
                total_stats["files"] += 1

                if verbose:
                    print(f"处理: {rel_path} | 代码: {c} 注释: {cm} 空行: {b} 总计: {t}")

            except Exception as e:
                print(f"处理文件 {path} 时出错: {e}")

    return total_stats, file_details
