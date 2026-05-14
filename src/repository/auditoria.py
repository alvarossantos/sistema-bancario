from src.model.auditoria import AuditoriaModel
from src.database.conexao import BancoDeDados


class AuditoriaRepository:
    def criar(self, auditoria: AuditoriaModel):
        sql = """
        INSERT INTO auditoria (conta_id, saldo_anterior, saldo_novo, operacao, usuario_db, data_alteracao)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id;
        """
        params = (
            auditoria.conta_id,
            auditoria.saldo_anterior,
            auditoria.saldo_novo,
            auditoria.operacao,
            auditoria.usuario_db,
            auditoria.data_alteracao,
        )

        with BancoDeDados() as cursor:
            cursor.execute(sql, params)
            novo_id = cursor.fetchone()[0]
            return novo_id

    def buscar_por_conta(self, conta_id: int):
        sql = """
        SELECT * FROM auditoria WHERE conta_id = %s ORDER BY data_alteracao DESC;
        """
        params = (conta_id,)

        with BancoDeDados() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchall()
