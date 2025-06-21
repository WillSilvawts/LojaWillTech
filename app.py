from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            preco REAL NOT NULL
        )
    ''')
    conn.commit()

    cursor = conn.execute('SELECT COUNT(*) FROM produtos')
    if cursor.fetchone()[0] == 0:
        produtos = [
            ("Mouse Gamer RGB", 99.90),
            ("Teclado Mecânico", 249.90),
            ("Monitor 24'' Full HD", 899.00),
            ("Headset Gamer", 199.90),
            ("Webcam Full HD", 149.90),
            ("Cadeira Gamer", 1299.00),
            ("Notebook i5 8GB", 2899.00),
            ("HD Externo 1TB", 399.90),
            ("SSD 480GB", 249.90),
            ("Placa de Vídeo RTX 3060", 2499.00),
            ("Fonte 650W", 449.00),
            ("Gabinete RGB", 599.00),
            ("Roteador Dual Band", 199.00),
            ("Microfone USB", 299.90),
            ("Carregador Portátil", 129.90)
        ]
        conn.executemany('INSERT INTO produtos (nome, preco) VALUES (?, ?)', produtos)
        conn.commit()

    conn.close()

init_db()

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    produtos = conn.execute('SELECT * FROM produtos').fetchall()
    conn.close()
    return render_template('index.html', produtos=produtos)

@app.route('/add', methods=('GET', 'POST'))
def add():
    if request.method == 'POST':
        nome = request.form['nome']
        preco = request.form['preco']
        conn = get_db_connection()
        conn.execute('INSERT INTO produtos (nome, preco) VALUES (?, ?)', (nome, preco))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('add_product.html')

@app.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit(id):
    conn = get_db_connection()
    produto = conn.execute('SELECT * FROM produtos WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        nome = request.form['nome']
        preco = request.form['preco']
        conn.execute('UPDATE produtos SET nome = ?, preco = ? WHERE id = ?', (nome, preco, id))
        conn.commit()
        conn.close()
        return redirect('/')
    conn.close()
    return render_template('edit_product.html', produto=produto)

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM produtos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)