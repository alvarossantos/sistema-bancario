-- =========================================================
-- ESQUEMA BANCÁRIO AVANÇADO
-- =========================================================

CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- =========================================================
-- TIPOS E ENUMS
-- =========================================================

CREATE TYPE tipo_conta AS ENUM ('corrente', 'poupanca');

CREATE TYPE tipo_transacao AS ENUM (
    'pix', 'transferencia', 'deposito', 'saque', 'emprestimo', 'pagamento'
);

CREATE TYPE status_transacao AS ENUM ('pendente', 'concluido', 'falhou', 'estornado');

-- =========================================================
-- TABELA: usuarios (Com Soft Delete)
-- =========================================================

CREATE TABLE usuarios (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome VARCHAR(150) NOT NULL,
    cpf CHAR(11) NOT NULL UNIQUE,
    data_nascimento DATE NOT NULL,
    email VARCHAR(255) UNIQUE,
    senha_hash TEXT NOT NULL,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    deletado_em TIMESTAMP, -- Soft Delete
    criado_em TIMESTAMP NOT NULL DEFAULT NOW(),
    atualizado_em TIMESTAMP NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_cpf_numerico CHECK (cpf ~ '^[0-9]{11}$'),
    CONSTRAINT chk_maioridade CHECK (data_nascimento <= CURRENT_DATE - INTERVAL '18 years')
);

CREATE INDEX idx_usuarios_ativo ON usuarios(ativo) WHERE ativo IS TRUE;

-- =========================================================
-- TABELA: contas
-- =========================================================

CREATE TABLE contas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    usuario_id UUID NOT NULL,
    numero_conta BIGSERIAL UNIQUE,
    agencia VARCHAR(10) NOT NULL DEFAULT '0001',
    tipo tipo_conta NOT NULL,
    saldo NUMERIC(20,2) NOT NULL DEFAULT 0.00, -- Aumentada a precisão
    limite_emprestimo NUMERIC(15,2) NOT NULL DEFAULT 0.00,
    ativa BOOLEAN NOT NULL DEFAULT TRUE,
    criada_em TIMESTAMP NOT NULL DEFAULT NOW(),
    atualizada_em TIMESTAMP NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_conta_usuario FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE RESTRICT,
    CONSTRAINT chk_saldo_valido CHECK (saldo >= 0)
);

-- =========================================================
-- TABELA: auditoria_saldos
-- Registra quem mudou o que e quando (Histórico crítico)
-- =========================================================

CREATE TABLE auditoria_saldos (
    id BIGSERIAL PRIMARY KEY,
    conta_id UUID NOT NULL,
    saldo_anterior NUMERIC(20,2),
    saldo_novo NUMERIC(20,2),
    operacao TEXT NOT NULL, -- 'UPDATE', 'INSERT', etc
    usuario_db TEXT DEFAULT current_user,
    data_alteracao TIMESTAMP DEFAULT NOW()
);

-- =========================================================
-- TABELA: transacoes (Com Status)
-- =========================================================

CREATE TABLE transacoes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conta_origem_id UUID,
    conta_destino_id UUID,
    tipo tipo_transacao NOT NULL,
    status status_transacao DEFAULT 'concluido',
    valor NUMERIC(20,2) NOT NULL,
    descricao TEXT,
    realizado_em TIMESTAMP NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_transacao_origem FOREIGN KEY (conta_origem_id) REFERENCES contas(id),
    CONSTRAINT fk_transacao_destino FOREIGN KEY (conta_destino_id) REFERENCES contas(id),
    CONSTRAINT chk_valor_positivo CHECK (valor > 0),
    CONSTRAINT chk_origem_ou_destino CHECK (conta_origem_id IS NOT NULL OR conta_destino_id IS NOT NULL),
    CONSTRAINT chk_contas_diferentes CHECK (conta_origem_id IS NULL OR conta_destino_id IS NULL OR conta_origem_id <> conta_destino_id)
);

-- =========================================================
-- TRIGGERS DE AUDITORIA E TIMESTAMP
-- =========================================================

-- Função para atualizar timestamp
CREATE OR REPLACE FUNCTION fn_atualizar_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.atualizado_em = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Função para log de auditoria de saldo
CREATE OR REPLACE FUNCTION fn_log_auditoria_saldo()
RETURNS TRIGGER AS $$
BEGIN
    IF (OLD.saldo <> NEW.saldo) THEN
        INSERT INTO auditoria_saldos (conta_id, saldo_anterior, saldo_novo, operacao)
        VALUES (OLD.id, OLD.saldo, NEW.saldo, TG_OP);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_usuarios_timestamp BEFORE UPDATE ON usuarios FOR EACH ROW EXECUTE FUNCTION fn_atualizar_timestamp();
CREATE TRIGGER trg_contas_timestamp BEFORE UPDATE ON contas FOR EACH ROW EXECUTE FUNCTION fn_atualizar_timestamp();
CREATE TRIGGER trg_auditoria_saldo AFTER UPDATE ON contas FOR EACH ROW EXECUTE FUNCTION fn_log_auditoria_saldo();

-- =========================================================
-- FUNÇÃO DE TRANSFERÊNCIA (Versão Robusta)
-- =========================================================

CREATE OR REPLACE FUNCTION realizar_transferencia(
    p_conta_origem UUID,
    p_conta_destino UUID,
    p_valor NUMERIC(20,2)
)
RETURNS VOID AS $$
DECLARE
    v_saldo_origem NUMERIC(20,2);
    v_destino_existe BOOLEAN;
BEGIN
    -- 1. Valida se a conta de destino existe antes de qualquer coisa
    SELECT EXISTS(SELECT 1 FROM contas WHERE id = p_conta_destino AND ativa = TRUE) INTO v_destino_existe;
    IF NOT v_destino_existe THEN
        RAISE EXCEPTION 'Conta de destino não encontrada ou inativa';
    END IF;

    -- 2. Bloqueia a conta de origem para evitar concorrência (Race Condition)
    SELECT saldo INTO v_saldo_origem
    FROM contas
    WHERE id = p_conta_origem AND ativa = TRUE
    FOR UPDATE;

    IF v_saldo_origem IS NULL THEN
        RAISE EXCEPTION 'Conta de origem não encontrada ou inativa';
    END IF;

    -- 3. Valida saldo
    IF v_saldo_origem < p_valor THEN
        RAISE EXCEPTION 'Saldo insuficiente para a transação';
    END IF;

    -- 4. Executa os débitos e créditos
    UPDATE contas SET saldo = saldo - p_valor WHERE id = p_conta_origem;
    UPDATE contas SET saldo = saldo + p_valor WHERE id = p_conta_destino;

    -- 5. Registra a transação
    INSERT INTO transacoes (conta_origem_id, conta_destino_id, tipo, status, valor, descricao)
    VALUES (p_conta_origem, p_conta_destino, 'transferencia', 'concluido', p_valor, 'Transferência bancária via sistema');

EXCEPTION
    WHEN OTHERS THEN
        -- Aqui você poderia inserir um registro em transacoes com status 'falhou' antes de propagar o erro
        RAISE;
END;
$$ LANGUAGE plpgsql;
