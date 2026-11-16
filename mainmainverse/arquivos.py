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
