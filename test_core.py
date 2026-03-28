import tempfile
from pathlib import Path
import pytest

from codestats.core import count_lines_in_file, count_lines_in_directory


def test_count_lines_in_file():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write("# comment\n")
        f.write("def foo():\n")
        f.write("    pass\n")
        f.write("\n")
        f.write("# another comment\n")
        f.write("x = 1\n")
        f.write("'''\n")
        f.write("multiline\n")
        f.write("'''\n")
        f.write("y = 2\n")
        f.write("\n")
        f.write("\n")
        f.write("# last comment\n")
        f.write("print('done')\n")
        tmp_path = Path(f.name)

    total, code, comment, blank = count_lines_in_file(tmp_path)

    # 预期: 总行数 13 (包括所有行)
    # 代码行: def foo():,     pass, x=1, y=2, print('done')  => 5
    # 注释行: # comment, # another comment, ''' ... ''' 整个多行块算作3行注释? 实现中将多行注释的每行都计为注释，所以这里多行注释有3行
    # 加上 # last comment => 总共 1+1+3+1=6 行注释
    # 空行: 2 个空行
    assert total == 13
    assert code == 5
    assert comment == 6
    assert blank == 2

    tmp_path.unlink()


def test_count_lines_in_directory():
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        # 创建测试文件结构
        file1 = root / "test1.py"
        file1.write_text("# comment\nprint('hello')\n\n")
        file2 = root / "test2.py"
        file2.write_text("def add(a,b):\n    return a+b\n")
        sub = root / "subdir"
        sub.mkdir()
        file3 = sub / "test3.py"
        file3.write_text("x=1\ny=2\n# comment\n")

        # 创建一个不应被统计的 .txt 文件
        (root / "ignore.txt").write_text("ignore")

        stats, details = count_lines_in_directory(
            root,
            extensions=[".py"],
            exclude_dirs=[".git", "__pycache__"]
        )

        # 期望: 3个文件
        assert stats["files"] == 3
        # 总行数: file1: 3行, file2: 2行, file3: 3行 => 8
        assert stats["total"] == 8
        # 代码行: file1: 1, file2: 2, file3: 2 => 5
        assert stats["code"] == 5
        # 注释行: file1: 1, file2: 0, file3: 1 => 2
        assert stats["comment"] == 2
        # 空行: file1: 1, file2: 0, file3: 0 => 1
        assert stats["blank"] == 1
