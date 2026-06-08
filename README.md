# Validador Formal em Tres Niveis

Exemplo de referencia do Tema 1 do projeto de Modelagem Computacional.

Este repositorio implementa tres reconhecedores manuais em Python:

- `src/regular.py`: DFA para validar o formato `ddd.ddd.ddd-dd`.
- `src/livre_contexto.py`: PDA para balanceamento de `()`, `[]` e `{}`.
- `src/recursiva.py`: Maquina de Turing para `L = { w#w | w pertence a {0,1}* }`.
- `src/testes.py`: executor da bateria completa.

## Como executar

Executar a bateria completa:

```bash
python src/testes.py
```

Executar cada reconhecedor individualmente:

```bash
python src/regular.py "123.456.789-00"
python src/livre_contexto.py "((x+y)*z)"
python src/recursiva.py "101#101"
```

## Estrutura

```text
.
├── README.md
├── IMPLEMENTACAO_EXEMPLO.md
├── requirements.txt
├── diagramas/
├── src/
└── testes/
```

Os diagramas foram entregues em Graphviz `.dot` para facilitar adaptacoes ou exportacao futura.