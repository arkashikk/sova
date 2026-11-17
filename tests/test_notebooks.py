"""Ноутбуки хранятся в Git без выводов: только код и текст."""

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
NOTEBOOKS = sorted((ROOT / "notebooks").glob("*.ipynb"))


@pytest.mark.parametrize("path", NOTEBOOKS, ids=lambda p: p.name)
def test_notebook_has_no_outputs(path):
    # .ipynb — это JSON: список ячеек, у ячеек с кодом есть outputs и execution_count.
    notebook = json.loads(path.read_text(encoding="utf-8"))
    for number, cell in enumerate(notebook["cells"], start=1):
        if cell["cell_type"] != "code":
            continue
        assert not cell["outputs"], f"ячейка {number}: есть вывод — очистите выводы перед коммитом"
        assert cell["execution_count"] is None, f"ячейка {number}: остался номер запуска"