# Desafio DIO - Criação de Sistema Bancário
#
# Por Walter Fróes
#

from colorama import Fore
from getpass import getpass

##==-- Variáveis --==##

LIMITE_SAQUE = 3
contaExiste = False
saldo = 0.0
nome = ""
senha = ""
operacao = ""
extrato = []
valor = 0.0
saques = 0.0

menu1 = """
1 - Criar Conta
2 - Sair

==> """

menu2 = """
1 - Depositar
2 - Sacar
3 - Extrato
4 - Sair

==> """

# Funçoes

def criarConta():
    global contaExiste
    global saldo
    global nome
    global senha
    global saques

    contaExiste = True
    saldo = 0
    while (not nome): 
        nome = input("Qual o seu nome: ")
    while (not senha):
        senha = getpass("Escolha uma senha: ")
    saques = 0

def depositar():
    global saldo
    global valor
    global extrato

    valor = float (input ("Informe o valor do depósito: "))

    if (valor <= 0):
        print (Fore.RED + "Valor de depósito deve ser maior que 0!")
    else:
        saldo += valor
        extrato.append(f"Deposito: R$ {valor:.2f}\n")

def sacar():
    global saldo
    global senha
    global saques
    global extrato
    global valor

    if (saques >= LIMITE_SAQUE):
        print (Fore.RED + "Limite de saques atingido!")
    else:
        valor = float (input ("Informe o valor do saque: "))

        if (valor <= 0):
            print (Fore.RED + "Valor de saque deve ser maior que 0!")
        elif (valor > 500):
            print (Fore.RED + "Valor de saque deve ser menor que R$ 500!")
        elif (valor > saldo):
            print (Fore.RED+"Saldo insuficiente!")
            print (f"Saldo atual: R$ {saldo:.2f}")
        else:
            senhaLocal = getpass("Informe a senha: ")
            if (senhaLocal != senha):
                print (Fore.RED + "Senha incorreta!")
                return
            saldo -= valor
            saques += 1
            extrato.append(f"Saque   : R$ {valor:.2f}\n")

def printExtrato():
    global saldo
    global extrato
    global nome

    print (Fore.BLUE+"\n\n############\n")
    print ("Extrato Bancário:\n")
    if (not extrato):
        print ("Não foram registradas movimentações nesta conta até o momento.")
    else:
        print (f"Olá {nome}")
        print ("Estas são suas movimentações financeiras: \n")
        print ("".join(extrato))

    print (f"\nSaldo atual: R$ {saldo:.2f}")
    print ("\n\n############")


##==-- Programa Principal --==##

while True:
    if (not contaExiste):
        print (Fore.YELLOW + "\nNenhuma conta cadastrada!")
        operacao = input (Fore.GREEN + menu1)
        if (operacao == "1"):
            criarConta()
        elif (operacao == "2"):
            break
        else:
            print (Fore.RED + "\nOperação inválida!")
    else:
        print (Fore.YELLOW + f"\nOlá {nome}")
        print (Fore.YELLOW + "Seja bem-vindo(a)!", end=" ")
        print (Fore.YELLOW + f"Seu saldo atual é R$ {saldo:.2f}")
        print (Fore.GREEN+"\nEscolha a operação desejada:")
        operacao = input (Fore.GREEN + menu2)
        if (operacao == "1"):
            depositar()
        elif (operacao == "2"):
            sacar()
        elif (operacao == "3"):
            printExtrato()
        elif (operacao == "4"):
            break
        else:
            print (Fore.RED + "\nOperação inválida!")
