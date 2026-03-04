from flask import Flask, render_template, request, redirect
import json
import os
from datetime import datetime

app = Flask(__name__)

def load_data():
    if os.path.exists("data.json"):
        with open("data.json", "r") as file:
            return json.load(file)
    return {}

def save_data(data):
    with open("data.json", "w") as file:
        json.dump(data, file)

targets = load_data()

@app.route("/", methods=["GET", "POST"])
def home():
    today = datetime.today()

    if request.method == "POST":

        aksi = request.form.get("aksi")

        if aksi == "tambah":
            nama = request.form["nama"]
            total_jam = request.form["total_jam"]
            deadline = request.form["deadline"]

            targets[nama] = {
                "total_jam": int(total_jam),
                "deadline": deadline,
                "jam_terkumpul": 0
            }

            save_data(targets)
            return redirect("/")

        elif aksi == "hitung":
            waktu_luang = float(request.form["waktu_luang"])
            total_kebutuhan = sum(
                targets[n]["total_jam"] - targets[n]["jam_terkumpul"]
                for n in targets
            )

            if waktu_luang > 0:
                hari_dibutuhkan = total_kebutuhan / waktu_luang
                hasil = f"Butuh sekitar {hari_dibutuhkan:.1f} hari"
            else:
                hasil = "Waktu luang tidak valid"

            return render_template(
                "index.html",
                targets=targets,
                total_kebutuhan=total_kebutuhan,
                hasil=hasil
            )

        save_data(targets)
        return redirect("/")

    for nama in targets:
        deadline_date = datetime.strptime(targets[nama]["deadline"], "%Y-%m-%d")
        sisa_hari = (deadline_date - today).days

        total_jam = targets[nama]["total_jam"]
        jam_terkumpul = targets[nama]["jam_terkumpul"]

        if sisa_hari > 0:
            targets[nama]["sisa_hari"] = sisa_hari
            targets[nama]["rekomendasi"] = (total_jam - jam_terkumpul) / sisa_hari

            # Hitung progress sekarang
            progress_sekarang = (jam_terkumpul / total_jam) * 100

            # Progress ideal sederhana (berdasarkan sisa waktu)
            progress_ideal = 100 - ((sisa_hari / (sisa_hari + 1)) * 100)

            if progress_sekarang >= progress_ideal:
                targets[nama]["status"] = "On Track"
            elif progress_sekarang >= progress_ideal - 20:
                targets[nama]["status"] = "Perlu Ditingkatkan"
            else:
                targets[nama]["status"] = "Tertinggal"

        else:
            targets[nama]["sisa_hari"] = 0
            targets[nama]["rekomendasi"] = 0
            targets[nama]["status"] = "Deadline Lewat"

    return render_template("index.html", targets=targets)

@app.route("/hapus/<nama>")
def hapus(nama):
    if nama in targets:
        del targets[nama]
        save_data(targets)
    return redirect("/")

@app.route("/update/<nama>", methods=["POST"])
def update(nama):
    tambah_jam = int(request.form["tambah_jam"])
    if nama in targets:
        targets[nama]["jam_terkumpul"] += tambah_jam
        save_data(targets)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)