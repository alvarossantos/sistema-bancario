class ContaModel:
    def __init__(
        self,
        usuario_id,
        numero_conta,
        agencia,
        tipo,
        saldo,
        limite_emprestimo,
        ativa,
        id=None,
        criada_em=None,
        atualizada_em=None,
    ):
        self.id = id
        self.usuario_id = usuario_id
        self.numero_conta = numero_conta
        self.agencia = agencia
        self.tipo = tipo
        self.saldo = saldo
        self.limite_emprestimo = limite_emprestimo
        self.ativa = ativa
        self.criada_em = criada_em
        self.atualizada_em = atualizada_em
