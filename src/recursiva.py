from __future__ import annotations

import sys
from dataclasses import dataclass


BLANK = "B"
INITIAL_STATE = "q_start"
ACCEPT_STATE = "q_accept"
REJECT_STATE = "q_reject"

TRANSITIONS = {
    ("q_start", "X"): ("q_start", "X", "R"),
    ("q_start", "Y"): ("q_start", "Y", "R"),
    ("q_start", "0"): ("q_seek_hash_0", "X", "R"),
    ("q_start", "1"): ("q_seek_hash_1", "Y", "R"),
    ("q_start", "#"): ("q_verify_right_done", "#", "R"),
    ("q_start", BLANK): (REJECT_STATE, BLANK, "S"),

    ("q_seek_hash_0", "0"): ("q_seek_hash_0", "0", "R"),
    ("q_seek_hash_0", "1"): ("q_seek_hash_0", "1", "R"),
    ("q_seek_hash_0", "X"): ("q_seek_hash_0", "X", "R"),
    ("q_seek_hash_0", "Y"): ("q_seek_hash_0", "Y", "R"),
    ("q_seek_hash_0", "#"): ("q_seek_match_0", "#", "R"),
    ("q_seek_hash_0", BLANK): (REJECT_STATE, BLANK, "S"),

    ("q_seek_hash_1", "0"): ("q_seek_hash_1", "0", "R"),
    ("q_seek_hash_1", "1"): ("q_seek_hash_1", "1", "R"),
    ("q_seek_hash_1", "X"): ("q_seek_hash_1", "X", "R"),
    ("q_seek_hash_1", "Y"): ("q_seek_hash_1", "Y", "R"),
    ("q_seek_hash_1", "#"): ("q_seek_match_1", "#", "R"),
    ("q_seek_hash_1", BLANK): (REJECT_STATE, BLANK, "S"),

    ("q_seek_match_0", "X"): ("q_seek_match_0", "X", "R"),
    ("q_seek_match_0", "Y"): ("q_seek_match_0", "Y", "R"),
    ("q_seek_match_0", "0"): ("q_return_left", "X", "L"),
    ("q_seek_match_0", "1"): (REJECT_STATE, "1", "S"),
    ("q_seek_match_0", "#"): (REJECT_STATE, "#", "S"),
    ("q_seek_match_0", BLANK): (REJECT_STATE, BLANK, "S"),

    ("q_seek_match_1", "X"): ("q_seek_match_1", "X", "R"),
    ("q_seek_match_1", "Y"): ("q_seek_match_1", "Y", "R"),
    ("q_seek_match_1", "1"): ("q_return_left", "Y", "L"),
    ("q_seek_match_1", "0"): (REJECT_STATE, "0", "S"),
    ("q_seek_match_1", "#"): (REJECT_STATE, "#", "S"),
    ("q_seek_match_1", BLANK): (REJECT_STATE, BLANK, "S"),

    ("q_return_left", "0"): ("q_return_left", "0", "L"),
    ("q_return_left", "1"): ("q_return_left", "1", "L"),
    ("q_return_left", "X"): ("q_return_left", "X", "L"),
    ("q_return_left", "Y"): ("q_return_left", "Y", "L"),
    ("q_return_left", "#"): ("q_return_left", "#", "L"),
    ("q_return_left", BLANK): ("q_start", BLANK, "R"),

    ("q_verify_right_done", "X"): ("q_verify_right_done", "X", "R"),
    ("q_verify_right_done", "Y"): ("q_verify_right_done", "Y", "R"),
    ("q_verify_right_done", "0"): (REJECT_STATE, "0", "S"),
    ("q_verify_right_done", "1"): (REJECT_STATE, "1", "S"),
    ("q_verify_right_done", "#"): (REJECT_STATE, "#", "S"),
    ("q_verify_right_done", BLANK): (ACCEPT_STATE, BLANK, "S"),
}


@dataclass
class TraceStep:
    step: int
    state_before: str
    state_after: str
    head_before: int
    head_after: int
    read_symbol: str
    written_symbol: str
    move: str
    tape: str


def make_tape(text: str) -> list[str]:
    return [BLANK, *text, BLANK]


def validate_alphabet(text: str) -> bool:
    return all(symbol in {"0", "1", "#"} for symbol in text)


def ensure_right_blank(tape: list[str], head: int) -> None:
    if head >= len(tape):
        tape.append(BLANK)


def recognize(text: str) -> dict:
    if not validate_alphabet(text):
        return {
            "accepted": False,
            "steps": 0,
            "final_state": INITIAL_STATE,
            "trace": [],
            "reason": "A entrada deve conter apenas 0, 1 e #.",
        }

    tape = make_tape(text)
    head = 1
    state = INITIAL_STATE
    steps = 0
    trace: list[TraceStep] = []

    while state not in {ACCEPT_STATE, REJECT_STATE}:
        ensure_right_blank(tape, head)
        read_symbol = tape[head]
        transition = TRANSITIONS.get((state, read_symbol))
        if transition is None:
            return {
                "accepted": False,
                "steps": steps,
                "final_state": state,
                "trace": trace,
                "reason": f"Transicao indefinida para estado={state}, simbolo={read_symbol!r}",
            }

        next_state, write_symbol, move = transition
        head_before = head
        tape[head] = write_symbol

        if move == "R":
            head += 1
            ensure_right_blank(tape, head)
        elif move == "L":
            head -= 1
        elif move != "S":
            return {
                "accepted": False,
                "steps": steps,
                "final_state": state,
                "trace": trace,
                "reason": f"Movimento invalido: {move}",
            }

        steps += 1
        trace.append(
            TraceStep(
                step=steps,
                state_before=state,
                state_after=next_state,
                head_before=head_before,
                head_after=head,
                read_symbol=read_symbol,
                written_symbol=write_symbol,
                move=move,
                tape="".join(tape).strip(BLANK),
            )
        )
        state = next_state

    accepted = state == ACCEPT_STATE
    return {
        "accepted": accepted,
        "steps": steps,
        "final_state": state,
        "trace": trace,
        "reason": "A fita foi completamente verificada." if accepted else "A maquina entrou em estado de rejeicao.",
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
        print('Uso: python src/recursiva.py "101#101"')
        return 1

    text = argv[1]
    result = recognize(text)
    print(format_result(text, result))
    return 0 if result["accepted"] else 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))