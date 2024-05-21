class Banco:
    def __init__(self):
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

def menu():
    banco = Banco()
    
    while True:
        print("\n--- Menu ---")
        print("1. Depositar")
        print("2. Sacar")
        print("3. Ver Extrato")
        print("4. Sair")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == '1':
            valor = float(input("Informe o valor para depósito: R$"))
            banco.depositar(valor)
        elif opcao == '2':
            valor = float(input("Informe o valor para saque: R$"))
            banco.sacar(valor)
        elif opcao == '3':
            banco.ver_extrato()
        elif opcao == '4':
            print("Saindo do sistema bancário.")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()
