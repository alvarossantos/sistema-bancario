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
    
    def buscar_por_id(self, id: int):
        sql = """
        SELECT * FROM contas WHERE id = %s;
        """
        params = (id)
        
        with BancoDeDados() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchone()
    
    def buscar_por_conta(self, numero_conta: int):
        sql = """
        SELECT * FROM contas WHERE numero_conta = %s;
        """
        params = (numero_conta)
        
        with BancoDeDados() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchone()
    
    def buscar_por_usuario(self, usuario_id: int):
        sql = """
        SELECT * FROM contas WHERE usuario_id = %s;
        """
        params = (usuario_id)
        
        with BancoDeDados() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchall()
    
    def desativar_conta(self, usuario: UsuarioModel):
        sql = """
        UPDATE contas SET ativa = %s WHERE usuario_id = %s
        RETURNING id;
        """
        params = (False, usuario.id)
        
        with BancoDeDados() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchone()