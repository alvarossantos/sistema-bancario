from src.model.transacoes import TransacoesModel
from src.database.conexao import BancoDeDados


class TransacoesRepository:
    def criar(self, transacao: TransacoesModel):
        sql = """
        INSERT INTO transacoes (conta_origem_id, conta_destino_id, tipo, status, valor, realizado_em)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id;
        """
        params = (
            transacao.conta_origem_id,
            transacao.conta_destino_id,
            transacao.tipo,
            transacao.status,
            transacao.valor,
            transacao.realizado_em,
        )
        
        with BancoDeDados() as cursor:
            cursor.execute(sql, params)
            novo_id = cursor.fetchone()[0]
            return novo_id
    
    def buscar_por_id(self, id: int):
        sql = """
        SELECT * FROM transacoes WHERE id = %s;
        """
        params = (id,)
        
        with BancoDeDados() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchone()
    
    def buscar_por_conta(self, conta_id: int):
        sql = """
        SELECT * FROM transacoes WHERE conta_origem_id = %s OR conta_destino_id = %s;
        """
        params = (conta_id, conta_id)
        
        with BancoDeDados() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchall()
    
    def listar_todos(self):
        sql = """
        SELECT * FROM transacoes;
        """
        
        with BancoDeDados() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()
