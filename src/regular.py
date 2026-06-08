from __future__ import annotations

import sys
from dataclasses import dataclass


ACCEPTING_STATES = {"q14"}
INITIAL_STATE = "q0"
SYMBOL_CLASSES = {"DIGIT", ".", "-"}

TRANSITIONS = {
    ("q0", "DIGIT"): "q1",
    ("q1", "DIGIT"): "q2",
    ("q2", "DIGIT"): "q3",
    ("q3", "."): "q4",
    ("q4", "DIGIT"): "q5",
    ("q5", "DIGIT"): "q6",
    ("q6", "DIGIT"): "q7",
    ("q7", "."): "q8",
    ("q8", "DIGIT"): "q9",
    ("q9", "DIGIT"): "q10",
    ("q10", "DIGIT"): "q11",
    ("q11", "-"): "q12",
    ("q12", "DIGIT"): "q13",
    ("q13", "DIGIT"): "q14",
}


@dataclass
class TraceStep:
    index: int
    symbol: str
    state_before: str
    state_after: str


def classify_symbol(symbol: str) -> str:
    if symbol.isdigit():
        return "DIGIT"
    if symbol in {".", "-"}:
        return symbol
    return "INVALID"


def recognize(text: str) -> dict:
    state = INITIAL_STATE
    steps = 0
    trace: list[TraceStep] = []

    for index, symbol in enumerate(text):
        symbol_class = classify_symbol(symbol)
        next_state = TRANSITIONS.get((state, symbol_class))
        if next_state is None:
            return {
                "accepted": False,
                "steps": steps,
                "final_state": state,
                "trace": trace,
                "reason": f"Transicao indefinida para estado={state} e simbolo={symbol!r}",
            }

        trace.append(TraceStep(index=index, symbol=symbol, state_before=state, state_after=next_state))
        state = next_state
        steps += 1

    accepted = state in ACCEPTING_STATES
    reason = "Entrada consumida em estado final." if accepted else "Entrada consumida fora de estado final."
    return {
        "accepted": accepted,
        "steps": steps,
        "final_state": state,
        "trace": trace,
        "reason": reason,
    }


def format_result(text: str, result: dict) -> str:
    verdict = "ACEITA" if result["accepted"] else "REJEITA"
    lines = [
        f"Entrada: {text}",
        f"Resultado: {verdict}",
        f"Estado final: {result['final_state']}",
        f"Passos: {result['steps']}",
        f"Motivo: {result['reason']}",
    ]
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print('Uso: python src/regular.py "123.456.789-00"')
        return 1

    text = argv[1]
    result = recognize(text)
    print(format_result(text, result))
    return 0 if result["accepted"] else 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))