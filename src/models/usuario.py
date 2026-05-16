import re
from datetime import datetime, date


class UsuarioModel:
    def __init__(
        self,
        nome,
        cpf,
        data_nascimento,
        email,
        senha_hash,
        is_admin=False,
        tipo='PF',
        id=None,
        ativo=True,
    ):
        self.id = id
        self.nome = nome
        self.cpf = self.verificar_cpf(cpf)
        self.data_nascimento = self.verificar_nascimento(data_nascimento)
        self.email = self.verificar_email(email)
        self.senha_hash = senha_hash
        self.is_admin = is_admin
        self.tipo = tipo
        self.ativo = ativo

    def verificar_cpf(self, cpf):
        cpf_limpo = re.sub(r'[^0-9]', '', str(cpf))
        if len(cpf_limpo) != 11:
            raise ValueError(
                "CPF inválido, somente números são aceitos e deve ter 11 dígitos."
            )
        return cpf_limpo
    
    def verificar_nascimento(self, data_str):
        try:
            data_nasc = datetime.strptime(data_str, "%Y-%m-%d").date()
            hoje = date.today()
            idade = hoje.year - data_nasc.year - ((hoje.month, hoje.day) < (data_nasc.month, data_nasc.day))
            
            if idade < 18:
                raise ValueError("Necessário ter pelo menos 18 anos para se cadastrar.")
            
            return data_str
        
        except ValueError as e:
            if "18 anos" in str(e):
                raise e
            raise ValueError("Formato de data inválido.")

    def verificar_email(self, email):
        if "@" not in email or "." not in email:
            raise ValueError("Formato de e-mail inválido.")
        return email
