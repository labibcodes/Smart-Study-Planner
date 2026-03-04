from flask import Flask, render_template, request, redirect
import json
import os
from datetime import datetime

app = Flask(__name__)

# =========================
# Data Persistence
# =========================

def load_data():
    if os.path.exists("data.json"):
        with open("data.json", "r") as file:
            return json.load(file)
    return {}

def save_data(data):
    with open("data.json", "w") as file:
        json.dump(data, file)

targets = load_data()

# =========================
# Main Route
# =========================

@app.route("/", methods=["GET", "POST"])
def home():
    today = datetime.today()
    total_kebutuhan = 0
    hasil = None

    if request.method == "POST":

        aksi = request.form.get("aksi")

        # ---------- Tambah Target ----------
        if aksi == "tambah":
            nama = request.form["nama"]
            total_jam = int(request.form["total_jam"])
            deadline = request.form["deadline"]

            targets[nama] = {
                "total_jam": total_jam,
                "deadline": deadline,
                "jam_terkumpul": 0
            }

            save_data(targets)
            return redirect("/")

        # ---------- Hitung Rencana ----------
        elif aksi == "hitung":
            waktu_luang = float(request.form["waktu_luang"])

            total_kebutuhan = sum(
                max(targets[n]["total_jam"] - targets[n]["jam_terkumpul"], 0)
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

    # =========================
    # Smart Calculation
    # =========================

    for nama in targets:
        try:
            deadline_date = datetime.strptime(
                targets[nama]["deadline"],
                "%Y-%m-%d"
            )
        except:
            continue

        sisa_hari = (deadline_date - today).days

        total_jam = targets[nama]["total_jam"]
        jam_terkumpul = targets[nama]["jam_terkumpul"]

        if sisa_hari > 0 and total_jam > 0:

            targets[nama]["sisa_hari"] = sisa_hari

            remaining = max(total_jam - jam_terkumpul, 0)
            targets[nama]["rekomendasi"] = round(remaining / sisa_hari, 1)

            # Progress
            progress_sekarang = (jam_terkumpul / total_jam) * 100
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

    return render_template("index.html", targets=targets, total_kebutuhan=total_kebutuhan, hasil=hasil)


# =========================
# Delete Target
# =========================

@app.route("/hapus/<nama>")
def hapus(nama):
    if nama in targets:
        del targets[nama]
        save_data(targets)
    return redirect("/")


# =========================
# Update Progress
# =========================

@app.route("/update/<nama>", methods=["POST"])
def update(nama):
    tambah_jam = int(request.form["tambah_jam"])

    if nama in targets:
        targets[nama]["jam_terkumpul"] += tambah_jam
        save_data(targets)

    return redirect("/")


# =========================
# Run App (Dev Only)
# =========================

if __name__ == "__main__":
    app.run()