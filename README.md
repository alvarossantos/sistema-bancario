# NexBank - Sistema Bancário

O NexBank é um sistema bancário web robusto que simula operações financeiras do mundo real. O sistema permite o cadastro de usuários (Pessoa Física e Jurídica), gerenciamento de contas bancárias, e a realização de diversas transações financeiras com segurança e persistência de dados.

## 🚀 O que faz?

O sistema oferece funcionalidades para dois perfis de acesso:

*   **Clientes:** Podem criar contas, realizar login, efetuar depósitos, saques, consultar extratos, transferir fundos para outras contas usando diferentes métodos de pagamento (PIX ou TED) com cálculos dinâmicos de taxas, e visualizar comprovantes de transação.
*   **Administradores:** Têm acesso a um dashboard exclusivo de métricas (total em custódia, quantidade de operações globais), além da capacidade de listar todos os clientes e acompanhar todo o fluxo de transações do banco.

## ⚙️ Como funciona?

O projeto foi desenvolvido em **Python** utilizando o framework web **Flask**. 
Para garantir integridade, escalabilidade e manutenibilidade, o sistema adota as seguintes abordagens:

1.  **Arquitetura (MVC e Repository Pattern):**
    *   **Models:** Representam a estrutura de dados (ex: `TransacoesModel`) e fazem validações de domínio.
    *   **Controllers:** Contêm a lógica de negócio (ex: cálculo de taxas de TED vs PIX usando o *Design Pattern Strategy*), validam regras, e intermedeiam as ações da View para os Repositórios.
    *   **Repositories:** Isolam completamente as *queries* SQL do restante do código, sendo responsáveis pelas interações CRUD com o banco de dados.
    *   **Views:** Templates HTML renderizados via Flask integrados aos dados fornecidos pelos controllers.
2.  **Banco de Dados (PostgreSQL):**
    *   O banco foi modelado com foco na consistência transacional (ACID).
    *   Utiliza **Triggers** para log de auditoria automatizado (qualquer alteração de saldo é registrada na tabela `auditoria_saldos`).
    *   Possui **Stored Functions/Procedures** (ex: `realizar_transferencia`) com **Row-Level Locking (`FOR UPDATE`)** para evitar condições de corrida (*race conditions*) durante transações simultâneas.
    *   Trabalha com Soft Delete para usuários.

## 🛠️ Ferramentas Utilizadas

- **Linguagem:** Python 3.x
- **Framework Web:** Flask
- **Banco de Dados:** PostgreSQL
- **Driver de BD:** Psycopg2 (inferido pela modelagem síncrona relacional)
- **Frontend:** HTML, CSS, e Flask/Jinja2 (Templates)

## 📂 Estrutura do Projeto

```text
sistema-bancario/
├── app.py                  # Ponto de entrada (Rotas web e servidor Flask)
├── banco.sql               # Scripts DDL para criação das tabelas e banco de dados
├── src/
│   ├── controllers/        # Camada de lógica de negócio e regras (Strategy, etc)
│   ├── database/           # Gerenciamento de conexão com PostgreSQL
│   ├── models/             # Classes de modelo (Entidades de dados)
│   ├── repository/         # Camada de interação com o PostgreSQL (queries SQL)
│   └── views/templates/    # Interface do usuário (Páginas HTML renderizadas)
```

## 💻 Como Rodar o Projeto Localmente

### Pré-requisitos
*   Python 3.8+ instalado na máquina.
*   PostgreSQL configurado e rodando.

### Passo 1: Configurar o Banco de Dados
1.  Crie um banco de dados no seu servidor PostgreSQL local (ex: `nexbank_db`).
2.  Execute o script `banco.sql` no seu banco de dados recém-criado para gerar as tabelas, enums, triggers e procedures.
    ```bash
    psql -U seu_usuario -d nexbank_db -f banco.sql
    ```
3.  Certifique-se de configurar as credenciais do banco de dados no arquivo responsável (ex: `src/database/conexao.py` ou via variáveis de ambiente `.env`).

### Passo 2: Configurar o Ambiente Python
1.  Abra o terminal na pasta raiz do projeto.
2.  Crie um ambiente virtual (recomendado):
    ```bash
    python -m venv venv
    ```
3.  Ative o ambiente virtual:
    *   Linux/macOS: `source venv/bin/activate`
    *   Windows: `venv\Scripts\activate`
4.  Instale as dependências. Como não há um `requirements.txt` detalhado nesta documentação, instale os pacotes principais:
    ```bash
    pip install flask psycopg2-binary
    ```

### Passo 3: Rodar a Aplicação
1.  Ainda na pasta raiz do projeto, execute:
    ```bash
    python app.py
    ```
2.  O servidor Flask iniciará. Acesse no seu navegador a URL informada no terminal, geralmente:
    ```text
    http://127.0.0.1:5000
    ```

Pronto! Agora você já pode criar sua conta, efetuar o login e começar a realizar movimentações simuladas no NexBank.