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

def passar_mes():
    global mes
    mes += 1
    print(f"Passou-se um mês. Agora estamos no mês {mes}.")
    for conta in contas_bancarias:
        if isinstance(conta, Conta_Corrente) or isinstance(conta, Conta_Conjunto):
            if not conta.tarifaPaga:
                conta.bloqueado = True
                print(
                    f"Conta de {conta.nomeProprietario} bloqueada "
                    "por tarifa não paga."
                )
            else:
                conta.tarifaPaga = False
                print(f"Tarifa paga na conta de {conta.nomeProprietario}.")
        elif isinstance(conta, Conta_Poupanca):
            rendimento = conta.saldo * conta.rendimento
            conta.saldo += rendimento
            print(
                f"Rendimento de R${rendimento:.2f} aplicado "
                f"na conta de {conta.nomeProprietario}."
            )

def criar_contaCorrente():
    print("\nCriação de conta corrente")
    nome = input("Nome do proprietário: ")
    senha = input("Crie uma senha: ")
    for conta in contas_bancarias:
        if isinstance(conta, Conta_Corrente) and conta.nomeProprietario == nome:
            print("Já existe uma conta corrente com esse nome!")
            return
    contas_bancarias.append(Conta_Corrente(nome, senha, 0.02))
    print("Conta corrente criada com sucesso!")

def criar_contaPoupanca():
    print("\nCriação de conta poupança")
    nome = input("Nome do proprietário: ")
    senha = input("Crie uma senha: ")
    for conta in contas_bancarias:
        if isinstance(conta, Conta_Poupanca) and conta.nomeProprietario == nome:
            print("Já existe uma conta poupança com esse nome!")
            return
    contas_bancarias.append(Conta_Poupanca(nome, senha, 0.02))
    print("Conta poupança criada com sucesso!")

def criar_contaConjunto():
    print("\nCriação de conta conjunta")
    nome = input("Nome do proprietário principal: ")
    senha = input("Crie uma senha: ")
    co_proprietario = input("Nome do primeiro co-proprietário: ")
    for conta in contas_bancarias:
        if isinstance(conta, Conta_Conjunto) and conta.nomeProprietario == nome:
            print("Já existe uma conta conjunta com esse proprietário!")
            return
    contas_bancarias.append(
        Conta_Conjunto(nome, senha, [co_proprietario], 0.02)
    )
    print("Conta conjunta criada com sucesso!")
    
def localizar_conta(nome, tipo=None):
    encontradas = []
    for conta in contas_bancarias:
        if conta.nomeProprietario == nome:
            if tipo is None or isinstance(conta, tipo):
                encontradas.append(conta)
    if not encontradas:
        print("Conta não encontrada.")
        return None
    if len(encontradas) == 1:
        return encontradas[0]
    print("\nForam encontradas várias contas:")
    for i, conta in enumerate(encontradas, 1):
        print(f"{i} - {type(conta).__name__} | Saldo: R${conta.saldo:.2f}")
    try:
        escolha = int(input("Escolha a conta: "))
        if 1 <= escolha <= len(encontradas):
            return encontradas[escolha - 1]
    except ValueError:
        pass
    print("Escolha inválida.")
    return None

def menu():
    while True:
        print("\n===============================")
        print("Bem-vindo ao Banco Tramontina!")
        print("===============================")

        print("""
1 - Criar conta
2 - Depositar
3 - Sacar
4 - Extrato
5 - Excluir conta
6 - Adicionar ou excluir co-proprietário
7 - Pagar tarifa
8 - Passar mês
0 - Sair
""")

        try:
            opcao = int(input("Digite a opção desejada: "))
        except ValueError:
            print("Digite uma opção numérica.")
            continue
        if opcao == 0:
            break
        elif opcao == 1:
            try:
                tipo_conta = int(input(
                    "1 - Conta Corrente\n"
                    "2 - Conta Poupança\n"
                    "3 - Conta Conjunta\n"
                    "Escolha: "
                ))
                if tipo_conta == 1:
                    criar_contaCorrente()
                elif tipo_conta == 2:
                    criar_contaPoupanca()
                elif tipo_conta == 3:
                    criar_contaConjunto()
                else:
                    print("Tipo de conta inválido.")
            except ValueError:
                print("Digite uma opção válida.")
           
        elif opcao in (2, 3, 4, 5, 6, 7):
            nome = input("Digite o nome do proprietário: ")

            conta = localizar_conta(nome)

            if conta is None:
                continue

            if opcao == 7 and isinstance(conta, (Conta_Corrente, Conta_Conjunto)):
                if conta.bloqueado:
                    print("Conta bloqueada por tentativas de senha.")
                    continue
                conta.liberar_acesso()
                if conta.acessoLiberado:
                    conta.pagar_tarifa()
                continue
            if conta.bloqueado:
                print("Conta bloqueada! Entre em contato com o banco.")
                continue
            conta.liberar_acesso()
            if not conta.acessoLiberado:
                continue

            if opcao == 2:
                conta.depositar()


            elif opcao == 3:
                conta.sacar()


            elif opcao == 4:
                conta.extrato()


            elif opcao == 5:
                conta.excluir_conta()


            elif opcao == 6:
                if isinstance(conta, Conta_Conjunto):
                    acao = input(
                        "Digite 'adicionar' ou 'excluir': "
                    ).lower()
                    if acao == 'adicionar':
                        conta.adicionar_co_proprietario()
                    elif acao == 'excluir':
                        conta.excluir_co_proprietario()
                    else:
                        print("Ação inválida.")
                        conta.acessoLiberado = False
                else:
                    print("Essa opção é exclusiva de contas conjuntas.")
                    conta.acessoLiberado = False


            elif opcao == 7:
                print("Essa conta não possui tarifa.")
                conta.acessoLiberado = False


        elif opcao == 8:
            passar_mes()


        else:
            print("Opção inválida!")


menu()


print("\nObrigado por utilizar o Banco Tramontina! Até a próxima!")
