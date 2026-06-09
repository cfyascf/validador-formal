from __future__ import annotations

import time

import livre_contexto
import recursiva
import recursiva_palindromo
import regular
import streamlit as st


RECOGNIZERS = {
    "Linguagem regular (CPF textual)": {
        "runner": regular.recognize,
        "kind": "regular",
        "default": "123.456.789-00",
        "help": "DFA manual para o formato ddd.ddd.ddd-dd.",
    },
    "Linguagem livre de contexto (delimitadores balanceados)": {
        "runner": livre_contexto.recognize,
        "kind": "pda",
        "default": "((x+y)*z)",
        "help": "PDA para balanceamento de (), [] e {}.",
    },
    "Linguagem recursiva (w#w)": {
        "runner": recursiva.recognize,
        "kind": "tm",
        "default": "101#101",
        "help": "MT que compara as duas metades em ordem identica.",
    },
    "Segunda MT bonus (palindromos binarios)": {
        "runner": recursiva_palindromo.recognize,
        "kind": "tm",
        "default": "0110",
        "help": "MT que verifica palindromos sobre {0,1}.",
    },
}


def render_summary(result: dict) -> None:
    col1, col2, col3 = st.columns(3)
    col1.metric("Resultado", "ACEITA" if result["accepted"] else "REJEITA")
    col2.metric("Passos", result["steps"])
    col3.metric("Estado final", result["final_state"])
    st.write("Motivo:", result["reason"])


def render_regular_frame(step_index: int, frame, total_steps: int) -> None:
    st.subheader(f"Passo {step_index} de {total_steps}")
    st.write(f"Simbolo lido: {frame.symbol}")
    st.write(f"Transicao: {frame.state_before} -> {frame.state_after}")


def render_pda_frame(step_index: int, frame, total_steps: int) -> None:
    st.subheader(f"Passo {step_index} de {total_steps}")
    st.write(f"Simbolo: {frame.symbol}")
    st.write(f"Estado: {frame.state_before} -> {frame.state_after}")
    st.write(f"Acao sobre a pilha: {frame.action}")
    st.code(f"Pilha antes: {frame.stack_before}\nPilha depois: {frame.stack_after}")


def render_tm_frame(step_index: int, frame, total_steps: int) -> None:
    st.subheader(f"Passo {step_index} de {total_steps}")
    st.write(f"Estado: {frame.state_before} -> {frame.state_after}")
    st.write(f"Leitura/escrita: {frame.read_symbol} -> {frame.written_symbol}")
    st.write(f"Movimento: {frame.move}")
    st.write(f"Cabeca: {frame.head_before} -> {frame.head_after}")
    st.code(f"Fita visivel: {frame.tape}")


def render_animation(kind: str, trace: list, delay: float) -> None:
    if not trace:
        st.info("Nao ha rastro para animar nessa execucao.")
        return

    placeholder = st.empty()
    for step_index, frame in enumerate(trace, start=1):
        with placeholder.container():
            if kind == "regular":
                render_regular_frame(step_index, frame, len(trace))
            elif kind == "pda":
                render_pda_frame(step_index, frame, len(trace))
            else:
                render_tm_frame(step_index, frame, len(trace))
        time.sleep(delay)


def build_trace_text(kind: str, trace: list) -> str:
    lines: list[str] = []
    if kind == "regular":
        for index, frame in enumerate(trace, start=1):
            lines.append(f"{index}. simbolo={frame.symbol} : {frame.state_before} -> {frame.state_after}")
    elif kind == "pda":
        for index, frame in enumerate(trace, start=1):
            lines.append(
                f"{index}. simbolo={frame.symbol} : {frame.state_before} -> {frame.state_after} | pilha {frame.stack_before} -> {frame.stack_after} | acao={frame.action}"
            )
    else:
        for frame in trace:
            lines.append(
                f"{frame.step}. {frame.state_before} -> {frame.state_after} | le={frame.read_symbol} escreve={frame.written_symbol} move={frame.move} | fita={frame.tape}"
            )
    return "\n".join(lines)


def main() -> None:
    st.set_page_config(page_title="Validador Formal", layout="wide")
    st.title("Validador Formal em Tres Niveis")
    st.write("Interface de demonstracao para o DFA, o PDA e as duas Maquinas de Turing do projeto.")

    selected_name = st.selectbox("Escolha o reconhecedor", list(RECOGNIZERS.keys()))
    config = RECOGNIZERS[selected_name]
    st.caption(config["help"])

    text = st.text_input("Cadeia de entrada", value=config["default"])
    animate = st.checkbox("Animar rastro", value=True)
    delay = st.slider("Atraso entre passos (segundos)", min_value=0.05, max_value=1.00, value=0.20, step=0.05)

    if st.button("Executar reconhecedor", type="primary"):
        result = config["runner"](text)
        render_summary(result)

        if config["kind"] == "regular":
            comparison = regular.compare_with_regex(text)
            st.write("Comparacao manual x re:")
            st.code(
                f"manual = {'ACEITA' if comparison['manual']['accepted'] else 'REJEITA'}\n"
                f"re     = {'ACEITA' if comparison['regex_accepted'] else 'REJEITA'}\n"
                f"equivalente = {'SIM' if comparison['equivalent'] else 'NAO'}"
            )

        st.divider()
        if animate:
            render_animation(config["kind"], result["trace"], delay)

        st.subheader("Rastro completo")
        st.code(build_trace_text(config["kind"], result["trace"]))


if __name__ == "__main__":
    main()