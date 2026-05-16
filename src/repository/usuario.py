from src.models.usuario import UsuarioModel
from src.database.conexao import BancoDeDados


class UsuarioRepository:
    def criar(self, usuario: UsuarioModel):
        sql = """
        INSERT INTO usuarios (nome, cpf, data_nascimento, email, senha_hash, is_admin)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id;
        """
        params = (
            usuario.nome,
            usuario.cpf,
            usuario.data_nascimento,
            usuario.email,
            usuario.senha_hash,
            usuario.is_admin
        )

        with BancoDeDados() as cursor:
            cursor.execute(sql, params)
            novo_id = cursor.fetchone()[0]
            cursor.connection.commit()
            return novo_id
    
    def editar(self, usuario: UsuarioModel):
        sql = """
        UPDATE usuarios SET nome = %s, email = %s, senha_hash = %s, ativo = %s WHERE id = %s
        RETURNING id;
        """
        params = (
            usuario.nome,
            usuario.email,
            usuario.senha_hash,
            usuario.ativo,
            usuario.id,
        )

        with BancoDeDados() as cursor:
            cursor.execute(sql, params)

    def buscar_por_email(self, email: str):
        sql = """
        SELECT * FROM usuarios WHERE email = %s;
        """
        params = (email,)
        
        with BancoDeDados() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchone()
    
    def buscar_por_id(self, id: int):
        sql = """
        SELECT * FROM usuarios WHERE id = %s;
        """
        params = (id,)
        
        with BancoDeDados() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchone()
    
    def listar_todos(self):
        sql = """
        SELECT * FROM usuarios WHERE ativo = TRUE ORDER BY criado_em DESC;
        """
        
        with BancoDeDados() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()