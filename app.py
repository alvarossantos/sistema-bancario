from flask import Flask, render_template, request, redirect, url_for, flash, session
from src.controllers.conta_controller import ContaController, TransferenciaPix, TransferenciaTED
from src.repository.usuario import UsuarioRepository
from src.controllers.usuario_controller import UsuarioController
from src.repository.conta import ContaRepository
from src.repository.transacoes import TransacoesRepository


app = Flask(__name__, template_folder='src/views/templates')
app.secret_key = 'chave_secreta'

usuario_repo = UsuarioRepository()
usuario_controller = UsuarioController()
conta_repo = ContaRepository()
conta_controller = ContaController()
transacao_repo = TransacoesRepository()

def logado():
    return 'usuario_id' in session

def e_admin():
    return session.get('papel') == 'admin'

@app.route('/')
def index():
    if 'usuario_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        usuario = usuario_controller.autenticar_usuario(email, senha)
        
        if usuario:
            session['usuario_id'] = str(usuario[0])
            session['nome'] = usuario[1]
            session['papel'] = 'admin' if usuario[6] == True else 'user'
            
            flash("Login realizado com sucesso!", "success")
            return redirect(url_for('dashboard'))
        
        flash("E-mail ou senha incorretos.", "danger")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form.get('nome')
        cpf = request.form.get('cpf')
        data_nascimento = request.form.get('data_nascimento')
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        tipo_pessoa = request.form.get('tipo_pessoa')
        tipo_conta = request.form.get('tipo_conta')

        try:
            usuario_id = usuario_controller.registrar_usuario(
                nome, 
                cpf, 
                data_nascimento, 
                email, 
                senha,
                tipo_pessoa
                )
            
            conta_controller.criar_conta_automatica(usuario_id, tipo_pessoa, tipo_conta)
            
            flash("Cadastro realizado com sucesso! Bem-vindo ao NexBank. Faça login para acessar sua conta.", "success")
            return redirect(url_for('login'))
        
        except ValueError as e:
            flash(str(e), "danger")
        
        except Exception as e:
            flash("Erro ao criar conta. Verifique se este E-mail ou CPF já estão cadastrados.", "danger")
            print(f"Erro BD: {e}")

    return render_template('cadastro.html')

@app.route('/dashboard')
def dashboard():
    if not logado():
        return redirect(url_for('login'))
    conta = conta_repo.buscar_por_usuario(session['usuario_id'])
    return render_template('user_dashboard.html', conta=conta)

@app.route('/extrato')
def extrato():
    if not logado():
        return redirect(url_for('login'))
    
    conta = conta_repo.buscar_por_usuario(session['usuario_id'])
    
    if not conta:
        flash("Conta bancária não encontrada.", "danger")
        return redirect(url_for('dashboard'))

    transacoes = transacao_repo.buscar_por_conta(conta[0])
    return render_template('extrato.html', conta=conta, transacoes=transacoes)

@app.route('/comprovante/<transacao_id>')
def visualizar_comprovante_historico(transacao_id):
    print(f"Buscando o comprovante número: {transacao_id}")
    if not logado():
        return redirect(url_for('login'))
    
    usuario_id = session['usuario_id']

    comprovante = conta_controller.gerar_comprovante_por_id(transacao_id, usuario_id)
    
    if not comprovante:
        flash("Transação não encontrada ou acesso não autorizado.", "danger")
        return redirect(url_for('extrato'))
    
    return render_template('comprovante.html', c=comprovante)

@app.route('/operacoes', methods=['POST'])
def operacoes():
    if not logado():
        return redirect(url_for('login'))

    tipo = request.form.get('tipo')
    valor = request.form.get('valor')
    usuario_id = session['usuario_id']
    
    try:
        if tipo == 'deposito':
            conta_controller.efetuar_deposito(usuario_id, valor)
            flash(f"Depósito de R$ {float(valor):.2f} realizado com sucesso!", "success")
        
        elif tipo == 'saque':
            conta_controller.efetuar_saque(usuario_id, valor)
            flash(f"Saque de R$ {float(valor):.2f} realizado com sucesso!", "success")
    
    except Exception as e:
        flash(str(e), "danger")
    
    return redirect(url_for('dashboard'))


@app.route('/transferir', methods=['POST'])
def transferir():
    if not logado():
        return redirect(url_for('login'))
    
    id_origem = request.form.get('id_origem')
    identificador_destino = request.form.get('identificador_destino')
    metodo = request.form.get('metodo')
    valor = request.form.get('valor')

    try:
        comprovante = conta_controller.transferir(id_origem, identificador_destino, valor, metodo)
        return render_template('comprovante.html', c=comprovante)
    
    except Exception as e:
        flash(str(e), "danger")
    
    return redirect(url_for('dashboard'))

@app.route('/perfil', methods=['GET', 'POST'])
def perfil():
    if not logado():
        return redirect(url_for('login'))
    
    usuario = usuario_repo.buscar_por_id(session['usuario_id'])
    
    if request.method == 'POST':
        flash("Perfil atualizado!", "success")
    return render_template('perfil.html', usuario=usuario)

@app.route('/admin/dashboard')
def admin_dashboard():
    if not e_admin():
        return "Acesso Negado!", 403
    
    metricas = conta_controller.obter_metricas_admin()
    return render_template('admin_dashboard.html', m=metricas)

@app.route('/admin/clientes')
def admin_clientes():
    if not e_admin():
        return "Acesso Negado!", 403
    clientes = usuario_repo.listar_todos()
    return render_template('admin_clientes.html', clientes=clientes)

@app.route('/admin/transacoes')
def admin_transacoes():
    if not e_admin():
        return "Acesso Negado!", 403
    transacoes = transacao_repo.listar_todos()
    return render_template('admin_transacoes.html', transacoes=transacoes)

if __name__ == '__main__':
    app.run(debug=True)