from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import hashlib

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'  # Necessário para usar sessões

# Função para inicializar o banco de dados
def init_db():
    conn = sqlite3.connect('clientes.db')
    cursor = conn.cursor()
    # Tabela de clientes
    cursor.execute('''CREATE TABLE IF NOT EXISTS clientes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT NOT NULL,
                        email TEXT NOT NULL,
                        telefone TEXT NOT NULL,
                        empresa_id INTEGER,
                        FOREIGN KEY (empresa_id) REFERENCES empresas(id)
                     )''')
    # Tabela de usuários
    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL UNIQUE,
                        password TEXT NOT NULL
                     )''')
    # Tabela de empresas
    cursor.execute('''CREATE TABLE IF NOT EXISTS empresas (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT NOT NULL
                     )''')
    # Tabela de leads
    cursor.execute('''CREATE TABLE IF NOT EXISTS leads (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT NOT NULL,
                        descricao TEXT,
                        status TEXT NOT NULL
                     )''')
    conn.commit()
    conn.close()

# Atualiza o banco de dados para corrigir inconsistências, se necessário
def update_db():
    conn = sqlite3.connect('clientes.db')
    cursor = conn.cursor()
    try:
        cursor.execute("ALTER TABLE clientes ADD COLUMN empresa_id INTEGER;")
    except sqlite3.OperationalError:
        pass  # A coluna já existe
    conn.commit()
    conn.close()

# Inicializa e atualiza o banco de dados
init_db()
update_db()

# Função para criptografar senhas
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Rota para login e registro
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        action = request.form.get('action')
        username = request.form['username']
        password = hash_password(request.form['password'])

        conn = sqlite3.connect('clientes.db')
        cursor = conn.cursor()

        if action == 'register':
            # Registro de novo usuário
            try:
                cursor.execute("INSERT INTO usuarios (username, password) VALUES (?, ?)", (username, password))
                conn.commit()
                return render_template('login.html', success_message="Usuário registrado com sucesso! Faça login.")
            except sqlite3.IntegrityError:
                return render_template('login.html', error_message="Nome de usuário já existe.")
        elif action == 'login':
            # Login de usuário existente
            cursor.execute("SELECT * FROM usuarios WHERE username = ? AND password = ?", (username, password))
            user = cursor.fetchone()
            conn.close()
            if user:
                session['user'] = username
                return redirect(url_for('dashboard'))
            else:
                return render_template('login.html', error_message="Credenciais inválidas.")
        conn.close()

    return render_template('login.html')

# Rota para logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

# Rota principal redirecionando para login
@app.route('/')
def home():
    return redirect(url_for('login'))

# Rota do dashboard
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect('clientes.db')
    cursor = conn.cursor()
    cursor.execute("SELECT c.id, c.nome, c.email, c.telefone, c.empresa_id, e.nome FROM clientes c LEFT JOIN empresas e ON c.empresa_id = e.id")
    contatos = cursor.fetchall()
    cursor.execute("SELECT id, nome FROM empresas")
    empresas = cursor.fetchall()
    cursor.execute("SELECT * FROM leads")
    leads = cursor.fetchall()
    conn.close()
    return render_template('index.html', contatos=contatos, empresas=empresas, leads=leads)

# Adicionar contato
@app.route('/add_contact', methods=['POST'])
def add_contact():
    if 'user' not in session:
        return redirect(url_for('login'))

    nome = request.form['nome']
    email = request.form['email']
    telefone = request.form['telefone']
    empresa_id = request.form['empresa_id']

    conn = sqlite3.connect('clientes.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO clientes (nome, email, telefone, empresa_id) VALUES (?, ?, ?, ?)", (nome, email, telefone, empresa_id))
    conn.commit()
    conn.close()

    return redirect(url_for('dashboard'))

# Adicionar empresa
@app.route('/add_company', methods=['POST'])
def add_company():
    if 'user' not in session:
        return redirect(url_for('login'))

    nome_empresa = request.form['nome']

    conn = sqlite3.connect('clientes.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO empresas (nome) VALUES (?)", (nome_empresa,))
    conn.commit()
    conn.close()

    return redirect(url_for('dashboard'))

# Adicionar lead
@app.route('/add_lead', methods=['POST'])
def add_lead():
    if 'user' not in session:
        return redirect(url_for('login'))

    nome = request.form['nome']
    descricao = request.form['descricao']
    status = request.form['status']

    conn = sqlite3.connect('clientes.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO leads (nome, descricao, status) VALUES (?, ?, ?)", (nome, descricao, status))
    conn.commit()
    conn.close()

    return redirect(url_for('dashboard'))

# Excluir lead
@app.route('/delete_lead/<int:id>', methods=['POST'])
def delete_lead(id):
    if 'user' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect('clientes.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM leads WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return redirect(url_for('dashboard'))

# Atualizar status do lead
@app.route('/update_lead_status/<int:lead_id>/<string:status>', methods=['POST'])
def update_lead_status(lead_id, status):
    if 'user' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect('clientes.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE leads SET status = ? WHERE id = ?", (status, lead_id))
    conn.commit()
    conn.close()

    return '', 204  # Retorna HTTP 204 No Content

if __name__ == '__main__':
    app.run(debug=True)
