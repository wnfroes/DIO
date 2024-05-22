# Desafio DIO - Criação de Sistema Bancário 2
#
# Por Walter Fróes
#

# Regras:
# Criar duas funções: criar_conta_corrente e criar_usuário
# Função saque() deve receber argumentos apenas por nome (saldo, valor, extrato, limite, número_saques, limite_saques)
# Função deposito() deve receber argumentos apenas por posição (saldo, valor, extrato)
# Função extrato() deve receber argumentos por posição e nome, saldo por posição e extrato por nome
# Usuário = [nome: "", data_nascimento: "", cpf: "", endereço: ""]
# Endereço é string com formato "logradouro, número - bairro - cidade/uf cep"
# CPF deve ser armazenado sem pontos e traços, somente número
# Não pode haver mais de um usuário com o mesmo CPF
# Deve armazenar contas correntes em uma lista. Conta corrente deve conter: agência, conta e usuário
# O número da conta corrente é sequencial, iniciando por 1
# O número da agência é fixo e igual a "0001"
# Um usuário pode ter mais de uma conta, mas cada conta pertence a apenas 1 usuário 
# Não é necessário verificar formatação de cpf, endereço e data de nascimento

from colorama import Fore
from datetime import datetime

##==-- Variáveis --==##

LIMITE_SAQUES = 3
AGENCIA = "0001"

operacao = ""
contas = []
clientes = []
numeroCC = 1
nivelMenu = 0
contaSelecionada = 0

menu0 = """
1  - Administrar
2  - Movimentar Conta
99 - Sair

==> """

menu1 = """
1  - Criar Usuário
2  - Criar Contas
3  - Listar Usuário
4  - Listar Contas
99 - Voltar

==> """

menu2 = """
1  - Depositar
2  - Sacar
3  - Extrato
4  - Selecionar Conta
99 - Voltar

==> """

menus = {0: menu0, 1: menu1, 2: menu2}

################################
# Funçoes                      #
################################

##########
# Cria usuários
##########

def criarUsuario (usuarios = []):

    cpf = input (Fore.GREEN + "Informe o CPF do usuário ou <ENTER> para retornar: " + Fore.YELLOW)
    while (not cpf):
        return

    if localizaUsuario(cpf):
        print (Fore.RED + "CPF já cadastrado")
        return

    nome = input (Fore.GREEN + "Qual o nome do usuário: " + Fore.YELLOW)
    while (not nome):
        nome = input (Fore.GREEN + "Qual o nome do usuário: " + Fore.YELLOW)

    endereco = input (Fore.GREEN + "Informe o endereço do usuário (logradouro, número - bairro - cidade/uf cep): " + Fore.YELLOW)
    while (not endereco):
        endereco = input (Fore.GREEN + "Informe o endereço do usuário: (logradouro, número - bairro - cidade/uf cep): " + Fore.YELLOW)

    dataNascimento = input (Fore.GREEN + "Informe a data de nascimento do usuário (dd-mm-aaaa): " + Fore.YELLOW)
    while (not dataNascimento):
        dataNascimento = input (Fore.GREEN + "Informe a data de nascimento do usuário (dd-mm-aaaa): " + Fore.YELLOW)
    
    usuario = {
        "nome": nome,
        "cpf": cpf,
        "endereco": endereco,
        "dataNascimento": dataNascimento
    }
    usuarios.append(usuario)

##########
# Cria conta corrente
##########

def criarConta(numConta, agencia, contas):   
    global LIMITE_SAQUES

    usuario = input (Fore.GREEN + "Informe o CPF do usuário ou <ENTER> para retornar: " + Fore.YELLOW)

    if (usuario == ""):
        return

    if localizaUsuario(usuario):
        conta = {
            "numConta": numConta,
            "agencia": agencia,
            "usuario": usuario,
            "saldo": 0.0,
            "extrato": [],
            "limiteSaques": LIMITE_SAQUES,
            "saques": 0
        }
        contas.append(conta)
        print (Fore.CYAN + "Conta criada com sucesso!")
        numConta += 1
    else:
        print (Fore.RED + "Usuário não localizado")

    return numConta

##########
# Localiza usuário por CPF
##########

def localizaUsuario(cpf):
    global clientes
    for usuario in clientes:
        if (usuario["cpf"] == cpf):
            return True
    return False

##########
# Deposita dinheiro na conta selecionada
##########

def depositar(saldo, valor, extrato, /):
    if (valor <= 0):
        print (Fore.RED + "Valor de depósito deve ser maior que 0!")
    else:
        saldo += valor
        extrato.append(Fore.GREEN + datetime.now().strftime("%d/%m/%Y - %H:%M:%S - ") + f"Deposito: R$ {valor:.2f}\n")
    
    return saldo, extrato

##########
# Saca dinheiro da conta selecionada
##########

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):

    if (numero_saques >= LIMITE_SAQUES):
        print (Fore.RED + "Limite de saques atingido!")
    else:
        if (valor <= 0):
            print (Fore.RED + "Valor de saque deve ser maior que 0!")
        elif (valor > limite):
            print (Fore.RED + "Valor de saque deve ser menor que R$ 500!")
        elif (valor > saldo):
            print (Fore.RED+"Saldo insuficiente!")
            print (f"Saldo atual: R$ {saldo:.2f}")
        else:
            saldo -= valor
            numero_saques += 1
            extrato.append(Fore.RED + datetime.now().strftime("%d/%m/%Y - %H:%M:%S - ") + f"Saque   : R$ {valor:.2f}\n")

    return saldo, extrato, numero_saques

##########
# Imprime Extrato
##########

def printExtrato(saldo, /, *, extrato):

    print (Fore.BLUE+"\n\n############\n")
    print ("Extrato Bancário:\n")
    if (not extrato):
        print ("Não foram registradas movimentações nesta conta até o momento.")
    else:
        print ("Estas são suas movimentações financeiras: \n")
        print ("".join(extrato))

    print (Fore.BLUE + f"\nSaldo atual: R$ {saldo:.2f}")
    print ("\n############")

##########
# Seleciona Conta 
##########

def selecionarConta (contas, contaSelecionada):

    if (not contas):
        print (Fore.RED + "Não existem contas cadastradas!")
        return 0

    print (Fore.CYAN + "\n----------------------------------\n")
    print (Fore.CYAN + "Selecione a conta:")
    print (Fore.CYAN + "\n----------------------------------\n")

    for conta in contas:
        print (Fore.CYAN + "Conta: " + Fore.YELLOW + f"{conta['numConta']} " + Fore.CYAN + "- Agência: {conta['agencia']} - Usuário: {conta['usuario']}")

    print("")
    conta = input (Fore.GREEN + "Informe o número da conta ou <ENTER> para retornar: " + Fore.YELLOW)

    if (conta):
        contaSelecionada = int(conta)
    else:
        return contaSelecionada

    for val in contas:
        if (val['numConta'] == contaSelecionada):
            return contaSelecionada
    
    return 0

##########
# Lista contas cadastrados
##########

def listarContas(contas):
    print (Fore.CYAN + "\n----------------------------------\n")
    print (Fore.CYAN + "Lista de Contas:")
    print (Fore.CYAN + "\n----------------------------------\n")
    for conta in contas:
        print (Fore.CYAN + f"Conta: {conta['numConta']} - Agência: {conta['agencia']} - Usuário: {conta['usuario']}")

##########
# Lista usuários cadastrados
##########

def listarUsuarios(clientes):
    print (Fore.CYAN + "\n----------------------------------\n")
    print (Fore.CYAN + "Lista de Usuários:")
    print (Fore.CYAN + "\n----------------------------------\n")
    for usuario in clientes:
        print (Fore.CYAN + f"Nome: {usuario['nome']} - CPF: {usuario['cpf']} - Data Nascimento {usuario['dataNascimento']}")    

##==-- Programa Principal --==##

while True:
    if (contas and contaSelecionada != 0):
        print (Fore.CYAN + "\n----------------------------------")
        print (Fore.CYAN + "Conta Selecionada: " + Fore.YELLOW + f"{contas[contaSelecionada -1]['numConta']} - " + Fore.CYAN + "Usuário: " + Fore.YELLOW + f"{contas[contaSelecionada -1]['usuario']}")
    operacao = input (Fore.GREEN + menus[nivelMenu] + Fore.YELLOW)
    match nivelMenu:
        case 0:
            if (operacao == "1"): # Administrar 
                nivelMenu = 1
            elif (operacao == "2"): # Movimentar Contas
                nivelMenu = 2
            elif (operacao == "99"): # Voltar
                break
            else:
                print (Fore.RED + "\nOperação inválida!")
        case 1:
            if (operacao == "2"): # CriarConta
                numeroCC = criarConta(numeroCC, AGENCIA, contas)
            elif (operacao == "4"): # ListarContas
                listarContas(contas)
            elif (operacao == "1"): # CriarUsuario
                criarUsuario(clientes)
            elif (operacao == "3"): # ListarUsuarios
                listarUsuarios(clientes)
            elif (operacao == "99"): # Voltar
                nivelMenu = 0    
            else:
                print (Fore.RED + "\nOperação inválida!")
        case 2:
            if ((not contas or contaSelecionada == 0) and operacao != "4"):
                print (Fore.RED + "\nNenhuma conta cadastrada ou não selecionada!")
                continue
            else:
                conta = contas[contaSelecionada -1]
            if (operacao == "1"): # depositar
                valor = float (input (Fore.GREEN + "Informe o valor do depósito: " + Fore.YELLOW))
                saldo, extrato = conta['saldo'], conta['extrato']
                retorno = depositar(saldo, valor, extrato)
                conta['saldo'] = retorno[0]
                conta['extrato'] = retorno[1]
            elif (operacao == "2"): # sacar
                saque = float (input (Fore.GREEN + "Informe o valor do saque: " + Fore.YELLOW))
                retorno = sacar(saldo=conta['saldo'], valor = saque, extrato = conta['extrato'], limite = 500, numero_saques = conta['saques'], limite_saques = conta['limiteSaques'])
                conta['saldo'] = retorno[0]
                conta['extrato'] = retorno[1]
                conta['saques'] = retorno[2]
            elif (operacao == "3"): # imprimir extrato
                printExtrato(conta['saldo'], extrato = conta['extrato'])
            elif (operacao == "4"): # selcionar conta
                contaSelecionada = selecionarConta(contas, contaSelecionada)
            elif (operacao == "99"):
                nivelMenu = 0    
            else:
                print (Fore.RED + "\nOperação inválida!")
