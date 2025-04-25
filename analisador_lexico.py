#GRUPO RA1 12 - Eduarda Dallagrana Batista, Felipe de Lima dos Santos, Kaua da Silva Nunes

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analisador Léxico e Sintático para Lógica Proposicional

Este programa implementa um validador léxico e sintático para expressões 
de lógica proposicional escritas em LaTeX, usando um analisador léxico 
que simula uma máquina de estados finitos e um parser LL(1).

A gramática implementada é:

FORMULA = CONSTANTE | PROPOSICAO | FORMULAUNARIA | FORMULABINARIA
CONSTANTE = true | false
PROPOSICAO = [0-9][0-9a-z]*
FORMULAUNARIA = ABREPAREN OPERADORUNARIO FORMULA FECHAPAREN
FORMULABINARIA = ABREPAREN OPERATORBINARIO FORMULA FORMULA FECHAPAREN
ABREPAREN = (
FECHAPAREN = )
OPERATORUNARIO = \neg
OPERATORBINARIO = \wedge | \vee | \rightarrow | \leftrightarrow
"""

import sys
import re


class AnalisadorLexico:
    """
    Classe que implementa o analisador léxico para a linguagem de lógica proposicional.
    Simula uma máquina de estados finitos para reconhecer os tokens da linguagem.
    """
    
    def __init__(self, expressao):
        """
        Inicializa o analisador léxico com a expressão a ser analisada.
        
        Args:
            expressao (str): A expressão a ser analisada
        """
        # Substitui qualquer dupla barra \\ por barra única \
        # Isso é necessário porque em Python a barra invertida é um caractere de escape
        self.expressao = re.sub(r'\\\\', r'\\', expressao)
        self.posicao = 0
        self.token_atual = None
        self.valor_atual = None
        self.proximo_token()
    
    def proximo_token(self):
        """
        Avança para o próximo token da expressão.
        Atualiza token_atual e valor_atual com o próximo token encontrado.
        """
        # Ignora espaços em branco
        while self.posicao < len(self.expressao) and self.expressao[self.posicao].isspace():
            self.posicao += 1
            
        # Verifica o fim da expressão
        if self.posicao >= len(self.expressao):
            self.token_atual = 'EOF'
            self.valor_atual = None
            return
            
        char = self.expressao[self.posicao]
        
        # Reconhecimento de parênteses
        if char == '(':
            self.token_atual = 'ABREPAREN'
            self.valor_atual = char
            self.posicao += 1
        elif char == ')':
            self.token_atual = 'FECHAPAREN'
            self.valor_atual = char
            self.posicao += 1
        # Reconhecimento de operadores LaTeX (começam com \)
        elif char == '\\':
            # Armazena o caractere barra invertida
            operador = char
            self.posicao += 1
            
            # Captura o nome do operador
            if self.posicao < len(self.expressao):
                # Identificação dos operadores por nome
                parte_restante = self.expressao[self.posicao:]
                
                if parte_restante.startswith('neg'):
                    operador += 'neg'
                    self.posicao += 3
                    self.token_atual = 'OPERADORUNARIO'
                    self.valor_atual = operador
                elif parte_restante.startswith('wedge'):
                    operador += 'wedge'
                    self.posicao += 5
                    self.token_atual = 'OPERADORBINARIO'
                    self.valor_atual = operador
                elif parte_restante.startswith('vee'):
                    operador += 'vee'
                    self.posicao += 3
                    self.token_atual = 'OPERADORBINARIO'
                    self.valor_atual = operador
                elif parte_restante.startswith('rightarrow'):
                    operador += 'rightarrow'
                    self.posicao += 10  # comprimento de 'rightarrow'
                    self.token_atual = 'OPERADORBINARIO'
                    self.valor_atual = operador
                elif parte_restante.startswith('leftrightarrow'):
                    operador += 'leftrightarrow'
                    self.posicao += 14  # comprimento de 'leftrightarrow'
                    self.token_atual = 'OPERADORBINARIO'
                    self.valor_atual = operador
                else:
                    # Operador não reconhecido
                    temp_pos = self.posicao
                    while temp_pos < len(self.expressao) and not self.expressao[temp_pos].isspace() and self.expressao[temp_pos] not in ['(', ')']:
                        operador += self.expressao[temp_pos]
                        temp_pos += 1
                    self.posicao = temp_pos
                    self.token_atual = 'ERRO'
                    self.valor_atual = operador
            else:
                # Barra invertida no final da expressão
                self.token_atual = 'ERRO'
                self.valor_atual = operador
        # Reconhecimento de proposições - pela gramática, devem começar com um dígito
        elif char.isdigit():
            proposicao = char
            self.posicao += 1
            
            # Captura o restante da proposição (dígitos ou letras)
            while self.posicao < len(self.expressao) and (self.expressao[self.posicao].isdigit() or 
                                                         ('a' <= self.expressao[self.posicao] <= 'z')):
                proposicao += self.expressao[self.posicao]
                self.posicao += 1
                
            self.token_atual = 'PROPOSICAO'
            self.valor_atual = proposicao
        # Reconhecimento de constantes (true, false) ou outras proposições
        elif char.isalpha():
            palavra = char
            self.posicao += 1
            
            # Captura a palavra completa
            while self.posicao < len(self.expressao) and self.expressao[self.posicao].isalnum():
                palavra += self.expressao[self.posicao]
                self.posicao += 1
                
            # Verifica se é uma constante válida
            if palavra in ['true', 'false']:
                self.token_atual = 'CONSTANTE'
                self.valor_atual = palavra
            # Verifica se é uma proposição no formato pX (onde X é um dígito)
            elif palavra.startswith('p') and len(palavra) > 1 and palavra[1:].isalnum():
                # Como a gramática define que proposições devem começar com dígito,
                # estamos considerando um caso especial para permitir o formato "pX"
                self.token_atual = 'PROPOSICAO'
                self.valor_atual = palavra
            else:
                self.token_atual = 'ERRO'
                self.valor_atual = palavra
        # Caractere desconhecido
        else:
            self.token_atual = 'ERRO'
            self.valor_atual = char
            self.posicao += 1


class Parser:
    """
    Classe que implementa o analisador sintático LL(1) para a linguagem de lógica proposicional.
    Verifica se a sequência de tokens produzida pelo analisador léxico segue a gramática especificada.
    """
    
    def __init__(self, lexico):
        """
        Inicializa o parser com o analisador léxico fornecido.
        
        Args:
            lexico (AnalisadorLexico): O analisador léxico a ser usado
        """
        self.lexico = lexico
        
    def parse(self):
        """
        Inicia a análise sintática a partir da regra inicial (FORMULA).
        
        Returns:
            bool: True se a expressão for válida, False caso contrário
        """
        resultado = self.formula()
        
        # Após processar toda a fórmula, precisamos garantir que chegamos ao fim da entrada
        if resultado and self.lexico.token_atual == 'EOF':
            return True
        return False
    
    def consumir(self, token_esperado):
        """
        Consome um token se ele corresponder ao esperado.
        
        Args:
            token_esperado (str): O token que se espera encontrar
            
        Returns:
            bool: True se o token foi consumido, False caso contrário
        """
        if self.lexico.token_atual == token_esperado:
            self.lexico.proximo_token()
            return True
        return False
    
    def formula(self):
        """
        Implementa a regra: FORMULA = CONSTANTE | PROPOSICAO | FORMULAUNARIA | FORMULABINARIA
        
        Returns:
            bool: True se a fórmula for válida, False caso contrário
        """
        # Caso: CONSTANTE (true ou false)
        if self.lexico.token_atual == 'CONSTANTE':
            return self.consumir('CONSTANTE')
        
        # Caso: PROPOSICAO (p0, p1, etc. ou 0, 1, etc.)
        elif self.lexico.token_atual == 'PROPOSICAO':
            return self.consumir('PROPOSICAO')
        
        # Caso: FORMULAUNARIA ou FORMULABINARIA (começam com parênteses)
        elif self.lexico.token_atual == 'ABREPAREN':
            # Consome o parêntese de abertura
            if not self.consumir('ABREPAREN'):
                return False
                
            # Caso: FORMULAUNARIA
            if self.lexico.token_atual == 'OPERADORUNARIO':
                if not self.consumir('OPERADORUNARIO'):
                    return False
                # Processa a subfórmula
                if not self.formula():
                    return False
                # Consome o parêntese de fechamento
                if not self.consumir('FECHAPAREN'):
                    return False
                return True
            
            # Caso: FORMULABINARIA
            elif self.lexico.token_atual == 'OPERADORBINARIO':
                if not self.consumir('OPERADORBINARIO'):
                    return False
                # Processa a primeira subfórmula
                if not self.formula():
                    return False
                # Processa a segunda subfórmula
                if not self.formula():
                    return False
                # Consome o parêntese de fechamento
                if not self.consumir('FECHAPAREN'):
                    return False
                return True
            
            # Se não encontrou operador após o parêntese
            return False
        
        # Se não corresponder a nenhuma alternativa da regra FORMULA
        return False


def print_tokens(expressao):
    """
    Função auxiliar para imprimir todos os tokens de uma expressão.
    Útil para debug.
    
    Args:
        expressao (str): A expressão a ser analisada
    """
    lexico = AnalisadorLexico(expressao)
    tokens = []
    
    print(f"Tokens da expressão '{expressao}':")
    while lexico.token_atual != 'EOF':
        tokens.append(f"{lexico.token_atual}('{lexico.valor_atual}')")
        lexico.proximo_token()
    
    print(" ".join(tokens))


def validar_expressao(expressao, debug=False):
    """
    Valida se uma expressão de lógica proposicional está correta léxica e sintaticamente.
    
    Args:
        expressao (str): A expressão a ser validada
        debug (bool): Se True, imprime informações de debug
        
    Returns:
        bool: True se a expressão for válida, False caso contrário
    """
    # Para evitar problemas com expressões vazias
    if not expressao or expressao.isspace():
        if debug:
            print(f"Expressão vazia ou só com espaços: '{expressao}'")
        return False
    
    if debug:
        print(f"Analisando expressão: '{expressao}'")
        
    # Cria o analisador léxico para a expressão
    lexico = AnalisadorLexico(expressao)
    
    # Se o primeiro token já é um erro, a expressão é inválida
    if lexico.token_atual == 'ERRO':
        if debug:
            print(f"Erro léxico: token '{lexico.valor_atual}' não reconhecido")
        return False
    
    # Cria o parser e analisa a expressão
    parser = Parser(lexico)
    resultado = parser.parse()
    
    if debug:
        if resultado:
            print("Expressão válida")
        else:
            print("Expressão inválida")
            
    return resultado


def teste_expressao(expressao, mostrar_tokens=True):
    """
    Testa se uma expressão é válida e imprime o resultado.
    
    Args:
        expressao (str): A expressão a ser testada
        mostrar_tokens (bool): Se True, imprime os tokens da expressão
    
    Returns:
        bool: True se a expressão for válida, False caso contrário
    """
    print(f"\nTestando expressão: '{expressao}'")
    
    if mostrar_tokens:
        print_tokens(expressao)
    
    resultado = validar_expressao(expressao)
    
    if resultado:
        print("Resultado: valida")
    else:
        print("Resultado: invalida")
        
    return resultado


def main():
    """
    Função principal que lê o arquivo de entrada e valida cada expressão.
    """
    # Verifica se foi fornecido um arquivo
    if len(sys.argv) < 2:
        print("Uso: python analisador_lexico.py <arquivo> [--debug] [--teste]")
        sys.exit(1)
    
    # Modo de teste - valida algumas expressões pré-definidas
    if "--teste" in sys.argv:
        expressoes_teste = [
            "true",
            "false",
            "p0",
            "p1",
            "p123abc",
            "0",
            "1",
            "123abc",
            "(\neg p0)",
            "(\wedge p1 p2)",
            "(\vee p0 p1)",
            "(\rightarrow p0 p1)",
            "(\leftrightarrow p0 p1)",
            "(\neg (\wedge p0 p1))",
            "(\rightarrow (\neg p0) (\vee p1 p2))",
            "(\leftrightarrow (\wedge p0 p1) (\rightarrow p2 p3))",
            "invalido",
            "(erro)",
            "p",
            "(\neg)",
            "(\wedge p0)"
        ]
        
        for expressao in expressoes_teste:
            teste_expressao(expressao)
        
        sys.exit(0)
        
    nome_arquivo = sys.argv[1]
    debug_mode = "--debug" in sys.argv
    
    try:
        # Abre e lê o arquivo
        with open(nome_arquivo, 'r') as arquivo:
            linhas = arquivo.readlines()
        
        # A primeira linha deve conter o número de expressões
        try:
            num_expressoes = int(linhas[0].strip())
        except ValueError:
            print("Erro: A primeira linha deve conter um número inteiro indicando a quantidade de expressões.")
            sys.exit(1)
            
        if debug_mode:
            print(f"Arquivo: {nome_arquivo}")
            print(f"Número de expressões: {num_expressoes}")
            print(f"Total de linhas no arquivo: {len(linhas)}")
        
        # Valida cada expressão no arquivo
        for i in range(1, num_expressoes + 1):
            if i < len(linhas):
                expressao = linhas[i].strip()
                
                if debug_mode:
                    print(f"\n--- Expressão {i}: '{expressao}' ---")
                    print_tokens(expressao)
                
                resultado = validar_expressao(expressao)
                
                # Imprime o resultado da validação
                if resultado:
                    print("valida")
                else:
                    print("invalida")
            else:
                # Se houver menos expressões que o número informado
                if debug_mode:
                    print(f"\n--- Expressão {i}: [Não encontrada no arquivo] ---")
                print("invalida")
                
    except FileNotFoundError:
        print(f"Arquivo {nome_arquivo} não encontrado.")
        sys.exit(1)
    except Exception as e:
        print(f"Erro ao processar o arquivo: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()