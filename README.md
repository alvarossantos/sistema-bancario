Com certeza! O seu ficheiro `README.md` atual já está muito bom e explica bem a arquitetura. No entanto, podemos torná-lo ainda mais atrativo, profissional e completo, adicionando "badges" (selos visuais), destacando as tecnologias de frontend (como o Bootstrap 5 e o Chart.js que utilizámos) e corrigindo a secção de instalação (uma vez que agora você tem um ficheiro `requirements.txt` completo).

Aqui está uma versão melhorada e muito mais elegante do seu `README.md`. Pode copiar este código e substituir o conteúdo atual do seu ficheiro:

```markdown
# 🏦 NexBank - Sistema Bancário Web

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.1.3-black.svg?logo=flask&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Advanced-336791.svg?logo=postgresql&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3.svg?logo=bootstrap&logoColor=white)

O **NexBank** é um sistema bancário web robusto e responsivo que simula operações financeiras do mundo real. O sistema permite o registo de utilizadores (Pessoa Física e Jurídica), a gestão automática de contas bancárias e a realização de diversas transações financeiras com segurança, auditoria e persistência de dados.

Desenvolvido como projeto prático para a disciplina de Engenharia de Software II.

---

## 🚀 Funcionalidades Principais

O sistema oferece interfaces e funcionalidades distintas para dois perfis de acesso:

### 👤 Área do Cliente
* **Abertura de Conta Inteligente:** Criação automática de agência e número de conta (Corrente ou Poupança) com base no perfil (PF/PJ).
* **Operações de Caixa:** Depósitos e Levantamentos em tempo real.
* **Transferências Avançadas:** Envio de fundos via **PIX** (isento de taxas) ou **TED** (com taxa de R$ 10,50 calculada dinamicamente).
* **Extrato Dinâmico:** Histórico cronológico de todas as operações com identificação visual de entradas e saídas.
* **Comprovativos:** Geração de talões de transferência eletrónicos formatados e prontos para impressão/PDF, com códigos únicos de autenticação.

### 🛡️ Área do Administrador
* **Dashboard Analítico:** Painel com gráficos interativos (Chart.js) mostrando em tempo real o volume de depósitos, levantamentos e transferências, além do total global em custódia.
* **Gestão de Clientes:** Listagem completa de utilizadores registados, com indicação de níveis de privilégio (Admin vs Cliente).
* **Auditoria Global:** Tabela de monitorização de todas as transações que circulam entre contas, com cruzamento de dados (UUIDs).

---

## ⚙️ Arquitetura e Engenharia

Para garantir integridade, escalabilidade e manutenção, o sistema adota as seguintes abordagens e padrões de projeto de Engenharia de Software:

* **Padrões Arquiteturais:**
    * **MVC (Model-View-Controller):** Separação clara de responsabilidades.
    * **Repository Pattern:** Isola completamente as *queries* SQL (Data Access Layer) do restante do código, facilitando a troca de SGBD no futuro.
* **Padrões de Desenho (Design Patterns):**
    * **Strategy Pattern:** Implementado no cálculo de taxas (`EstrategiaTransferencia`, `TransferenciaPix`, `TransferenciaTED`) permitindo adicionar novos métodos de envio no futuro sem alterar o código base (`Open/Closed Principle`).
* **Segurança e Consistência (PostgreSQL):**
    * **ACID:** Foco total na consistência transacional.
    * **Triggers & Auditoria:** Função automatizada no banco (`fn_log_auditoria_saldo`) que regista numa tabela isolada qualquer alteração de saldo (quem, quando, saldo antigo e novo).
    * **Stored Procedures & Row-Level Locking:** Transações orquestradas no banco de dados (`FOR UPDATE`) para evitar condições de corrida (*Race Conditions*) em concorrências.
    * **UUIDs:** Chaves primárias universais para maior segurança, dificultando a enumeração de contas.
    * **Hashing:** Palavras-passe encriptadas utilizando o `werkzeug.security`.

---

## 🛠️ Tecnologias Utilizadas

**Backend:**
* Python 3.x
* Flask (Framework Web)
* Psycopg2-binary (Driver do BD)
* python-dotenv (Gestão de variáveis de ambiente)

**Base de Dados:**
* PostgreSQL (com extensão `pgcrypto`)

**Frontend:**
* HTML5 / CSS3 / Jinja2 (Templates Web)
* Bootstrap 5.3 (Grelha, Responsividade e Componentes)
* Chart.js (Gráficos no Dashboard Admin)
* FontAwesome (Ícones)
* Animações CSS Customizadas (Efeitos *Fade-In*, *Slide-Up* e *Card-Hover*)

---

## 📂 Estrutura do Projeto

```text
sistema-bancario/
├── app.py                     # Ponto de entrada (Aplicação Flask e Rotas)
├── banco.sql                  # Scripts DDL (Tabelas, Enums, Triggers e Procedures)
├── requirements.txt           # Dependências do projeto
└── src/
    ├── controllers/           # Regras de negócio e orquestração (Strategy Pattern)
    ├── database/              # Gestão de conexão com o PostgreSQL
    ├── models/                # Classes e entidades de domínio com validações
    ├── repository/            # Camada de Acesso a Dados (Queries SQL)
    └── views/templates/       # Interfaces de utilizador renderizadas (HTML)

```

---

## 💻 Como Rodar o Projeto Localmente

### Pré-requisitos

* Python 3.8+ instalado.
* PostgreSQL configurado e a correr.

### 1. Configurar a Base de Dados

1. Crie uma base de dados no seu servidor PostgreSQL (ex: `nexbank_db`).
2. Execute o script `banco.sql` para gerar toda a infraestrutura de dados:
```bash
psql -U seu_usuario -d nexbank_db -f banco.sql

```


3. Crie um ficheiro `.env` na raiz do projeto (verifique o ficheiro `src/database/conexao.py` para as chaves exatas) com as suas credenciais:
```env
DB_NAME=nexbank_db
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_PORT=5432

```



### 2. Configurar o Ambiente Python

1. Abra o terminal na pasta raiz do projeto e crie um ambiente virtual:
```bash
python -m venv venv

```


2. Ative o ambiente virtual:
* Linux/macOS: `source venv/bin/activate`
* Windows: `venv\Scripts\activate`


3. Instale todas as dependências oficiais:
```bash
pip install -r requirements.txt

```



### 3. Iniciar a Aplicação

Execute o ficheiro principal da aplicação:

```bash
python app.py

```

O servidor Flask iniciará. Aceda no seu navegador à morada:
👉 **`http://127.0.0.1:5000`**

### 👑 Como criar uma conta de Administrador

1. Aceda à aplicação web e crie uma conta normalmente (ex: usando o e-mail `admin@nexbank.com`).
2. No seu terminal SQL ou interface de base de dados (ex: pgAdmin), promova esse utilizador a administrador correndo:
```sql
UPDATE usuarios SET is_admin = true WHERE email = 'admin@nexbank.com';

```


3. Termine a sessão no site e volte a entrar. O menu de "Dashboard Admin" surgirá.

---

*Desenvolvido com ☕ e Python.*

```

### O que mudou:
1. **Design mais Premium:** Adicionei *badges* coloridas no topo e emojis nos títulos para tornar a leitura mais dinâmica e atrativa.
2. **Atualização Tecnológica:** Destaquei o uso do Bootstrap 5 e da *Chart.js*, que foram adicionados nas últimas fases do projeto.
3. **Engenharia:** Deixei muito explícito o uso do **Strategy Pattern**, dos UUIDs, do hashing e da arquitetura MVC limpa. Isto é excelente para quem estiver a avaliar o código.
4. **Instruções de Instalação:** Agora menciona a utilização correta do ficheiro `.env` para segurança das *passwords* do banco e atualiza a instrução para o `pip install -r requirements.txt` real.
5. **Configuração de Admin:** Inclui o passo final de como atribuir poderes de administrador via comando SQL, algo que vai poupar tempo a quem quiser testar o projeto a 100%.

```