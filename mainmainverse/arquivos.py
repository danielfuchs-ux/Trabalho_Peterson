contas_bancarias = []
mes = 1

class Conta_Bancaria:
    def __init__(self, nomeProprietario, senha):
        self.nomeProprietario = nomeProprietario
        self.__senha = senha
        self.bloqueado = False
        self.tentativas = 0
        self.saldo = 0.0
        self.acessoLiberado = False
        
    def liberar_acesso(self):
        if self.bloqueado:
            print("Conta bloqueada por tentativas inválidas!")
            return
        senha_digitada = input("Digite a senha: ")
        if senha_digitada == self.__senha:
            self.acessoLiberado = True
            self.tentativas = 0
            print("Acesso liberado!")
        else:
            self.tentativas += 1
            print("Senha incorreta!")
            if self.tentativas >= 3:
                self.bloqueado = True
                print("Conta bloqueada devido a tentativas inválidas.")


    def depositar(self):
        if self.acessoLiberado:
            try:
                valor = float(input("Digite o valor do depósito: "))
                if valor > 0:
                    self.saldo += valor
                    print(f"Depósito de R${valor:.2f} realizado com sucesso!")
                else:
                    print("Valor inválido para depósito.")
            except ValueError:
                print("Digite um valor numérico válido.")
            finally:
                self.acessoLiberado = False
        else:
            print("Acesso não liberado.")


    def sacar(self):
        if self.acessoLiberado:
            try:
                valor = float(input("Digite o valor do saque: "))
                if valor > 0 and valor <= self.saldo:
                    self.saldo -= valor
                    print(f"Saque de R${valor:.2f} realizado com sucesso!")
                else:
                    print("Valor inválido ou saldo insuficiente.")
            except ValueError:
                print("Digite um valor numérico válido.")
            finally:
                self.acessoLiberado = False
        else:
            print("Acesso não liberado.")


    def extrato(self):
        if self.acessoLiberado:
            print(f"\nExtrato da conta de {self.nomeProprietario}:")
            print(f"Saldo atual: R${self.saldo:.2f}")
            self.acessoLiberado = False
        else:
            print("Acesso não liberado.")


    def excluir_conta(self):
        if self.acessoLiberado:
            confirmacao = input("Tem certeza que deseja excluir a conta? (s/n): ")
            if confirmacao.lower() == 's':
                if self in contas_bancarias:
                    contas_bancarias.remove(self)
                    print("Conta excluída com sucesso!")
            else:
                print("Exclusão cancelada.")
            self.acessoLiberado = False
        else:
            print("Acesso não liberado.")

class Conta_Corrente(Conta_Bancaria):
    def __init__(self, nomeProprietario, senha, tarifa):
        super().__init__(nomeProprietario, senha)
        self.tarifa = tarifa
        self.tarifaPaga = False


    def pagar_tarifa(self):
        if self.acessoLiberado:
            taxa = self.tarifa * self.saldo
            if self.saldo >= taxa:
                self.saldo -= taxa
                self.tarifaPaga = True
                print(f"Tarifa de R${taxa:.2f} paga com sucesso!")
            else:
                print("Saldo insuficiente para pagar a tarifa.")
            self.acessoLiberado = False
        else:
            print("Acesso não liberado.")

class Conta_Poupanca(Conta_Bancaria):
    def __init__(self, nomeProprietario, senha, rendimento):
        super().__init__(nomeProprietario, senha)
        self.rendimento = rendimento

class Conta_Conjunto(Conta_Bancaria):
    def __init__(self, nomeProprietario, senha, co_proprietarios, tarifa):
        super().__init__(nomeProprietario, senha)
        self.co_proprietarios = list(co_proprietarios)
        self.tarifa = tarifa
        self.tarifaPaga = False

    def pagar_tarifa(self):
        if self.acessoLiberado:
            taxa = self.tarifa * self.saldo
            if self.saldo >= taxa:
                self.saldo -= taxa
                self.tarifaPaga = True
                print(f"Tarifa de R${taxa:.2f} paga com sucesso!")
            else:
                print("Saldo insuficiente para pagar a tarifa.")


            self.acessoLiberado = False
        else:
            print("Acesso não liberado.")

    def adicionar_co_proprietario(self):
        if self.acessoLiberado:
            novo_co_proprietario = input(
                "Digite o nome do novo co-proprietário: "
            ).strip()
            if novo_co_proprietario and novo_co_proprietario not in self.co_proprietarios:
                self.co_proprietarios.append(novo_co_proprietario)
                print(f"{novo_co_proprietario} adicionado com sucesso!")
            else:
                print("Nome inválido ou já cadastrado.")

            self.acessoLiberado = False
        else:
            print("Acesso não liberado.")

    def excluir_co_proprietario(self):
        if self.acessoLiberado:
            co_proprietario = input(
                "Digite o nome do co-proprietário a ser removido: "
            )
            if co_proprietario in self.co_proprietarios:
                self.co_proprietarios.remove(co_proprietario)
                print(f"{co_proprietario} removido com sucesso!")
            else:
                print("Co-proprietário não encontrado.")
            self.acessoLiberado = False
        else:
            print("Acesso não liberado.")