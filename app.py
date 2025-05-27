from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DB_NAME = 'database.db'

# Buat tabel kalau belum ada
def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)')
init_db()

@app.route('/')
def index():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.execute('SELECT * FROM items')
        items = [{'id': row[0], 'name': row[1]} for row in cursor.fetchall()]
    return render_template('index.html', items=items)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        with sqlite3.connect(DB_NAME) as conn:
            conn.execute('INSERT INTO items (name) VALUES (?)', (name,))
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:item_id>', methods=['GET', 'POST'])
def edit(item_id):
    if request.method == 'POST':
        new_name = request.form['name']
        with sqlite3.connect(DB_NAME) as conn:
            conn.execute('UPDATE items SET name = ? WHERE id = ?', (new_name, item_id))
        return redirect(url_for('index'))
    else:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.execute('SELECT * FROM items WHERE id = ?', (item_id,))
            row = cursor.fetchone()
            item = {'id': row[0], 'name': row[1]}
        return render_template('edit.html', item=item)

@app.route('/delete/<int:item_id>')
def delete(item_id):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('DELETE FROM items WHERE id = ?', (item_id,))
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
