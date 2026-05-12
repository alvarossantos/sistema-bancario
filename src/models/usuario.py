class UsuarioModel:
    def __init__(
        self,
        nome,
        cpf,
        email,
        senha_hash,
        ativo,
        id=None,
        deletado_em=None,
        criado_em=None,
        atualizado_em=None,
    ):
        self.id = id
        self.nome = nome
        self.verificar_cpf(cpf)
        self.verificar_email(email)
        self.senha_hash = senha_hash
        self.ativo = ativo
        self.deletado_em = deletado_em
        self.criado_em = criado_em
        self.atualizado_em = atualizado_em

    def verificar_cpf(self, cpf):
        if cpf.isdigit() and len(cpf) == 11:
            self.cpf = cpf
        else:
            raise ValueError(
                "CPF inválido, somente números são aceitos e deve ter 11 dígitos."
            )

    def verificar_email(self, email):
        if "@" in email:
            self.email = email
        else:
            raise ValueError(f"Email inválido, não possui '@': {email}")
