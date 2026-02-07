from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

def conectar():
    return sqlite3.connect("zona.db")

@app.route("/videos")
def index():
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT * FROM videos ORDER BY id DESC")
    videos = cur.fetchall()
    con.close()
    return render_template("index.html", videos=videos)

@app.route("/video/<id>")
def video(id):
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT * FROM videos WHERE id=?", (id,))
    video = cur.fetchone()
    con.close()
    return render_template("video.html", video=video)

@app.route("/admin", methods=["GET","POST"])
def admin():
    if request.method == "POST":
        titulo = request.form["titulo"]
        link = request.form["link"]
        categoria = request.form["categoria"]
        descripcion = request.form["descripcion"]

        con = conectar()
        cur = con.cursor()
        cur.execute("""
            INSERT INTO videos (titulo, link, categoria, descripcion)
            VALUES (?,?,?,?)
        """, (titulo, link, categoria, descripcion))
        con.commit()
        con.close()

        return redirect("/")

    return render_template("admin.html")

@app.route("/comentar/<id>", methods=["POST"])
def comentar(id):
    texto = request.form["texto"]

    con = conectar()
    cur = con.cursor()
    cur.execute("INSERT INTO comentarios (video_id, texto) VALUES (?,?)", (id, texto))
    con.commit()
    con.close()

    return redirect("/video/" + id)

if __name__ == "__main__":
    app.run(debug=True)
