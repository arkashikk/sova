"""
Тесты репозитория: .gitignore прячет окружение, данные и веса, но не код.
"""

import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent


def is_ignored(path: str) -> bool:
    result = subprocess.run(["git", "check-ignore", "-q", path], cwd=ROOT)
    assert result.returncode in (0, 1), f"git check-ignore вернул {result.returncode}"
    return result.returncode == 0


@pytest.mark.parametrize("path", [
    ".venv/",
    "data/raw.txt",
    "checkpoints/model.pt",
    "sova/__pycache__/check_env.cpython-313.pyc",
])
def test_heavy_and_local_files_are_ignored(path):
    assert is_ignored(path)


@pytest.mark.parametrize("path", [
    "data/.gitkeep",
    "sova/check_env.py",
    "requirements.txt",
])
def test_code_and_markers_are_ignored(path):
    assert not is_ignored(path)
