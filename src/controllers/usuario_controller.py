from werkzeug.security import generate_password_hash, check_password_hash
from src.models.usuario import UsuarioModel
from src.repository.usuario import UsuarioRepository


class UsuarioController:
    def __init__(self):
        self.usuario_repo = UsuarioRepository()
    
    def registrar_usuario(self, nome, cpf, data_nascimento, email, senha_pura, tipo_pessoa, is_admin=False):
        senha_criptografada = generate_password_hash(senha_pura)
        
        novo_usuario = UsuarioModel(
            nome=nome,
            cpf=cpf,
            data_nascimento=data_nascimento,
            email=email,
            senha_hash=senha_criptografada,
            is_admin=is_admin,
            tipo=tipo_pessoa
        )
        
        novo_id = self.usuario_repo.criar(novo_usuario)
        return novo_id
    
    def autenticar_usuario(self, email, senha_pura):
        usuario_db = self.usuario_repo.buscar_por_email(email)
        
        if not usuario_db:
            return None
        
        hash_salvo = usuario_db[5]
        
        if check_password_hash(hash_salvo, senha_pura):
            return usuario_db
        else:
            return None
        