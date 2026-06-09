# Validador Formal em Tres Niveis

Este repositorio implementa tres reconhecedores manuais em Python:

- `src/regular.py`: DFA para validar o formato `ddd.ddd.ddd-dd`.
- `src/livre_contexto.py`: PDA para balanceamento de `()`, `[]` e `{}`.
- `src/recursiva.py`: Maquina de Turing para `L = { w#w | w pertence a {0,1}* }`.
- `src/recursiva_palindromo.py`: segunda Maquina de Turing para palindromos binarios.
- `src/testes.py`: executor da bateria completa.
- `src/app.py`: interface simples em Streamlit com animacao dos rastros.

## Como executar

Executar a bateria completa:

```bash
python src/testes.py
```

Executar tambem os bonus automatizados:

```bash
python src/testes.py
```

Executar cada reconhecedor individualmente:

```bash
python src/regular.py "123.456.789-00"
python src/livre_contexto.py "((x+y)*z)"
python src/recursiva.py "101#101"
python src/recursiva_palindromo.py "0110"
python src/regular.py "123.456.789-00" --compare-re
```

Executar a interface web:

```bash
pip install -r requirements.txt
streamlit run src/app.py
```

## Bonus implementados

- Interface simples em Streamlit para testar os reconhecedores.
- Visualizacao animada do estado do DFA, da pilha do PDA e da fita das MTs.
- Segunda MT para palindromos binarios.
- Comparacao direta entre o DFA manual e o modulo `re` do Python.
- Documento com a prova de nao-regularidade via Lema do Bombeamento em `BONUS_IMPLEMENTADOS.md`.
```
