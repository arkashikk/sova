"""
Проверка окружения

Запуск из корня проекта: python -m sova.check_env
Скрипт только смотрит и печатает ответ, ничего не меняет в системе
"""

import platform
import shutil
import subprocess
import sys
from importlib import metadata
from pathlib import Path

# Требования
MIN_PYTHON = (3, 13)   # Версия Python
MIN_FREE_GB = 100      # Место под корпуса, индексы и чекпоинты
# Корень проекта
PROJECT_ROOT = Path(__file__).resolve().parent.parent


def report(ok: bool, text: str) -> bool:
    """Строка отчёта и результат проверки"""
    mark = "ОК" if ok else "НЕТ"
    print(f"[{mark}] {text}")
    return ok


def check_python() -> bool:
    ok = sys.version_info[:2] >= MIN_PYTHON
    need = ".".join(map(str, MIN_PYTHON))
    return report(ok, f"Python {platform.python_version()} (нужно {need} или новее)")


def check_venv() -> bool:
    in_venv = sys.prefix != sys.base_prefix
    in_project = Path(sys.prefix).resolve().is_relative_to(PROJECT_ROOT)
    ok = report(in_venv and in_project, f"Виртуальное окружение: {sys.prefix}")
    if not in_venv:
        print("      Запущен глобальный Python: окружение не активировано.")
    elif not in_project:
        print("      Окружение не из этого проекта: проверьте интерпретатор в PyCharm.")
    return ok


def check_utf8() -> bool:
    ok = bool(sys.flags.utf8_mode)
    return report(ok, f"Режим UTF-8 (PYTHONUTF8=1): {'включён' if ok else 'выключен'}")


def check_path() -> bool:
    # Кириллица и пробелы в пути ломают часть инструментов сборки.
    path = str(PROJECT_ROOT)
    ok = path.isascii() and " " not in path
    return report(ok, f"Путь к проекту без кириллицы и без пробелов: {path}")


def check_disk() -> bool:
    free_gb = shutil.disk_usage(PROJECT_ROOT).free / 1024**3
    ok = free_gb >= MIN_FREE_GB
    return report(ok, f"Свободно на диске проекта: {free_gb:.0f} ГБ (нужно {MIN_FREE_GB})")


def check_gpu_driver() -> bool:
    # PyTorch - позже
    exe = shutil.which("nvidia-smi")
    if exe is None:
        return report(False, "nvidia-smi не найден: драйвер NVIDIA не установлен или не в PATH")
    result = subprocess.run(
        [exe, "--query-gpu=name,memory.total,driver_version", "--format=csv,noheader"],
        capture_output=True, text=True, timeout=30,
    )
    ok = result.returncode == 0
    info = (result.stdout if ok else result.stderr).strip()
    return report(ok, f"Видеокарта: {info}")


def show_packages(names: list[str]) -> None:
    print("Пакеты:")
    for name in names:
        try:
            version = metadata.version(name)
        except metadata.PackageNotFoundError:
            version = "не установлен"
        print(f"      {name}: {version}")


def main() -> int:
    print(f"Проверка окружения СОВА · {platform.system()} {platform.release()}")
    checks = [
        check_python(),
        check_venv(),
        check_utf8(),
        check_path(),
        check_disk(),
        check_gpu_driver(),
    ]
    show_packages(["pip", "requests", "pytest", "sova"])
    passed = sum(checks)
    print(f"Итог: {passed} из {len(checks)} проверок пройдено.")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    sys.exit(main())