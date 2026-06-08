# Implementacao de Exemplo do Projeto

## 1. Escopo adotado

Este exemplo resolve o **Tema 1** do enunciado e mantem os tres niveis da hierarquia de Chomsky no mesmo contexto aplicado:

- **LR**: validacao textual de CPF no formato `ddd.ddd.ddd-dd`.
- **LLC**: balanceamento de parenteses, colchetes e chaves em expressoes simbolicas.
- **R**: comparacao de copia exata na linguagem `L = { w#w | w pertence a {0,1}* }`.

O objetivo foi produzir uma base didatica, pequena o bastante para ser lida em sala, mas completa o bastante para mostrar claramente a diferenca entre DFA, PDA e Maquina de Turing.

## 2. Estrutura do repositorio

```text
validador-formal/
├── README.md
├── IMPLEMENTACAO_EXEMPLO.md
├── requirements.txt
├── diagramas/
│   ├── dfa_regular.dot
│   ├── pda_livre_contexto.dot
│   └── mt_recursiva.dot
├── src/
│   ├── regular.py
│   ├── livre_contexto.py
│   ├── recursiva.py
│   └── testes.py
└── testes/
    ├── testes_regular.txt
    ├── testes_livre_contexto.txt
    └── testes_recursiva.txt
```

## 3. Linguagem regular

### 3.1 Descricao

O reconhecedor aceita apenas cadeias com exatamente 14 simbolos no formato:

```text
ddd.ddd.ddd-dd
```

Cada `d` representa um digito decimal. O modelo nao verifica digitos verificadores, apenas o formato.

### 3.2 Definicao formal

$$
L_{LR} = \{ d_1 d_2 d_3 . d_4 d_5 d_6 . d_7 d_8 d_9 - d_{10} d_{11} \mid d_i \in \{0,1,2,3,4,5,6,7,8,9\} \}
$$

### 3.3 Implementacao

O arquivo `src/regular.py` declara:

- estado inicial `q0`;
- estado final `q14`;
- funcao de transicao como um dicionario `TRANSITIONS`;
- simulacao simbolo a simbolo.

Cada passo corresponde a uma leitura de simbolo com mudanca de estado. O contador de passos incrementa uma vez por transicao bem sucedida.

### 3.4 Caminho de execucao

Para a entrada `123.456.789-00`, o DFA percorre:

```text
q0 -> q1 -> q2 -> q3 -> q4 -> q5 -> q6 -> q7 -> q8 -> q9 -> q10 -> q11 -> q12 -> q13 -> q14
```

Total de passos: `14`.

Para `12.34.56-78`, a simulacao trava ao tentar usar `.` a partir de `q2`, porque nesse ponto o automato ainda espera um digito.

## 4. Linguagem livre de contexto

### 4.1 Descricao

O reconhecedor aceita expressoes cujos delimitadores `()`, `[]` e `{}` estejam corretamente balanceados e aninhados. Os demais simbolos da expressao sao ignorados pelo automato, desde que estejam no alfabeto permitido.

### 4.2 Definicao formal

Uma forma equivalente de descrever a linguagem e pela gramatica:

$$
S \to SS \mid (S) \mid [S] \mid \{S\} \mid a \mid \varepsilon
$$

onde $a$ representa qualquer simbolo nao delimitador permitido na expressao.

### 4.3 Implementacao

O arquivo `src/livre_contexto.py` implementa um PDA deterministico simplificado com:

- um estado principal `q_loop`;
- marcador de base da pilha `Z`;
- regras de empilhamento para `(`, `[` e `{`;
- regras de desempilhamento apenas quando o topo combina com `)`, `]` ou `}`;
- uma transicao epsilon final para `q_accept` quando a entrada termina e o topo e `Z`.

As transicoes ficam em uma lista de regras, nao em um encadeamento de `if/else` decisorio do reconhecedor. O programa procura a regra compativel com `(estado, simbolo, topo_da_pilha)` e a aplica.

### 4.4 Passos

Cada caractere consumido conta um passo. A transicao epsilon final de aceitacao tambem conta um passo, pois ainda e uma aplicacao da funcao de transicao do PDA.

### 4.5 Exemplo aceito

Entrada: `((x+y)*z)`

Resumo da pilha:

```text
Z
Z(
Z((
Z((
Z((
Z((
Z(
Z(
Z
aceita por epsilon
```

### 4.6 Exemplo rejeitado

Entrada: `([)]`

Fluxo principal:

```text
le '('  -> empilha '('
le '['  -> empilha '['
le ')'  -> falha, porque o topo atual e '['
```

Nesse ponto, a transicao e indefinida e a cadeia e rejeitada.

## 5. Linguagem recursiva

### 5.1 Descricao

O terceiro reconhecedor verifica se a cadeia possui a forma `w#w`, com `w` binaria. Isso exige memoria mais forte do que uma pilha simples, porque a maquina precisa comparar a parte da esquerda com a da direita na mesma ordem.

### 5.2 Definicao formal

$$
L_R = \{ w\#w \mid w \in \{0,1\}^* \}
$$

### 5.3 Ideia da Maquina de Turing

O arquivo `src/recursiva.py` usa uma fita simples com branco `B` nas extremidades e marcacoes `X` e `Y`:

- `X` marca um `0` ja comparado;
- `Y` marca um `1` ja comparado.

Algoritmo:

1. Encontra o primeiro simbolo nao marcado antes de `#`.
2. Marca esse simbolo na esquerda.
3. Avanca ate `#`.
4. Procura o primeiro simbolo nao marcado na direita.
5. Se o simbolo corresponder, marca e retorna ao inicio.
6. Quando a esquerda termina, verifica se na direita restaram apenas simbolos marcados.

### 5.4 Passos

Cada transicao da MT conta um passo, incluindo leituras com escrita identica e movimento `S` para aceitacao ou rejeicao.

### 5.5 Exemplo aceito

Entrada: `101#101`

Sequencia conceitual:

```text
101#101
Y01#101
Y01#Y01
YY1#Y01
YY1#YY1
YYX#YY1
YYX#YYX
aceita
```

### 5.6 Exemplo rejeitado

Entrada: `101#100`

Nas duas primeiras comparacoes, a maquina consegue casar `1` e `0`. Na comparacao final, o ultimo simbolo esperado e `1`, mas encontra `0`, entrando em `q_reject`.

## 6. Arquivo de testes

O arquivo `src/testes.py`:

- le os arquivos em `testes/`;
- executa cada cadeia no reconhecedor correspondente;
- imprime uma tabela `esperado x obtido`;
- mostra o numero de passos de cada execucao;
- retorna codigo de saida `0` apenas quando toda a bateria passa.

Formato de cada linha dos arquivos de teste:

```text
entrada|ACCEPT ou REJECT|descricao curta
```

## 7. Decisoes de projeto

### 7.1 Por que nao usei `re`

O enunciado exige simulacao explicita do modelo formal. Por isso, o nivel regular nao usa o mecanismo de expressoes regulares do Python como reconhecedor principal.

### 7.2 Por que o PDA usa categoria `OTHER`

Seria pouco didatico listar uma transicao individual para cada letra, digito e operador da expressao. Em vez disso, o codigo classifica esses simbolos como `OTHER` e aplica uma unica regra de permanencia no estado com pilha inalterada.

### 7.3 Por que a MT usa `X` e `Y`

Essas marcas evitam precisar de memoria auxiliar fora da fita. A propria fita registra quais simbolos ja foram comparados, o que torna a implementacao fiel ao modelo de Maquina de Turing.

## 8. Como usar este material em aula

Este repositorio funciona bem como exemplo porque permite discutir:

- por que o DFA resolve o caso de formato fixo;
- por que o balanceamento precisa de pilha;
- por que a linguagem `w#w` excede o poder de um PDA simples;
- como definir `passo` no nivel do modelo formal, e nao no nivel do Python.

Uma estrategia pratica e demonstrar em sala:

```bash
python src/testes.py
python src/regular.py "123.456.789-00"
python src/livre_contexto.py "([)]"
python src/recursiva.py "101#100"
```

Assim, os alunos veem o mesmo projeto rodando em tres niveis diferentes de poder computacional.