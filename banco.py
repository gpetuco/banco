import textwrap
from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
    def realizaTransacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.nascimento = nascimento
        self.cpf = cpf
    
class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()
    
    @classmethod
    def criaContaNova(cls, cliente, numero):
        return cls(numero, cliente)
    
    @property
    def historico(self):
        return self._historico
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia

    @property
    def saldo(self):
        return self._saldo
    
    @property
    def cliente(self):
        return self._cliente

    def sacar(self, valor):
        if valor <= 0:
            print("Valor de saque inválido. O valor deve ser positivo.")
        elif valor > self.saldo:
            print("Saldo insuficiente.")
        else:
            self._saldo -= valor
            print(f"Saque de R${valor:.2f} realizado com sucesso.")
            return True
        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print(f"Depósito de R${valor:.2f} realizado com sucesso.")
        else:
            print("Valor de depósito inválido. O valor deve ser positivo.")
            return False
        return True

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite = 500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__])

        if valor > self.limite:
            print(f"Valor de saque excede o limite de R${self.limite:.2f}.")
        elif numero_saques >= self.limite_saques:
            print("Número máximo de saques diários atingido.")
        else:
            return super().sacar(valor)
        return False
    
    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
            """

class Historico:
    def __init__(self):
        self._transacoes = []
    
    @property
    def transacoes(self):
        return self._transacoes
    
    def transacaoHistorico(self, transacao):
        self._transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor
        })

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso = conta.sacar(self.valor)

        if sucesso:
            conta.historico.transacaoHistorico(self)     
    
class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso = conta.depositar(self.valor)

        if sucesso:
            conta.historico.transacaoHistorico(self)

def menu():
    print("1. Criar Usuário")
    print("2. Criar Conta Corrente")
    print("3. Depositar")
    print("4. Sacar")
    print("5. Ver Extrato")
    print("6. Listar Contas")
    print("7. Sair")
        
    opcao = input("Escolha uma opção: ")
    return opcao


def findClient(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def recuperarConta(cliente):
    if not cliente.contas:
        print("Cliente não possui conta!")
        return

    # FIXME: não permite cliente escolher a conta
    return cliente.contas[0]


def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = findClient(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado!")
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperarConta(cliente)
    if not conta:
        return

    cliente.realizaTransacao(conta, transacao)


def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = findClient(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado!")
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperarConta(cliente)
    if not conta:
        return

    cliente.realizaTransacao(conta, transacao)


def listaExtrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = findClient(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado!")
        return

    conta = recuperarConta(cliente)
    if not conta:
        return

    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==========================================")


def newClient(clientes):
    cpf = input("Informe o CPF (somente número): ")
    cliente = findClient(cpf, clientes)

    if cliente:
        print("Já existe cliente com esse CPF!")
        return

    nome = input("Informe o nome completo: ")
    nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço: ")

    cliente = PessoaFisica(nome=nome, nascimento=nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)

    print("\n=== Cliente criado com sucesso! ===")


def newConta(nrConta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = findClient(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado!")
        return

    conta = ContaCorrente.criaContaNova(cliente=cliente, numero=nrConta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("\n=== Conta criada com sucesso! ===")


def allContas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))


def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "1":
            newClient(clientes)

        elif opcao == "2":
            nrConta = len(contas) + 1
            newConta(nrConta, clientes, contas)

        elif opcao == "3":
            depositar(clientes)

        elif opcao == "4":
            sacar(clientes)

        elif opcao == "5":
            listaExtrato(clientes)

        elif opcao == "6":
            allContas(contas)

        elif opcao == "7":
            break

        else:
            print("Operação inválida.")

main()
