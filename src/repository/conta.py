class ContaRepository:
    def criar(self, conta: ContaModel):
        sql = """
        INSERT INTO contas (usuario_id, numero_conta, agencia, tipo, saldo, limite_emprestimo, ativa)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING id;
        """
        params = {
            conta.usuario_id,
            conta.numero_conta,
            conta.agencia,
            conta.tipo,
            conta.saldo,
            conta.limite_emprestimo,
            conta.ativa,
        }
        
        with BancoDeDados() as cursor:
            cursor.execute(sql, params)
            novo_id = cursor.fetchone()[0]
            return novo_id
    
    def editar(self, conta: ContaModel):
        sql = """
        UPDATE contas SET numero_conta = %s, agencia = %s, tipo = %s, saldo = %s, limite_emprestimo = %s, ativa = %s WHERE id = %s
        RETURNING id;
        """
        params = {
            conta.numero_conta,
            conta.agencia,
            conta.tipo,
            conta.saldo,
            conta.limite_emprestimo,
            conta.ativa,
            conta.id,
        }
        
        with BancoDeDados() as cursor:
            cursor.execute(sql, params)