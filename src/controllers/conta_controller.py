from abc import ABC, abstractmethod
from src.repository.conta import ContaRepository
from src.repository.transacoes import TransacoesRepository
from src.models.transacoes import TransacoesModel


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
    
    def depositar(self, conta_id: id, valor: float):
        """Executa um depósito aumentando o saldo e registrando a transação."""
        conta = self.conta_repo.buscar_por_id(conta_id)
        if not conta:
            raise Exception("Conta não encontrada.")
        
        conta.saldo += valor
        self.conta_repo.editar(conta)
        
        nova_transacao = TransacoesModel(conta_id, "DEPOSITO", valor)
        self.transacao_repo.criar(nova_transacao)
        return True
    
    def sacar(self, conta_id: int, valor: float):
        """Executa um levantamento validandno se existe saldo suficiente e registrando a transação."""
        conta = self.conta_repo.buscar_por_id(conta_id)
        if not conta:
            raise ValueError("Conta não encontrada.")
        
        if conta.saldo < valor:
            raise ValueError("Saldo insuficiente para esta operação.")

        conta.saldo -= valor
        self.conta_repo.editar(conta)
        
        nova_transacao = TransacoesModel(conta_id, "LEVANTAMENTO", valor)
        self.transacao_repo.criar(nova_transacao)
        return True
    
    def transferir(self, id_origem: int, id_destino: int, valor: float, estrategia: EstrategiaTransferencia):
        """
        Orquestra uma transferência entre contas aplicando a Estrategia de taxas.
        """        
        conta_origem = self.conta_repo.buscar_por_id(id_origem)
        conta_destino = self.conta_repo.buscar_por_id(id_destino)
        
        if not conta_origem or not conta_destino:
            raise ValueError("Uma ou ambas as contas não foram encontradas.")
        
        taxa = estrategia.calcular_taxa(valor)
        custo_total = valor + taxa
        
        if conta_origem.saldo < custo_total:
            raise ValueError("Saldo insuficiente para esta operação.")
        
        conta_origem.saldo -= custo_total
        self.conta_repo.editar(conta_origem)
        
        conta_destino.saldo += valor
        self.conta_repo.editar(conta_destino)
        
        t_debito = TransacoesModel(id_origem, "TRANSFERENCIA_SAIDA", valor)
        t_credito = TransacoesModel(id_destino, "TRANSFERENCIA_ENTRADA", valor)
        
        self.transacao_repo.criar(t_debito)
        self.transacao_repo.criar(t_credito)
        
        return f"Transferência realizada! Taxa aplicada: R$ {taxa:.2f}"
    