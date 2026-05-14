from flask import Flask, render_template, request, redirect, url_for, flash, session
from src.controllers.conta_controller import ContaController, TransferenciaPix, TransferenciaTED
from src.repository.usuario import UsuarioRepository
from src.repository.conta import ContaRepository
from src.repository.transacoes import TransacoesRepository


app = Flask(__name__)
app.secret_key = 'chave_secreta'

usuario_repo = UsuarioRepository()
conta_repo = ContaRepository()
transacao_repo = TransacoesRepository()
conta_controller = ContaController()

def logado():
    return 'usuario_id' in session

def e_admin():
    return session.get('papel') == 'admin'

@app.route('/')
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        usuario = usuario_repo.buscar_por_email(email)
        
        if usuario and usuario.senha_hash == senha:
            session['usuario_id'] = usuario.id
            session['nome'] = usuario.nome
            session['papel'] = usuario.papel
            return redirect(url_for('dashboard'))
        flash("E-mail ou senha incorretos.")
    return render_template('login.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        pass
    return render_template('cadastro.html')

@app.route('/dashboard')
def dashboard():
    if not logado():
        return redirect(url_for('login'))
    conta = conta_repo.buscar_por_usuario(session['usuario_id'])
    return render_template('user_dashboard.html', conta=conta)

@app.route('/perfil', methods=['GET', 'POST'])
def perfil():
    if not logado():
        return redirect(url_for('login'))
    usuario = conta_repo.buscar_por_usuario(session['usuario_id'])
    if request.method == 'POST':
        flash("Perfil atualizado!", "success")
    return render_template('perfil.html', usuario=usuario)

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