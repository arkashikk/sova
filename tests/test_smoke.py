"""
Первые тесты: пакет импортируется, а CLI отвечает корректным JSON.
"""

import json
import os
import subprocess
import sys

import sova

QUERY = "Когда основан Казанский университет?"


def test_version_is_ser():
    assert sova.__version__ == "0.1.0"


def test_cli_returns_json_with_query():
    # Запускаем `python -m sova` тем же интерпретатором, что и тесты.
    # PYTHONIOENCODING заставляет дочерний процесс писать в канал в UTF-8.
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    result = subprocess.run(
        [sys.executable, "-m", "sova", QUERY],
        capture_output=True, encoding="utf-8", env=env, timeout=30,
    )
    assert result.returncode == 0, result.stderr
    answer = json.loads(result.stdout)
    assert answer["query"] == QUERY
    assert answer["status"] == "stub"