from flask import Flask, render_template, redirect, request, url_for
from mysql import connector
from datetime import datetime

app = Flask(__name__)

db = connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = '',
    database = 'db_berita_0547'
)

if db.is_connected():
    print('Database is opened successfully!!!')

@app.route('/')
def mainpage():
    cursor = db.cursor()
    cursor.execute('select * from tbl_berita_0547')
    result = cursor.fetchall()
    cursor.close()
    return render_template('home.html', hasil = result)

@app.route('/admin_dashboard')
def dashboard():
    cursor = db.cursor()
    cursor.execute('select * from tbl_berita_0547')
    result = cursor.fetchall()
    cursor.close()
    return render_template('dashboard.html', hasil = result)

@app.route('/add/')
def add_data():
    return render_template('add.html')

@app.route('/add_in_process/', methods=['post'])
def add_processing():
    date = datetime.now()
    now = date.strftime('%Y-%m-%d')
    title = request.form['title']
    konten = request.form['content']
    auth = request.form['author']
    cursor = db.cursor()
    cursor.execute('INSERT INTO tbl_berita_0547 (date, judul, isi, author) VALUES (%s ,%s, %s, %s)', (now, title, konten, auth))
    db.commit()
    return redirect(url_for('mainpage'))

@app.route('/edit/<judul>', methods=['get'])
def change_data(judul):
    cursor = db.cursor()
    cursor.execute('select * from tbl_berita_0547 where judul=%s', (judul,))
    result = cursor.fetchall()
    cursor.close()
    return render_template('edit.html', hasil = result)

@app.route('/edit_in_process/', methods=['post'])
def change_processing():
    date = datetime.now()
    now = date.strftime('%Y-%m-%d')
    title_ori = request.form['title_ori']
    title = request.form['title_n']
    konten = request.form['content_n']
    cursor = db.cursor()
    sql = 'UPDATE tbl_berita_0547 SET date=%s, judul=%s, isi=%s WHERE judul=%s'
    value = (now, title, konten, title_ori)
    db.commit()
    cursor.execute(sql, value)
    return redirect(url_for('mainpage'))

@app.route('/del/<judul>', methods=['get'])
def del_data(judul):
    cursor =db.cursor()
    cursor.execute("DELETE from tbl_berita_0547 where judul=%s", (judul,))
    db.commit()
    return redirect(url_for('mainpage'))

@app.route('/read/<judul>', methods=['get'])
def read_data(judul):
    cursor = db.cursor()
    cursor.execute('select * from tbl_berita_0547 where judul=%s', (judul,))
    result = cursor.fetchall()
    cursor.close()
    return render_template('read.html', hasil = result)

if __name__ == "__main__":
    app.run()