from src.models.transacoes import TransacoesModel
from src.database.conexao import BancoDeDados


class TransacoesRepository:
    def criar(self, transacao: TransacoesModel):
        sql = """
        INSERT INTO transacoes (conta_origem_id, conta_destino_id, tipo, status, valor, realizado_em)
        VALUES (%s, %s, %s::tipo_transacao, %s::status_transacao, %s, %s)
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

    def buscar_detalhes_comprovante(self, transacao_id, conta_logada_id):
        """
        Executa a query no banco de dados para buscar os detalhes da transação.
        Retorna a tupla com os dados ou None se não encontrar.
        """
        sql = """
        SELECT t.id, t.tipo, t.status, t.valor, t.realizado_em,
               co.numero_conta as conta_origem,
               cd.numero_conta as conta_destino,
               ud.nome as nome_destino,
               uo.nome as nome_origem
        FROM transacoes t
        LEFT JOIN contas co ON t.conta_origem_id = co.id
        LEFT JOIN usuarios uo ON co.usuario_id = uo.id
        LEFT JOIN contas cd ON t.conta_destino_id = cd.id
        LEFT JOIN usuarios ud ON cd.usuario_id = ud.id
        WHERE t.id = %s AND (t.conta_origem_id = %s OR t.conta_destino_id = %s);
        """
        
        with BancoDeDados() as cursor:
            cursor.execute(sql, (transacao_id, conta_logada_id, conta_logada_id))
            return cursor.fetchone()