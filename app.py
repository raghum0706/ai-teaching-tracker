from flask import Flask, render_template, request, redirect, session, send_file
import sqlite3, os
from config import SECRET_KEY, DATABASE
from auth.auth_routes import auth_bp
from ai_engine.syllabus_parser import parse_syllabus
from ai_engine.timetable_generator import generate_timetable
from ai_engine.coverage_analyzer import analyze_coverage
from ai_engine.rescheduler import reschedule
from pdf_engine.pdf_creator import create_pdf

app = Flask(__name__)
app.secret_key = SECRET_KEY

# Setup Folders
UPLOADS = ["uploads/syllabus", "uploads/lectures", "uploads/pdfs"]
for folder in UPLOADS: os.makedirs(folder, exist_ok=True)

app.register_blueprint(auth_bp)

def get_db():
    conn = sqlite3.connect(DATABASE)
    return conn, conn.cursor()

@app.route("/")
def index():
    return redirect("/dashboard")

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session: return redirect("/login")
    
    if session["role"] == "teacher":
        return render_template("teacher_dashboard.html")
    else:
        return render_template("student_dashboard.html")

@app.route("/upload_syllabus", methods=["GET", "POST"])
def upload_syllabus():
    if session.get("role") != "teacher": return redirect("/")
    
    if request.method == "POST":
        file = request.files["syllabus"]
        path = "uploads/syllabus/syllabus.txt"
        file.save(path)

        topics = parse_syllabus(path)
        timetable = generate_timetable(topics)

        conn, cur = get_db()
        teacher_id = session["user_id"]

        for t in topics: cur.execute("INSERT INTO syllabus (teacher_id, topic) VALUES (?,?)", (teacher_id, t))
        for day, tpcs in timetable.items():
            for t in tpcs: cur.execute("INSERT INTO timetable (teacher_id, day, topic) VALUES (?,?,?)", (teacher_id, day, t))
        
        conn.commit()
        conn.close()

        timetable_text = "\n\n".join([f"Day {d}:\n" + "\n".join(ts) for d, ts in timetable.items()])
        create_pdf("Updated Timetable", timetable_text, "uploads/pdfs/timetable.pdf")

        return render_template("syllabus_result.html", timetable_pdf="timetable.pdf")

    return render_template("upload_syllabus.html")

@app.route("/upload_lecture", methods=["GET", "POST"])
def upload_lecture():
    if session.get("role") != "teacher": return redirect("/")
    
    if request.method == "POST":
        file = request.files["lecture"]
        path = "uploads/lectures/lecture.txt"
        file.save(path)

        conn, cur = get_db()
        teacher_id = session["user_id"]
        
        # Get Current Day
        cur.execute("SELECT MAX(day) FROM lecture_progress WHERE teacher_id=?", (teacher_id,))
        res = cur.fetchone()[0]
        curr_day = res + 1 if res else 1

        cur.execute("SELECT topic FROM timetable WHERE teacher_id=? AND day=?", (teacher_id, curr_day))
        topics = [t[0] for t in cur.fetchall()]

        analysis = analyze_coverage(topics, path)
        
        cur.execute("INSERT INTO lecture_progress (teacher_id, day) VALUES (?,?)", (teacher_id, curr_day))
        reschedule(teacher_id, curr_day, analysis, cur)
        
        conn.commit()
        conn.close()

        return render_template("lecture_result.html", analysis=analysis, day=curr_day)

    return render_template("upload_lecture.html")

@app.route("/download/<filename>")
def download_file(filename):
    return send_file(os.path.join("uploads/pdfs", filename), as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)