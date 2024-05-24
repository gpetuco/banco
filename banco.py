class Usuario:
    def __init__(self, nome, cpf):
        self.nome = nome
        self.cpf = cpf

class ContaCorrente:
    def __init__(self, usuario):
        self.usuario = usuario
        self.saldo = 0.0
        self.extrato = []
        self.limite_saque = 500.0
        self.saques_realizados = 0
        self.max_saques = 3
        
    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            self.extrato.append(f"Depósito: +R${valor:.2f}")
            print(f"Depósito de R${valor:.2f} realizado com sucesso.")
        else:
            print("Valor de depósito inválido. O valor deve ser positivo.")
        
    def sacar(self, valor):
        if valor <= 0:
            print("Valor de saque inválido. O valor deve ser positivo.")
        elif valor > self.limite_saque:
            print(f"Valor de saque excede o limite de R${self.limite_saque:.2f}.")
        elif self.saques_realizados >= self.max_saques:
            print("Número máximo de saques diários atingido.")
        elif valor > self.saldo:
            print("Saldo insuficiente.")
        else:
            self.saldo -= valor
            self.extrato.append(f"Saque: -R${valor:.2f}")
            self.saques_realizados += 1
            print(f"Saque de R${valor:.2f} realizado com sucesso.")
        
    def ver_extrato(self):
        print("\n--- Extrato ---")
        if not self.extrato:
            print("Nenhuma transação realizada.")
        else:
            for transacao in self.extrato:
                print(transacao)
        print(f"Saldo atual: R${self.saldo:.2f}")
        print(f"Saques realizados hoje: {self.saques_realizados}/{self.max_saques}")
        print("----------------\n")

class Banco:
    def __init__(self):
        self.usuarios = []
        self.contas = []
    
    def criar_usuario(self, nome, cpf):
        usuario = Usuario(nome, cpf)
        self.usuarios.append(usuario)
        print(f"Usuário {nome} criado com sucesso.")
        return usuario
    
    def criar_conta_corrente(self, usuario):
        conta = ContaCorrente(usuario)
        self.contas.append(conta)
        print(f"Conta corrente para {usuario.nome} criada com sucesso.")
        return conta

def menu():
    banco = Banco()
    
    while True:
        print("\n--- Menu ---")
        print("1. Criar Usuário")
        print("2. Criar Conta Corrente")
        print("3. Depositar")
        print("4. Sacar")
        print("5. Ver Extrato")
        print("6. Sair")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == '1':
            nome = input("Informe o nome do usuário: ")
            cpf = input("Informe o CPF do usuário: ")
            banco.criar_usuario(nome, cpf)
        elif opcao == '2':
            cpf = input("Informe o CPF do usuário para vincular a conta: ")
            usuario = next((u for u in banco.usuarios if u.cpf == cpf), None)
            if usuario:
                banco.criar_conta_corrente(usuario)
            else:
                print("Usuário não encontrado.")
        elif opcao == '3':
            cpf = input("Informe o CPF do usuário: ")
            conta = next((c for c in banco.contas if c.usuario.cpf == cpf), None)
            if conta:
                valor = float(input("Informe o valor para depósito: R$"))
                conta.depositar(valor)
            else:
                print("Conta não encontrada.")
        elif opcao == '4':
            cpf = input("Informe o CPF do usuário: ")
            conta = next((c for c in banco.contas if c.usuario.cpf == cpf), None)
            if conta:
                valor = float(input("Informe o valor para saque: R$"))
                conta.sacar(valor)
            else:
                print("Conta não encontrada.")
        elif opcao == '5':
            cpf = input("Informe o CPF do usuário: ")
            conta = next((c for c in banco.contas if c.usuario.cpf == cpf), None)
            if conta:
                conta.ver_extrato()
            else:
                print("Conta não encontrada.")
        elif opcao == '6':
            print("Saindo do sistema bancário.")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()
