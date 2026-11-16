# СОВА — Система Отбора и Выдачи Ответов

Учебный проект: система отвечает на вопросы по найденным источникам,
все нейросети обучены с нуля.

## Быстрый старт (Windows, PowerShell)

    py -3.13 -m venv .venv
    .\.venv\Scripts\Activate.ps1
    python -m pip install -r requirements-lock.txt
    python -m pip install -r requirements-torch.txtgit
    python -m pip install -e .
    python -m sova.check_env