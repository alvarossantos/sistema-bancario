class AuditoriaModel:
    def __init__(
        self,
        conta_id,
        saldo_anterior,
        saldo_novo,
        operacao,
        usuario_db,
        data_alteracao,
        id=None,
    ):
        self.id = id
        self.conta_id = conta_id
        self.saldo_anterior = saldo_anterior
        self.saldo_novo = saldo_novo
        self.operacao = operacao
        self.usuario_db = usuario_db
        self.data_alteracao = data_alteracao
