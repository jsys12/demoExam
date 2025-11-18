from fastapi import FastAPI, Form
from fastapi.responses import FileResponse
import sqlite3

app = FastAPI()

ADMIN_LOGIN = "admin"
ADMIN_PASSWORD = "12345"

def init_db():
    con = sqlite3.connect('data.db')
    cur = con.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, email TEXT, password TEXT, pasport TEXT)
    ''')
    cur.execute('''
    CREATE TABLE IF NOT EXISTS bookings (id INTEGER PRIMARY KEY, home_address TEXT, user_id TEXT, start_date TEXT, quantity_days TEXT, status TEXT)
    ''')
    con.commit()
    con.close()

@app.get("/")
def index():
    return FileResponse("templates/index.html")

@app.get("/index")
def index():
    return FileResponse("templates/index.html")

@app.get("/auth")
def index():
    return FileResponse("templates/auth.html")

@app.get("/admin")
def index():
    return FileResponse("templates/admin.html")

@app.get("/bookings")
def index():
    return FileResponse("templates/bookings.html")

@app.get("/create_booking")
def index():
    return FileResponse("templates/create_booking.html")

@app.get("/reg")
def index():
    return FileResponse("templates/reg.html")

@app.post("/register")
def register(username: str = Form(...), 
            email: str = Form(...),
            password: str = Form(...),
            pasport: str = Form(...)
            ):
    con = sqlite3.connect('data.db')
    cur = con.cursor()
    cur.execute('''
    INSERT INTO users (username, email, password, pasport) VALUES (?, ?, ?, ?)
    ''', (username, email, password, pasport))
    con.commit()
    con.close()
    return{"message": "Fine"}

@app.post("/auth")
def auth( 
            email: str = Form(...),
            password: str = Form(...)
            ):
    con = sqlite3.connect('data.db')
    cur = con.cursor()
    cur.execute('''
    SELECT * FROM users WHERE email = ? and password = ?
    ''', (email, password))
    res = cur.fetchone()
    con.close()
    if res == None:
        return {"message": "Password or email incorrect"}
    return{"message": "Fine", "email": email, "id": res[0]}

@app.post("/create_booking")
def create_booking(adres: str = Form(...), start_date: str = Form(...), quantity_days: str = Form(...), user_id: str = Form(...)):
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    cur.execute('''
        INSERT INTO bookings (home_address, user_id, start_date, quantity_days, status) VALUES (?, ?, ?, ?, ?)
''', (adres, user_id, start_date, quantity_days, "новая"))
    con.commit()
    con.close()
    return{"message": "Fine"}

@app.get("/bookings_view")
def create_booking(user_id: str):
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    cur.execute('''
        SELECT * FROM bookings WHERE user_id = ?
''', (user_id))
    res = cur.fetchall()
    return{"message": "Fine", "result": res}

@app.get("/bookings_all")
def bookings_all():
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    cur.execute('''
        SELECT * FROM bookings
''')
    res = cur.fetchall()
    return{"message": "Fine", "result": res}

@app.post("/auth_admin")
def auth_admin( 
            login: str = Form(...),
            password: str = Form(...)
            ):
    if login == ADMIN_LOGIN and password == ADMIN_PASSWORD:
        return {"message": "Fine"}
    else:
        return {"message": "Password or login incorrect"}
    
@app.get("/change_status")
def change_status(id, status):
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    cur.execute('''
        UPDATE bookings SET status = ? WHERE id = ?
''', (status, id))
    con.commit()
    return{"message": "Fine"}

init_db()
