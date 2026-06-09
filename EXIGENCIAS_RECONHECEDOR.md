# Exigências de Cada Reconhecedor

## 1. Linguagem regular

### 1.1 Descricao em portugues da linguagem

O reconhecedor aceita apenas cadeias com exatamente 14 simbolos no formato:

```text
ddd.ddd.ddd-dd
```

Cada `d` representa um digito decimal. O modelo nao verifica digitos verificadores, apenas o formato.

### 1.2 Definicao formal em notacao matematica

$$
L_{LR} = \{ d_1 d_2 d_3 . d_4 d_5 d_6 . d_7 d_8 d_9 - d_{10} d_{11} \mid d_i \in \{0,1,2,3,4,5,6,7,8,9\} \}
$$

### 1.3 Alfabeto utilizado

O alfabeto de entrada da linguagem regular e:

$$
\Sigma_{LR} = \{0,1,2,3,4,5,6,7,8,9,.,-\}
$$

No codigo, os simbolos sao classificados em tres classes relevantes para o DFA:

- `DIGIT` para qualquer digito de `0` a `9`.
- `.` para o separador entre o terceiro e o quarto, e entre o sexto e o setimo digitos.
- `-` para o separador antes dos dois ultimos digitos.

### 1.4 Exemplos de cadeias rejeitadas e aceitas

Exemplos aceitos:

- `123.456.789-00`
- `000.111.222-33`
- `999.999.999-99`

Exemplos rejeitados:

- `12.34.56-78`, porque faltam digitos em cada bloco.
- `12345678900`, porque nao ha separadores.
- `123.456.789.00`, porque o ultimo separador deveria ser `-`.

### 1.5 Modelo computacional escolhido com tabela de transição completa (DFA, MT) ou transições principais com evolução da pilha (PDA), acompanhado de diagrama

O modelo escolhido foi um **DFA** com estado inicial `q0`, estado final `q14` e uma transicao por simbolo consumido. O diagrama correspondente esta em `diagramas/dfa_regular.dot`.

Tabela completa de transicoes:

| Estado atual | Simbolo lido | Proximo estado |
| --- | --- | --- |
| `q0` | `DIGIT` | `q1` |
| `q1` | `DIGIT` | `q2` |
| `q2` | `DIGIT` | `q3` |
| `q3` | `.` | `q4` |
| `q4` | `DIGIT` | `q5` |
| `q5` | `DIGIT` | `q6` |
| `q6` | `DIGIT` | `q7` |
| `q7` | `.` | `q8` |
| `q8` | `DIGIT` | `q9` |
| `q9` | `DIGIT` | `q10` |
| `q10` | `DIGIT` | `q11` |
| `q11` | `-` | `q12` |
| `q12` | `DIGIT` | `q13` |
| `q13` | `DIGIT` | `q14` |

Qualquer combinacao ausente dessa tabela e rejeitada por transicao indefinida.

### 1.6 Execução passo a passo de uma cadeia aceita e uma rejeitada

#### 1.6.1 Execucao passo a passo de uma cadeia aceita

Entrada: `123.456.789-00`

| Passo | Simbolo | Estado antes | Estado depois |
| --- | --- | --- | --- |
| 1 | `1` | `q0` | `q1` |
| 2 | `2` | `q1` | `q2` |
| 3 | `3` | `q2` | `q3` |
| 4 | `.` | `q3` | `q4` |
| 5 | `4` | `q4` | `q5` |
| 6 | `5` | `q5` | `q6` |
| 7 | `6` | `q6` | `q7` |
| 8 | `.` | `q7` | `q8` |
| 9 | `7` | `q8` | `q9` |
| 10 | `8` | `q9` | `q10` |
| 11 | `9` | `q10` | `q11` |
| 12 | `-` | `q11` | `q12` |
| 13 | `0` | `q12` | `q13` |
| 14 | `0` | `q13` | `q14` |

Ao fim da entrada, o automato esta em `q14`, que e estado final. Portanto, a cadeia e aceita em `14` passos.

#### 1.6.2 Execucao passo a passo de uma cadeia rejeitada

Entrada: `12.34.56-78`

| Passo | Simbolo | Estado antes | Estado depois |
| --- | --- | --- | --- |
| 1 | `1` | `q0` | `q1` |
| 2 | `2` | `q1` | `q2` |

No terceiro simbolo, o automato le `.` ainda em `q2`. Nao existe transicao `(q2, '.')`, porque nessa posicao o DFA ainda espera o terceiro digito do primeiro bloco. Logo, a cadeia e rejeitada apos `2` passos validos.

---

## 2. Linguagem livre de contexto

### 2.1 Descricao em portugues da linguagem

O reconhecedor aceita expressoes cujos delimitadores `()`, `[]` e `{}` estejam corretamente balanceados e aninhados. Os demais simbolos da expressao sao ignorados pelo automato, desde que estejam no alfabeto permitido.

### 2.2 Definicao formal em notacao matematica

Uma forma equivalente de descrever a linguagem e pela gramatica:

$$
S \to SS \mid (S) \mid [S] \mid \{S\} \mid a \mid \varepsilon
$$

onde $a$ representa qualquer simbolo nao delimitador permitido na expressao.

### 2.3 Alfabeto utilizado

O alfabeto de entrada desse reconhecedor e composto por tres grupos:

$$
\Sigma_{LLC} = \{(,),[,],\{,\}\} \cup A
$$

onde $A$ representa os demais simbolos permitidos na expressao. Na implementacao, esse conjunto inclui:

- letras maiusculas e minusculas;
- digitos de `0` a `9`;
- operadores e separadores como `+`, `-`, `*`, `/`, `^`, `_`, `=`, `,`, `.`, `;`, `:`, `<`, `>`, `!`, `?`;
- espaco em branco.

O alfabeto da pilha e:

$$
\Gamma_{LLC} = \{Z,(,[,\{\}
$$

em que `Z` e o marcador de base da pilha.

### 2.4 Exemplos de cadeias rejeitadas e aceitas

Exemplos aceitos:

- `((x+y)*z)`
- `{[a+(b*c)]}`
- cadeia vazia `""`

Exemplos rejeitados:

- `((a+b)`, porque sobra um delimitador aberto ao fim da entrada.
- `([)]`, porque a ordem de fechamento nao respeita o aninhamento.
- `{a+b]]`, porque `]` tenta fechar um `[` que nunca foi aberto naquele topo.

### 2.5 Modelo computacional escolhido com tabela de transição completa (DFA, MT) ou transições principais com evolução da pilha (PDA), acompanhado de diagrama

O modelo escolhido foi um **PDA** com estado principal `q_loop`, estado final `q_accept` e marcador de base `Z`. O diagrama correspondente esta em `diagramas/pda_livre_contexto.dot`.

Como se trata de PDA, o mais importante e explicitar as transicoes principais junto com a evolucao da pilha:

| Estado | Simbolo de entrada | Topo da pilha | Acao | Proximo estado |
| --- | --- | --- | --- | --- |
| `q_loop` | `(` | `*` | empilha `(` | `q_loop` |
| `q_loop` | `[` | `*` | empilha `[` | `q_loop` |
| `q_loop` | `{` | `*` | empilha `{` | `q_loop` |
| `q_loop` | `)` | `(` | desempilha | `q_loop` |
| `q_loop` | `]` | `[` | desempilha | `q_loop` |
| `q_loop` | `}` | `{` | desempilha | `q_loop` |
| `q_loop` | `OTHER` | `*` | nenhuma alteracao | `q_loop` |
| `q_loop` | `EPSILON` | `Z` | nenhuma alteracao | `q_accept` |

O simbolo `*` significa que a regra vale para qualquer topo de pilha. Qualquer tentativa de fechar um delimitador com topo incompatível leva a rejeicao por ausencia de transicao.

### 2.6 Execução passo a passo de uma cadeia aceita e uma rejeitada

#### 2.6.1 Execução passo a passo de uma cadeia aceita

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

#### 2.6.2 Execução passo a passo de uma cadeia rejeitada

Entrada: `([)]`

Fluxo principal:

```text
le '('  -> empilha '('
le '['  -> empilha '['
le ')'  -> falha, porque o topo atual e '['
```

Nesse ponto, a transicao e indefinida e a cadeia e rejeitada.

Uma forma tabular de ver o mesmo processo e:

| Passo | Simbolo | Pilha antes | Acao | Pilha depois |
| --- | --- | --- | --- | --- |
| 1 | `(` | `Z` | push `(` | `Z(` |
| 2 | `[` | `Z(` | push `[` | `Z([` |
| 3 | `)` | `Z([` | falha, topo esperado `(` | rejeita |

---

## 3. Linguagem recursiva

### 3.1 Descricao em portugues da linguagem

O terceiro reconhecedor verifica se a cadeia possui a forma `w#w`, com `w` binaria. Isso exige memoria mais forte do que uma pilha simples, porque a maquina precisa comparar a parte da esquerda com a da direita na mesma ordem.

### 3.2 Definicao formal em notacao matematica

$$
L_R = \{ w\#w \mid w \in \{0,1\}^* \}
$$

### 3.3 Alfabeto utilizado

O alfabeto de entrada da linguagem recursiva e:

$$
\Sigma_R = \{0,1,\#\}
$$

Como a implementacao e uma Maquina de Turing, tambem existe um alfabeto de fita mais amplo:

$$
\Gamma_R = \{0,1,\#,X,Y,B\}
$$

onde:

- `X` marca um `0` da esquerda ou da direita que ja foi comparado;
- `Y` marca um `1` da esquerda ou da direita que ja foi comparado;
- `B` representa branco.

### 3.4 Exemplos de cadeias rejeitadas e aceitas

Exemplos aceitos:

- `#`, caso em que `w = \varepsilon`
- `0#0`
- `101#101`

Exemplos rejeitados:

- `1#0`, porque os lados nao coincidem.
- `101#100`, porque o ultimo simbolo da copia difere.
- `10#010`, porque a segunda metade nao e a mesma cadeia na mesma ordem.

### 3.5 Modelo computacional escolhido com tabela de transição completa (DFA, MT) ou transições principais com evolução da pilha (PDA), acompanhado de diagrama

O modelo escolhido foi uma **Maquina de Turing deterministica** de uma fita. O diagrama correspondente esta em `diagramas/mt_recursiva.dot`.

Tabela de transicoes organizada por estado:

| Estado atual | Simbolo lido | Escreve | Move | Proximo estado |
| --- | --- | --- | --- | --- |
| `q_start` | `X` | `X` | `R` | `q_start` |
| `q_start` | `Y` | `Y` | `R` | `q_start` |
| `q_start` | `0` | `X` | `R` | `q_seek_hash_0` |
| `q_start` | `1` | `Y` | `R` | `q_seek_hash_1` |
| `q_start` | `#` | `#` | `R` | `q_verify_right_done` |
| `q_start` | `B` | `B` | `S` | `q_reject` |
| `q_seek_hash_0` | `0` | `0` | `R` | `q_seek_hash_0` |
| `q_seek_hash_0` | `1` | `1` | `R` | `q_seek_hash_0` |
| `q_seek_hash_0` | `X` | `X` | `R` | `q_seek_hash_0` |
| `q_seek_hash_0` | `Y` | `Y` | `R` | `q_seek_hash_0` |
| `q_seek_hash_0` | `#` | `#` | `R` | `q_seek_match_0` |
| `q_seek_hash_0` | `B` | `B` | `S` | `q_reject` |
| `q_seek_hash_1` | `0` | `0` | `R` | `q_seek_hash_1` |
| `q_seek_hash_1` | `1` | `1` | `R` | `q_seek_hash_1` |
| `q_seek_hash_1` | `X` | `X` | `R` | `q_seek_hash_1` |
| `q_seek_hash_1` | `Y` | `Y` | `R` | `q_seek_hash_1` |
| `q_seek_hash_1` | `#` | `#` | `R` | `q_seek_match_1` |
| `q_seek_hash_1` | `B` | `B` | `S` | `q_reject` |
| `q_seek_match_0` | `X` | `X` | `R` | `q_seek_match_0` |
| `q_seek_match_0` | `Y` | `Y` | `R` | `q_seek_match_0` |
| `q_seek_match_0` | `0` | `X` | `L` | `q_return_left` |
| `q_seek_match_0` | `1` | `1` | `S` | `q_reject` |
| `q_seek_match_0` | `#` | `#` | `S` | `q_reject` |
| `q_seek_match_0` | `B` | `B` | `S` | `q_reject` |
| `q_seek_match_1` | `X` | `X` | `R` | `q_seek_match_1` |
| `q_seek_match_1` | `Y` | `Y` | `R` | `q_seek_match_1` |
| `q_seek_match_1` | `1` | `Y` | `L` | `q_return_left` |
| `q_seek_match_1` | `0` | `0` | `S` | `q_reject` |
| `q_seek_match_1` | `#` | `#` | `S` | `q_reject` |
| `q_seek_match_1` | `B` | `B` | `S` | `q_reject` |
| `q_return_left` | `0` | `0` | `L` | `q_return_left` |
| `q_return_left` | `1` | `1` | `L` | `q_return_left` |
| `q_return_left` | `X` | `X` | `L` | `q_return_left` |
| `q_return_left` | `Y` | `Y` | `L` | `q_return_left` |
| `q_return_left` | `#` | `#` | `L` | `q_return_left` |
| `q_return_left` | `B` | `B` | `R` | `q_start` |
| `q_verify_right_done` | `X` | `X` | `R` | `q_verify_right_done` |
| `q_verify_right_done` | `Y` | `Y` | `R` | `q_verify_right_done` |
| `q_verify_right_done` | `0` | `0` | `S` | `q_reject` |
| `q_verify_right_done` | `1` | `1` | `S` | `q_reject` |
| `q_verify_right_done` | `#` | `#` | `S` | `q_reject` |
| `q_verify_right_done` | `B` | `B` | `S` | `q_accept` |

Em termos intuitivos, a maquina marca um simbolo ainda nao processado na esquerda, atravessa o `#`, procura o correspondente na direita, marca, volta ao inicio e repete o processo.

### 3.6 Execução passo a passo de uma cadeia aceita e uma rejeitada

#### 3.6.1 Execução passo a passo de uma cadeia aceita

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

#### 3.6.2 Execução passo a passo de uma cadeia rejeitada

Entrada: `101#100`

Nas duas primeiras comparacoes, a maquina consegue casar `1` e `0`. Na comparacao final, o ultimo simbolo esperado e `1`, mas encontra `0`, entrando em `q_reject`.

Uma decomposicao resumida e:

| Etapa | Configuracao relevante | Acao |
| --- | --- | --- |
| 1 | `101#100` | marca o primeiro `1` da esquerda com `Y` |
| 2 | `Y01#100` | encontra e marca o primeiro `1` da direita |
| 3 | `Y01#Y00` | volta ao inicio |
| 4 | `Y01#Y00` | marca o `0` da esquerda com `X` |
| 5 | `YX1#Y00` | encontra e marca o `0` correspondente na direita |
| 6 | `YX1#YX0` | volta ao inicio |
| 7 | `YX1#YX0` | marca o ultimo `1` da esquerda com `Y` |
| 8 | `YXY#YX0` | ao procurar o correspondente na direita, encontra `0` em vez de `1` |
| 9 | `YXY#YX0` | entra em `q_reject` |