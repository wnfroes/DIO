# DIO_Desafio_Sistema_Bancario_Com_Classes.py
#
# Por Walter Fróes
#

#####
# Definição de classes
#####

from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime
from colorama import Fore

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

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao (self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta (self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, endereco, data_nascimento):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento
    
class PessoaJuridica(Cliente):
    def __init__(self, cnpj, nome, endereco):
        super().__init__(endereco)
        self.cnpj = cnpj
        self.nome = nome
    
class Conta:
    def __init__(self, cliente, numero, saldo_inicial=0):
        self.cliente = cliente
        self._agencia = "0001"
        self._numero = numero
        self._saldo = saldo_inicial
        self._historico = Historico()

        cliente.adicionar_conta(self)

    @property
    def saldo (self):
        return self._saldo

    @saldo.setter
    def saldo(self, valor):
        if (valor >= 0):
            self._saldo = valor
        else:
            print("Valor de saldo negativo.")

    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def historico(self):
        return self._historico
        
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(cliente, numero)

    def depositar(self, valor):
        if (valor >= 0):
            self._saldo += valor
            return True
        else:
            print("Valor de depósito negativo.")
            return False

    def sacar(self, valor):
        if valor >= 0 and self.saldo >= valor:
            self.saldo -= valor
            return True
        else:
            print("Valor de saque negativo ou saldo insuficiente.")
            return False

class ContaCorrente(Conta):
    def __init__(self, cliente, numero, limite, limite_saques, saldo_inicial=0):
        super().__init__(cliente, numero, saldo_inicial)
        self.saques = 0
        self.limite = limite
        self.limite_saques = limite_saques

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @property
    @abstractproperty
    def data(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__ (self, valor):
        self._valor = valor
        self._data = datetime.now()

    @property
    def valor(self):
        return self._valor

    @property
    def data(self):
        return self._data

    def registrar(self, conta):
        if conta.sacar (self._valor):
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__ (self, valor):
        self._valor = valor
        self._data = datetime.now()
    
    @property
    def valor(self):
        return self._valor

    @property
    def data(self):
        return self._data

    def registrar(self, conta):
        if conta.depositar (self._valor):
            conta.historico.adicionar_transacao(self)
    

################################
# Funçoes                      #
################################

##########
# Cria usuários
##########

def criarUsuario (usuarios):

    cpf = input (Fore.GREEN + "Informe o CPF do usuário ou <ENTER> para retornar: " + Fore.YELLOW)
    while (not cpf):
        return

    if localizaUsuario(cpf, usuarios):
        print (Fore.RED + "CPF já cadastrado")
        return

    nome = ""
    while (not nome):
        nome = input (Fore.GREEN + "Qual o nome do usuário: " + Fore.YELLOW)

    endereco = ""
    while (not endereco):
        endereco = input (Fore.GREEN + "Informe o endereço do usuário: (logradouro, número - bairro - cidade/uf cep): " + Fore.YELLOW)

    dataNascimento = ""
    while (not dataNascimento):
        dataNascimento = input (Fore.GREEN + "Informe a data de nascimento do usuário (dd-mm-aaaa): " + Fore.YELLOW)
    
    novoUsuario = PessoaFisica (cpf, nome, endereco, dataNascimento)

    usuarios.append(novoUsuario)

    return

##########
# Cria conta corrente
##########

def criarConta(contas, clientes):   

    cpf = input (Fore.GREEN + "Informe o CPF do usuário ou <ENTER> para retornar: " + Fore.YELLOW)

    if (cpf == ""):
        return

    if localizaUsuario(cpf, clientes):
        for cliente in clientes:
            if (cliente.cpf == cpf):
                break
        novaConta = ContaCorrente(cliente, len(contas)+1, 500, 3, 0)
        contas.append(novaConta)
        print (Fore.CYAN + "Conta criada com sucesso!")
    else:
        print (Fore.RED + "Usuário não localizado")

    return

##########
# Localiza usuário por CPF
##########

def localizaUsuario(cpf, clientes):
    for cliente in clientes:
        if (cliente.cpf == cpf):
            return True
    return False

##########
# Deposita dinheiro na conta selecionada
##########

def depositar(conta, valor):
    if (valor <= 0):
        print (Fore.RED + "Valor de depósito deve ser maior que 0!")
    else:
        operacao = Deposito(valor)
        conta.cliente.realizar_transacao (conta, operacao)
    
    return 

##########
# Saca dinheiro da conta selecionada
##########

def sacar(conta, valor):

    if (conta.saques >= conta.limite_saques):
        print (Fore.RED + "Limite de saques atingido!")
    else:
        if (valor <= 0):
            print (Fore.RED + "Valor de saque deve ser maior que 0!")
        elif (valor > conta.limite):
            print (Fore.RED + "Valor de saque deve ser menor que R$ 500!")
        elif (valor > conta.saldo):
            print (Fore.RED+"Saldo insuficiente!")
            print (f"Saldo atual: R$ {conta.saldo:.2f}")
        else:
            conta.saques += 1
            conta.cliente.realizar_transacao (conta, Saque(valor))

    return

##########
# Imprime Extrato
##########

def printExtrato(conta):

    saldo = conta.saldo
    transacoes = conta.historico.transacoes

    print (Fore.BLUE+"\n\n############\n")
    print ("Extrato Bancário:\n")
    if (not transacoes):
        print ("Não foram registradas movimentações nesta conta até o momento.")
    else:
        print ("Estas são suas movimentações financeiras: \n")     
        for transacao in transacoes:
            if (transacao.__class__.__name__ == "Deposito"):
                print(Fore.BLUE + f"{transacao.data} \t" +Fore.GREEN + "+" + " "*(10-len(str(transacao.valor))) + f" {transacao.valor:.2f}")
            else:
                print(Fore.BLUE + f"{transacao.data} \t" +Fore.RED + "-" + " "*(10-len(str(transacao.valor))) + f" {transacao.valor:.2f}")

    corSaldo = Fore.GREEN if saldo >= 0 else Fore.RED
    print (Fore.BLUE + f"\nSaldo atual: " + corSaldo + f" R$ {saldo:.2f}")
    print (Fore.BLUE+"\n############")

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
        print (Fore.CYAN + "Conta: " + Fore.YELLOW + f"{conta.numero} " + Fore.CYAN + "- Agência: " + Fore.YELLOW + f"{conta.agencia} " + Fore.CYAN + "- Usuário: " + Fore.YELLOW + f"{conta.cliente.nome}")

    print("")
    conta = input (Fore.GREEN + "Informe o número da conta ou <ENTER> para retornar: " + Fore.YELLOW)

    if (conta):
        contaSelecionada = int(conta)
    else:
        return contaSelecionada

    for val in contas:
        if (val.numero == contaSelecionada):
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
        print (Fore.CYAN + f"Conta: " + Fore.YELLOW + f"{conta.numero} " + Fore.CYAN + "- Agência: " + Fore.YELLOW + f"{conta.agencia} " + Fore.CYAN + "- Usuário: " + Fore.YELLOW + f"{conta.cliente.nome}")

##########
# Lista usuários cadastrados
##########

def listarUsuarios(clientes):
    print (Fore.CYAN + "\n----------------------------------\n")
    print (Fore.CYAN + "Lista de Usuários:")
    print (Fore.CYAN + "\n----------------------------------\n")
    for usuario in clientes:
        print (Fore.CYAN + f"Nome: " + Fore.YELLOW + f"{usuario.nome} " + Fore.CYAN + "- CPF: " + Fore.YELLOW + f"{usuario.cpf} " + Fore.CYAN + "- Data Nascimento: " + Fore.YELLOW + f"{usuario.data_nascimento} " + Fore.CYAN + "Endereço: "+ Fore.YELLOW + f"{usuario.endereco} ")    

################################
# Programa Principal           #
################################

contas = []
clientes = []
nivelMenu = 0
contaSelecionada = 0

while True:
    if (contas and contaSelecionada != 0):
        print (Fore.CYAN + "\n----------------------------------")
        print (Fore.CYAN + "Conta Selecionada: " + Fore.YELLOW + f"{contas[contaSelecionada -1].numero} - " + Fore.CYAN + "Usuário: " + Fore.YELLOW + f"{contas[contaSelecionada -1].cliente.nome}")
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
                criarConta(contas, clientes)
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
                depositar(conta, valor)
            elif (operacao == "2"): # sacar
                valor = float (input (Fore.GREEN + "Informe o valor do saque: " + Fore.YELLOW))
                sacar(conta, valor)
            elif (operacao == "3"): # imprimir extrato
                printExtrato(conta)
            elif (operacao == "4"): # selcionar conta
                contaSelecionada = selecionarConta(contas, contaSelecionada)
            elif (operacao == "99"):
                nivelMenu = 0    
            else:
                print (Fore.RED + "\nOperação inválida!")
