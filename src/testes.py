from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import livre_contexto
import recursiva
import recursiva_palindromo
import regular


BASE_DIR = Path(__file__).resolve().parent.parent
TESTS_DIR = BASE_DIR / "testes"


@dataclass
class TestCase:
    text: str
    expected: bool
    description: str


RECOGNIZERS = {
    "regular": (regular.recognize, TESTS_DIR / "testes_regular.txt"),
    "livre_contexto": (livre_contexto.recognize, TESTS_DIR / "testes_livre_contexto.txt"),
    "recursiva": (recursiva.recognize, TESTS_DIR / "testes_recursiva.txt"),
}

BONUS_RECOGNIZERS = {
    "recursiva_palindromo": (recursiva_palindromo.recognize, TESTS_DIR / "testes_recursiva_palindromo.txt"),
}


def parse_expected(raw: str) -> bool:
    normalized = raw.strip().upper()
    if normalized == "ACCEPT":
        return True
    if normalized == "REJECT":
        return False
    raise ValueError(f"Valor esperado invalido: {raw}")


def load_cases(path: Path) -> list[TestCase]:
    cases: list[TestCase] = []
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("#") and not line.startswith("#|"):
            continue
        text, expected, description = [part.strip() for part in line.split("|", maxsplit=2)]
        cases.append(TestCase(text=text, expected=parse_expected(expected), description=description))
    return cases


def verdict_label(value: bool) -> str:
    return "ACEITA" if value else "REJEITA"


def print_header(title: str) -> None:
    print(f"\n=== {title.upper()} ===")
    print(f"{'Entrada':<18} {'Esperado':<10} {'Obtido':<10} {'Passos':<8} Descricao")
    print("-" * 80)


def run_suite(name: str, recognizer, path: Path) -> bool:
    print_header(name)
    suite_ok = True
    for case in load_cases(path):
        result = recognizer(case.text)
        obtained = result["accepted"]
        suite_ok = suite_ok and obtained == case.expected
        print(
            f"{case.text:<18} {verdict_label(case.expected):<10} {verdict_label(obtained):<10} {result['steps']:<8} {case.description}"
        )
    return suite_ok


def run_regex_comparison() -> bool:
    print_header("comparacao_regular_re")
    suite_ok = True
    for case in load_cases(TESTS_DIR / "testes_regular.txt"):
        comparison = regular.compare_with_regex(case.text)
        obtained = comparison["manual"]["accepted"]
        regex_accepted = comparison["regex_accepted"]
        equivalent = comparison["equivalent"]
        suite_ok = suite_ok and equivalent and obtained == case.expected
        regex_label = verdict_label(regex_accepted)
        print(
            f"{case.text:<18} {verdict_label(case.expected):<10} {regex_label:<10} {comparison['manual']['steps']:<8} manual x re = {'OK' if equivalent else 'DIVERGE'}"
        )
    return suite_ok


def main() -> int:
    global_ok = True
    for name, (recognizer, path) in RECOGNIZERS.items():
        global_ok = run_suite(name, recognizer, path) and global_ok

    bonus_ok = True
    for name, (recognizer, path) in BONUS_RECOGNIZERS.items():
        bonus_ok = run_suite(name, recognizer, path) and bonus_ok

    regex_ok = run_regex_comparison()

    global_ok = global_ok and bonus_ok and regex_ok

    print("\nResultado final:", "TODOS OS TESTES PASSARAM" if global_ok else "HOUVE FALHAS")
    return 0 if global_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())