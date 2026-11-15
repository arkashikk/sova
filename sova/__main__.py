"""
Точка входа: команда python -m sova "вопрос"

Пока заглушка: принимает запрос и печатает JSON без ответа.
"""

import argparse
import json

from sova import __version__

def build_parser() -> argparse.ArgumentParser:
    """Описываем аргументы каждой строки"""
    parser = argparse.ArgumentParser(
        prog="sova",
        description="СОВА отвечает на вопросы, опираясь на найденные источники.",
    )
    parser.add_argument("query", help="вопрос на русском языке, в кавычках")
    parser.add_argument("--version", action="version", version=f"sova {__version__}")
    return parser


def main() -> None:
    args = build_parser().parse_args()

    answer = {
        "query": args.query,
        "short_answer": None,   # Отвечать пока нечем
        "key_points": [],
        "sources": [],
        "status": "stub",       # Заглушка
    }
    # ensure_ascii=False печатает кириллицу как есть, а не \u041a...
    print(json.dumps(answer, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()