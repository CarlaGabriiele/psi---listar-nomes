from flask import Flask, render_template, url_for, request, redirect
import sqlite3

app = Flask(__name__)

def obter_conexao():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('pages/index.html')

@app.route('/create', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        nome = request.form['nome']
        conn = obter_conexao()
        conn.execute("INSERT INTO usuarios(nome) VALUES(?)", (nome,))
        conn.commit()
        conn.close()
        return redirect(url_for('listar'))
    return render_template('pages/create-user.html')

@app.route('/listar')
def listar():
    conn = obter_conexao()
    users = conn.execute("SELECT * FROM usuarios").fetchall()
    conn.close()
    return render_template('pages/listar-users.html', users=users)

@app.route('/delete/<int:id>')
def delete_user(id):
    conn = obter_conexao()
    conn.execute("DELETE FROM usuarios WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('listar'))

if __name__ == '__main__':
    app.run(debug=True)
