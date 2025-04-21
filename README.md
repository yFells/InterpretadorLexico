# Validador de Lógica Proposicional

Este programa implementa um validador léxico e sintático para expressões de lógica proposicional escritas em LaTeX, usando um analisador léxico que simula uma máquina de estados finitos e um parser LL(1).

## Gramática Implementada

```
FORMULA = CONSTANTE | PROPOSICAO | FORMULAUNARIA | FORMULABINARIA
CONSTANTE = true | false
PROPOSICAO = [0-9][0-9a-z]*
FORMULAUNARIA = ABREPAREN OPERADORUNARIO FORMULA FECHAPAREN
FORMULABINARIA = ABREPAREN OPERATORBINARIO FORMULA FORMULA FECHAPAREN
ABREPAREN = (
FECHAPAREN = )
OPERATORUNARIO = \neg
OPERATORBINARIO = \wedge | \vee | \rightarrow | \leftrightarrow
```

## Tratamento Especial de Proposições

De acordo com a gramática, as proposições devem começar com um dígito (0-9) seguido por zero ou mais dígitos ou letras minúsculas. No entanto, para compatibilidade com os exemplos fornecidos, o programa também reconhece proposições no formato "pX", onde "p" é a letra 'p' e X é um número seguido de letras ou dígitos.

## Como Executar

Para executar o validador, utilize o seguinte comando:

```bash
python analisador_lexico.py <arquivo_de_entrada> [--debug] [--teste]
```

Onde:
- `<arquivo_de_entrada>` é o nome do arquivo contendo as expressões a serem validadas.
- `--debug` (opcional) ativa o modo de depuração, exibindo informações detalhadas sobre a análise.
- `--teste` (opcional) executa um conjunto de expressões de teste pré-definidas, ignorando o arquivo de entrada.

## Formato do Arquivo de Entrada

O arquivo de entrada deve seguir o seguinte formato:
1. A primeira linha contém um número inteiro que indica quantas expressões lógicas estão no arquivo.
2. Cada linha subsequente contém uma expressão lógica a ser validada.

## Exemplos de Arquivos de Teste

Foram incluídos quatro arquivos de teste:
- `teste1.txt`: 5 expressões válidas usando proposições no formato 'pX'
- `teste2.txt`: 7 expressões, algumas inválidas
- `teste3.txt`: 10 expressões variadas
- `teste4.txt`: 8 expressões usando proposições que começam com dígitos (formato da gramática)

## Saída do Programa

Para cada expressão no arquivo de entrada, o programa imprimirá uma linha contendo:
- `valida`: se a expressão estiver léxica e gramaticalmente correta
- `invalida`: se a expressão contiver erros

## Exemplos de Expressões Válidas

### Proposições no formato padrão (começando com dígito):
- `0`, `1`, `123abc` (proposições)

### Proposições no formato alternativo (começando com 'p'):
- `p0`, `p1`, `p123abc` (proposições)

### Constantes:
- `true` ou `false`

### Expressões com operadores:
- `(\neg p0)` ou `(\neg 0)` (negação)
- `(\wedge p0 p1)` ou `(\wedge 0 1)` (conjunção)
- `(\vee p0 p1)` ou `(\vee 0 1)` (disjunção)
- `(\rightarrow p0 p1)` ou `(\rightarrow 0 1)` (implicação)
- `(\leftrightarrow p0 p1)` ou `(\leftrightarrow 0 1)` (bi-implicação)
- Expressões aninhadas como `(\rightarrow (\neg p0) (\wedge p1 p2))`

## Detalhes da Implementação

O programa é composto por duas classes principais:

1. `AnalisadorLexico`: Responsável por converter a entrada de texto em tokens.
2. `Parser`: Implementa um analisador sintático LL(1) que verifica se a sequência de tokens segue a gramática especificada.

Funções auxiliares:
- `print_tokens(expressao)`: Imprime todos os tokens de uma expressão (útil para debug).
- `teste_expressao(expressao)`: Testa se uma expressão é válida e imprime o resultado.
- `validar_expressao(expressao)`: Função principal que valida uma expressão.

## Problemas Comuns e Soluções

### Operadores LaTeX
Os operadores LaTeX devem ser escritos exatamente como especificado na gramática. Por exemplo:
- Use `\neg` para negação (não `\lnot` ou `~`)
- Use `\wedge` para conjunção (não `\land` ou `&`)
- Use `\vee` para disjunção (não `\lor` ou `|`)
- Use `\rightarrow` para implicação (não `\to` ou `->`)
- Use `\leftrightarrow` para bi-implicação (não `\iff` ou `<->`)

### Espaços em Branco
Espaços em branco são ignorados durante a análise, então `(\neg p0)` e `( \neg p0 )` são equivalentes.

### Caracteres de Escape
Ao escrever a barra invertida `\` em uma string Python ou em um arquivo de texto, pode ser necessário duplicá-la `\\` ou usar raw strings `r"\neg"` para evitar que ela seja interpretada como um caractere de escape.

### Expressões Aninhadas
Expressões podem ser aninhadas a qualquer profundidade, desde que cada fórmula aberta seja fechada adequadamente:
```
(\rightarrow (\neg (\wedge p0 p1)) (\vee p2 (\leftrightarrow p3 p4)))
```

## Limitações

- O programa não realiza validação semântica, apenas sintática. Ou seja, ele verifica se a expressão está bem formada de acordo com a gramática, mas não verifica se ela faz sentido logicamente.
- A gramática não suporta o uso de parênteses para agrupar fórmulas em conjunções ou disjunções múltiplas como em notação infixa tradicional. Por exemplo, `(p0 \wedge p1 \wedge p2)` não é válido. Em vez disso, use `(\wedge p0 (\wedge p1 p2))`.

## Resolução de Problemas

Se o programa estiver marcando uma expressão aparentemente correta como inválida, verifique:
1. Se os operadores estão escritos exatamente como na gramática
2. Se os parênteses estão balanceados corretamente
3. Se todas as proposições começam com um dígito ou com a letra 'p' seguida por um dígito
4. Execute o programa com a opção `--debug` para visualizar a análise passo a passo

## Extensão do Projeto

O programa poderia ser estendido para:
1. Implementar avaliação semântica das expressões lógicas
2. Suportar mais operadores lógicos
3. Criar visualizações de tabelas verdade
4. Implementar normalização de fórmulas (forma normal conjuntiva/disjuntiva)
5. Verificar equivalência lógica entre expressões

dador de Lógica Proposicional

Este programa implementa um validador léxico e sintático para expressões de lógica proposicional escritas em LaTeX, usando um analisador léxico que simula uma máquina de estados finitos e um parser LL(1).

## Gramática Implementada

```
FORMULA = CONSTANTE | PROPOSICAO | FORMULAUNARIA | FORMULABINARIA
CONSTANTE = true | false
PROPOSICAO = [0-9][0-9a-z]*
FORMULAUNARIA = ABREPAREN OPERADORUNARIO FORMULA FECHAPAREN
FORMULABINARIA = ABREPAREN OPERATORBINARIO FORMULA FORMULA FECHAPAREN
ABREPAREN = (
FECHAPAREN = )
OPERATORUNARIO = \neg
OPERATORBINARIO = \wedge | \vee | \rightarrow | \leftrightarrow
```

## Como Executar

Para executar o validador, utilize o seguinte comando:

```bash
python validador_logica.py <arquivo_de_entrada>
```

Onde `<arquivo_de_entrada>` é o nome do arquivo contendo as expressões a serem validadas.

## Formato do Arquivo de Entrada

O arquivo de entrada deve seguir o seguinte formato:
1. A primeira linha contém um número inteiro que indica quantas expressões lógicas estão no arquivo.
2. Cada linha subsequente contém uma expressão lógica a ser validada.

## Exemplos de Arquivos de Teste

Foram incluídos três arquivos de teste:
- `teste1.txt`: 5 expressões válidas
- `teste2.txt`: 7 expressões, algumas inválidas
- `teste3.txt`: 10 expressões variadas

## Saída do Programa

Para cada expressão no arquivo de entrada, o programa imprimirá uma linha contendo:
- `valida`: se a expressão estiver lexica e gramaticalmente correta
- `invalida`: se a expressão contiver erros

## Exemplos de Expressões Válidas

- `true` ou `false` (constantes)
- `p0`, `p1`, `p123abc` (proposições)
- `(\neg p0)` (negação)
- `(\wedge p0 p1)` (conjunção)
- `(\vee p0 p1)` (disjunção)
- `(\rightarrow p0 p1)` (implicação)
- `(\leftrightarrow p0 p1)` (bi-implicação)
- Expressões aninhadas como `(\rightarrow (\neg p0) (\wedge p1 p2))`

## Resultados Esperados: 

Teste1.txt
valida
valida
valida
valida
valida

Teste2.txt
valida
valida
valida
valida
valida
invalida
invalida

Teste3.txt
valida
valida
valida
valida
valida
valida
valida
valida
valida
valida

Teste4.txt 
Tudo valido