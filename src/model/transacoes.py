class TransacoesModel:
    def __init__(
        self,
        conta_destino_id,
        tipo,
        status,
        valor,
        realizado_em,
        id=None,
        conta_origem_id=None,
        descricao=None,
    ):
        self.id = id
        self.conta_origem_id = conta_origem_id
        self.conta_destino_id = conta_destino_id
        self.tipo = tipo
        self.status = status
        self.verificar_valor(valor)
        self.descricao = descricao
        self.realizado_em = realizado_em

    def verificar_valor(self, valor):
        if valor > 0:
            self.valor = valor
        else:
            raise ValueError("Transação inválida, informe um valor acima de R$0,00")
