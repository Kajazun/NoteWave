from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import sqlite3
from datetime import datetime
from werkzeug.security import check_password_hash,generate_password_hash





app = Flask(__name__)
app.secret_key = 'your_secret_key_here'


DATABASE = 'notes.db'

# Function to get a database connection
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with app.app_context():
        conn = get_db_connection()
        try:

            conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL
                );
            ''')


            conn.execute('''
                CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    content TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                );
            ''')
            conn.commit()
            print("Տվյալների բազան հաջողությամբ ստեղծված է:")
            print("- users աղյուսակ")
            print("- notes աղյուսակ")
        except sqlite3.Error as e:
            print("Սխալ տվյալների բազան ստեղծելիս:", e)
        finally:
            conn.close()

init_db()

notes = []

sign_in = []
users = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login_suc')
def login_suc():
    return render_template('login_suc.html')
@app.route('/signout')
def signout():
    global users
    users = []
    print(users, 'signout')
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        conn = get_db_connection()
        user = conn.execute('SELECT id, email, password FROM users WHERE email = ?', (email,)).fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password):  # Համեմատում ենք թաքնագրված գաղտնաբառը
            session['user_id'] = user['id']  # Պահպանում ենք session-ում
            flash('Մուտքը հաջողվեց!', 'success')
            return redirect(url_for('voice'))  # Հաջող մուտք գործելու դեպքում տանում է voice էջ

        flash('Սխալ էլ․ հասցե կամ գաղտնաբառ։', 'danger')

    return render_template('login.html')  # Եթե POST չէ, ուղղակի ցուցադրում ենք login էջը


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm-password')
        conn = get_db_connection()
        email1 = conn.execute('SELECT email FROM users')

        for i in email1:

                users.append(i)

        for i in range(len(users)):
            users[i] = list(users[i])

        print(users, 'users')
        if [email] in users:
            print('yes')
            return redirect(url_for('login'))
        else:
            if confirm_password == password:
                hashed_password = generate_password_hash(password)  # Hash ենք անում գաղտնաբառը

                print('start else')
                conn = get_db_connection()
                conn.execute(
                    'INSERT INTO users (email, password) VALUES (?, ?)',
                    (email, hashed_password))
                conn.commit()
                conn.close()
                print('end')
            else:
                return render_template('signin.html')

        # print(sign_in, len(sign_in[1]['notes']))

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('signin.html')


@app.route('/voice', methods=['GET', 'POST'])
def voice():
    if 'user_id' not in session:  # Ստուգում ենք, արդյոք օգտատերը մուտք է գործել
        return redirect(url_for('login'))

    user_id = session['user_id']

    if request.method == 'POST':
        note_content = request.form.get('note')
        if note_content:
            with sqlite3.connect('notes.db') as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO notes (user_id, content, created_at) VALUES (?, ?, CURRENT_TIMESTAMP)',
                               (user_id, note_content))
                conn.commit()

    with sqlite3.connect('notes.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, content, created_at FROM notes WHERE user_id = ? ORDER BY created_at DESC',
                       (user_id,))
        notes = cursor.fetchall()

    formatted_notes = []
    for id, note, created_at in notes:
        if isinstance(created_at, str):
            created_at = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
        formatted_date = created_at.strftime("%Y-%m-%d %H:%M:%S")
        formatted_notes.append((id, note, formatted_date))

    return render_template('notes.html', notes=formatted_notes)


@app.route('/edit-note/<int:note_id>', methods=['POST'])
def edit_note(note_id):
    user_id = session['user_id']
    new_content = request.json.get('content')

    with sqlite3.connect('notes.db') as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE notes SET content = ?  WHERE id = ? AND user_id = ?', (new_content, note_id, user_id))
        conn.commit()

    return jsonify({"success": True})


@app.route('/delete-note/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    user_id = session['user_id']

    with sqlite3.connect('notes.db') as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM notes WHERE id = ? AND user_id = ?', (note_id, user_id))
        conn.commit()

    return jsonify({"success": True})

# if __name__ == '__main__':
#     app.run(debug=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)