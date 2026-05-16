from abc import ABC, abstractmethod
from src.repository.conta import ContaRepository
from src.models.conta import ContaModel
from src.repository.transacoes import TransacoesRepository
from src.models.transacoes import TransacoesModel
import random
from datetime import datetime


class EstrategiaTransferencia(ABC):
    @abstractmethod
    def calcular_taxa(self, valor: float) -> float:
        pass

class TransferenciaPix(EstrategiaTransferencia):
    def calcular_taxa(self, valor: float) -> float:
        return 0.0

class TransferenciaTED(EstrategiaTransferencia):
    def calcular_taxa(self, valor: float) -> float:
        return 10.50

class ContaController:
    def __init__(self):
        self.conta_repo = ContaRepository()
        self.transacao_repo = TransacoesRepository()
        
    def criar_conta_automatica(self, usuario_id, tipo_pessoa, tipo_conta):
        """Gera automaticamente os dados bancários e persiste a conta."""
        agencias_existentes = ["0001", "0002", "0345", "1010"]
        agencia = random.choice(agencias_existentes)

        numero_conta = str(random.randint(10000, 99999))
        
        if tipo_conta == 'corrente':
            # Se for corrente e PJ, limite é 2000. Se for corrente e PF, é 200
            limite = 2000.0 if tipo_pessoa == 'PJ' else 200.0
        else:
            # Se for poupança, o limite é 0
            limite = 0.0
        
        nova_conta = ContaModel(
            usuario_id=usuario_id,
            numero_conta=numero_conta,
            agencia=agencia,
            tipo=tipo_conta,
            saldo=0.0,
            limite_emprestimo=limite,
            ativa=True
        )
        
        return self.conta_repo.criar(nova_conta)
    
    # Simular depósito
    def efetuar_deposito(self, usuario_id, valor_str):
        """Valida o valor recebido, atualiza o saldo da conta e registra a transação."""
        try:
            valor = float(valor_str)        
            if valor <= 0:
                raise ValueError("O valor do depósito deve ser maior que zero.")
        except ValueError:
            raise ValueError("O valor de depósito inválido. Insira um número válido.")
            
        conta_db = self.conta_repo.buscar_por_usuario(usuario_id)
        if not conta_db:
            raise ValueError("Conta não encontrada.")
        
        # Recostruir o objeto (tupla da conta)
        # 0:id, 1:usuario_id, 2:numero_conta, 3:agencia, 4:tipo, 5:saldo, 6:limite, 7:ativa
        saldo_atual = float(conta_db[5])
        novo_saldo = saldo_atual + valor
        
        # Atualizar o saldo na tabela 'contas'
        self.conta_repo.atualizar_saldo(conta_db[0], novo_saldo)
        
        nova_transacao = TransacoesModel(
            conta_destino_id=conta_db[0],
            tipo="deposito",
            status="concluido",
            valor=valor,
            realizado_em=datetime.now()
        )
        self.transacao_repo.criar(nova_transacao)
        
        return novo_saldo
    
    def efetuar_saque(self, usuario_id, valor_str):
        """Executa um levantamento validandno se existe saldo suficiente e registrando a transação."""
        try:
            valor = float(valor_str)
            if valor <= 0:
                raise ValueError("O valor do saque deve ser maior que zero.")
        except ValueError:
            raise ValueError("O valor de saque inválido. Insira um número válido.")
        
        conta_db = self.conta_repo.buscar_por_usuario(usuario_id)
        if not conta_db:
            raise ValueError("Conta não encontrada.")
        
        conta_id = conta_db[0]
        saldo_atual = float(conta_db[5])
        
        if saldo_atual < valor:
            raise ValueError("Saldo insuficiente para realizar este saque.")

        novo_saldo = saldo_atual - valor
        self.conta_repo.atualizar_saldo(conta_id, novo_saldo)
        
        nova_transacao = TransacoesModel(
            conta_origem_id=conta_id, 
            conta_destino_id=None,
            tipo="saque",
            status="concluido", 
            valor=valor, 
            realizado_em=datetime.now()
        )
        self.transacao_repo.criar(nova_transacao)
        return True
    
    def transferir(self, id_origem, identificador_destino, valor_str, metodo_envio):
        """
        Orquestra uma transferência entre contas aplicando a Estrategia de taxas.
        """
        try:
            valor = float(valor_str)
            if valor <= 0:
                raise ValueError("O valor da transferência deve ser maior que zero.")
        except ValueError:
            raise ValueError("O valor de transferência inválido. Insira um número válido.")
        
        conta_origem = self.conta_repo.buscar_por_id(id_origem)
        if not conta_origem:
            raise ValueError("A sua conta de origem não foi encontrada.")
        
        if metodo_envio == "PIX":
            estrategia = TransferenciaPix()
            cpf_limpo = identificador_destino.strip() if identificador_destino else ""
            conta_destino = self.conta_repo.buscar_por_cpf(cpf_limpo)
            if not conta_destino:
                raise ValueError("A conta de destino não foi encontrada.")
        
        elif metodo_envio == "TED":
            estrategia = TransferenciaTED()
            numero_limpo = identificador_destino.strip() if identificador_destino else ""
            conta_destino = self.conta_repo.buscar_por_numero(numero_limpo)
            if not conta_destino:
                raise ValueError("A conta de destino não foi encontrada.")
            
        else:
            raise ValueError("Método de envio não suportado.")
        
        taxa = estrategia.calcular_taxa(valor)
        custo_total = valor + taxa
        
        saldo_origem = float(conta_origem[5])
        if saldo_origem < custo_total:
            raise ValueError(f"Saldo insuficiente. Custo total com taxa: R$ {custo_total:.2f}")
        
        novo_saldo_origem = saldo_origem - custo_total
        self.conta_repo.atualizar_saldo(conta_origem[0], novo_saldo_origem)
        
        novo_saldo_destino = float(conta_destino[5]) + valor
        self.conta_repo.atualizar_saldo(conta_destino[0], novo_saldo_destino)
        
        nova_transacao = TransacoesModel(
            conta_origem_id=conta_origem[0],
            conta_destino_id=conta_destino[0],
            tipo="transferencia",
            status="concluido",
            valor=valor,
            realizado_em=datetime.now()
        )
        
        self.transacao_repo.criar(nova_transacao)
        
        dados_comprovante = {
            "metodo": metodo_envio,
            "valor": valor,
            "taxa": taxa,
            "total_debitado": custo_total,
            "destino": identificador_destino,
            "data_hora": datetime.now().strftime("%d/%m/%Y às %H:%M:%S"),
            "autenticacao": f"NEX{random.randint(10000000, 99999999)}BR"
        }
        
        return dados_comprovante
    
    def gerar_comprovante_por_id(self, transacao_id, usuario_id):
        """
        Busca uma transação específica e formata os dados para o comprovante,
        garantindo que a transação pertence à conta do usuário.
        """
        conta_usuario = self.conta_repo.buscar_por_usuario(usuario_id)
        if not conta_usuario:
            return None
        conta_logada_id = conta_usuario[0]
        
        transacao_dados = self.transacao_repo.buscar_detalhes_comprovante(transacao_id, conta_logada_id)
        if not transacao_dados:
            return None
        
        # transacao_dados: [0]=id, [1]=tipo, [2]=status, [3]=valor, [4]=realizado_em
        # [5]=conta_origem_id, [6]=conta_destino_id, [7]=nome_destino, [8]=nome_origem
        valor = float(transacao_dados[3])
        tipo_transacao = transacao_dados[1]
        
        if tipo_transacao == 'transferencia':
            destino = f"{transacao_dados[7]} (Conta: {transacao_dados[6]})" if transacao_dados[7] else f"Conta: {transacao_dados[6]}"
            metodo = "Transferência Eletrônica"
        elif tipo_transacao == 'deposito':
            destino = f"Própria Conta (Conta: {transacao_dados[5]})"
            metodo = "Depósito em Caixa"
        else:
            destino = "Retirada de Recursos"
            metodo = "Saque Automático"
        
        id_str = str(transacao_dados[0]).replace('-', '').upper()[:8]
        
        return {
            "metodo": metodo,
            "valor": valor,
            "taxa": 0.0,
            "total_debitado": valor,
            "destino": destino,
            "data_hora": transacao_dados[4].strftime("%d/%m/%Y às %H:%M:%S") if transacao_dados[4] else 'N/A',
            "autenticacao": f"NEX{id_str}-BR"
        }
