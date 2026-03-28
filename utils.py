"""辅助函数"""

import json
from typing import Dict, List, Any


def format_output(
    total_stats: Dict[str, int],
    file_details: List[Dict[str, Any]],
    output_format: str,
    verbose: bool
) -> str:
    """根据格式输出结果"""
    if output_format == "json":
        data = {
            "summary": total_stats,
            "files": file_details if verbose else []
        }
        return json.dumps(data, indent=2)
    else:
        # 表格格式
        lines = []
        lines.append("=" * 70)
        lines.append(f"{'统计项':<20} {'总计':>10} {'代码':>10} {'注释':>10} {'空行':>10}")
        lines.append("-" * 70)
        lines.append(
            f"{'合计':<20} {total_stats['total']:>10} {total_stats['code']:>10} "
            f"{total_stats['comment']:>10} {total_stats['blank']:>10}"
        )
        lines.append("-" * 70)
        lines.append(f"统计文件数: {total_stats['files']}")
        lines.append("=" * 70)

        if verbose and file_details:
            lines.append("\n详细文件列表:")
            lines.append("-" * 70)
            lines.append(f"{'文件路径':<50} {'总计':>6} {'代码':>6} {'注释':>6} {'空行':>6}")
            lines.append("-" * 70)
            for f in file_details:
                lines.append(
                    f"{f['file']:<50} {f['total']:>6} {f['code']:>6} "
                    f"{f['comment']:>6} {f['blank']:>6}"
                )
            lines.append("-" * 70)

        return "\n".join(lines)
