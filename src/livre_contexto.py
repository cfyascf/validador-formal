from __future__ import annotations

import sys
from dataclasses import dataclass


INITIAL_STATE = "q_loop"
FINAL_STATE = "q_accept"
STACK_BOTTOM = "Z"
OPENERS = {"(", "[", "{"}
CLOSERS = {")": "(", "]": "[", "}": "{",
}
ALLOWED_OTHER = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+-*/^_=,.;: <>!?")

TRANSITIONS = [
    {"state": "q_loop", "input": "(", "stack_top": "*", "next": "q_loop", "action": ("push", "(")},
    {"state": "q_loop", "input": "[", "stack_top": "*", "next": "q_loop", "action": ("push", "[")},
    {"state": "q_loop", "input": "{", "stack_top": "*", "next": "q_loop", "action": ("push", "{")},
    {"state": "q_loop", "input": ")", "stack_top": "(", "next": "q_loop", "action": ("pop", None)},
    {"state": "q_loop", "input": "]", "stack_top": "[", "next": "q_loop", "action": ("pop", None)},
    {"state": "q_loop", "input": "}", "stack_top": "{", "next": "q_loop", "action": ("pop", None)},
    {"state": "q_loop", "input": "OTHER", "stack_top": "*", "next": "q_loop", "action": ("noop", None)},
    {"state": "q_loop", "input": "EPSILON", "stack_top": "Z", "next": "q_accept", "action": ("noop", None)},
]


@dataclass
class TraceStep:
    position: int
    symbol: str
    state_before: str
    state_after: str
    stack_before: str
    stack_after: str
    action: str


def classify_symbol(symbol: str) -> str:
    if symbol in OPENERS or symbol in CLOSERS:
        return symbol
    if symbol in ALLOWED_OTHER or symbol.isspace():
        return "OTHER"
    return "INVALID"


def find_transition(state: str, input_symbol: str, stack_top: str) -> dict | None:
    for rule in TRANSITIONS:
        if rule["state"] != state:
            continue
        if rule["input"] != input_symbol:
            continue
        if rule["stack_top"] not in {stack_top, "*"}:
            continue
        return rule
    return None


def apply_action(stack: list[str], action: tuple[str, str | None]) -> None:
    kind, value = action
    if kind == "push" and value is not None:
        stack.append(value)
    elif kind == "pop":
        stack.pop()


def recognize(text: str) -> dict:
    state = INITIAL_STATE
    stack = [STACK_BOTTOM]
    steps = 0
    trace: list[TraceStep] = []

    for position, symbol in enumerate(text):
        stack_before = "".join(stack)
        input_symbol = classify_symbol(symbol)
        if input_symbol == "INVALID":
            return {
                "accepted": False,
                "steps": steps,
                "final_state": state,
                "trace": trace,
                "reason": f"Simbolo invalido: {symbol!r}",
            }

        rule = find_transition(state, input_symbol, stack[-1])
        if rule is None:
            return {
                "accepted": False,
                "steps": steps,
                "final_state": state,
                "trace": trace,
                "reason": f"Transicao indefinida para estado={state}, simbolo={symbol!r}, topo={stack[-1]!r}",
            }

        apply_action(stack, rule["action"])
        steps += 1
        trace.append(
            TraceStep(
                position=position,
                symbol=symbol,
                state_before=state,
                state_after=rule["next"],
                stack_before=stack_before,
                stack_after="".join(stack),
                action=rule["action"][0],
            )
        )
        state = rule["next"]

    epsilon_rule = find_transition(state, "EPSILON", stack[-1])
    if epsilon_rule is None:
        return {
            "accepted": False,
            "steps": steps,
            "final_state": state,
            "trace": trace,
            "reason": f"Fim da entrada com pilha remanescente: {''.join(stack)}",
        }

    stack_before = "".join(stack)
    apply_action(stack, epsilon_rule["action"])
    steps += 1
    trace.append(
        TraceStep(
            position=len(text),
            symbol="EPSILON",
            state_before=state,
            state_after=epsilon_rule["next"],
            stack_before=stack_before,
            stack_after="".join(stack),
            action=epsilon_rule["action"][0],
        )
    )
    state = epsilon_rule["next"]

    return {
        "accepted": state == FINAL_STATE,
        "steps": steps,
        "final_state": state,
        "trace": trace,
        "reason": "Pilha esvaziada ate o marcador de base." if state == FINAL_STATE else "Estado final nao alcancado.",
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
        print('Uso: python src/livre_contexto.py "((x+y)*z)"')
        return 1

    text = argv[1]
    result = recognize(text)
    print(format_result(text, result))
    return 0 if result["accepted"] else 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))