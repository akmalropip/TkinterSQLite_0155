import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as msg
import sqlite3

DB_NAME = "prediksi_diabetes.db"


# Membuat database dan tabel
def buat_database():
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS pasien (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama_pasien TEXT NOT NULL,
        usia INTEGER NOT NULL,
        gula_darah INTEGER NOT NULL,
        bmi REAL NOT NULL,
        riwayat_ortu TEXT NOT NULL,
        hasil_prediksi TEXT NOT NULL
    )""")

    con.commit()
    con.close()


# Menentukan hasil prediksi
def prediksi_risiko(gula_darah, bmi, riwayat_ortu):
    if gula_darah >= 200:
        if bmi >= 30 and riwayat_ortu == "Ya":
            return "Sangat Tinggi"
        return "Tinggi"

    elif gula_darah >= 140:
        if bmi >= 30 or riwayat_ortu == "Ya":
            return "Tinggi"
        return "Sedang"

    else:
        if bmi >= 30:
            if riwayat_ortu == "Ya":
                return "Sedang"
            return "Waspada"

        elif riwayat_ortu == "Ya":
            return "Waspada"

        return "Rendah"


buat_database()

# Membuat jendela utama
top = tk.Tk()
top.title("Aplikasi Prediksi Risiko Diabetes")
top.geometry("1100x720")
top.minsize(900, 620)
top.configure(bg="#eef2f7")

# Bagian judul
header = tk.Frame(top, bg="#1e293b", padx=20, pady=16)
header.pack(fill="x")

tk.Label(
    header,
    text="APLIKASI PREDIKSI RISIKO DIABETES",
    font=("Arial", 19, "bold"),
    bg="#1e293b",
    fg="white"
).pack(anchor="w")

tk.Label(
    header,
    text="Masukkan data pasien, lalu simpan hasil prediksinya.",
    font=("Arial", 10),
    bg="#1e293b",
    fg="#cbd5e1"
).pack(anchor="w", pady=(4, 0))

# Form input pasien
body = tk.Frame(top, bg="#eef2f7", padx=18, pady=14)
body.pack(fill="both", expand=True)

form_frame = tk.LabelFrame(
    body,
    text=" Data Pasien ",
    font=("Arial", 11, "bold"),
    bg="white",
    fg="#1e293b",
    padx=14,
    pady=12
)
form_frame.pack(fill="x", pady=(0, 12))

tk.Label(
    form_frame, text="Nama Pasien",
    bg="white", font=("Arial", 10)
).grid(row=0, column=0, sticky="w", padx=8, pady=7)

E1 = tk.Entry(form_frame, bd=2, font=("Arial", 10))
E1.grid(row=0, column=1, sticky="ew", padx=8, pady=7, ipady=4)

tk.Label(
    form_frame, text="Usia (tahun)",
    bg="white", font=("Arial", 10)
).grid(row=0, column=2, sticky="w", padx=8, pady=7)

E2 = tk.Entry(form_frame, bd=2, font=("Arial", 10))
E2.grid(row=0, column=3, sticky="ew", padx=8, pady=7, ipady=4)

tk.Label(
    form_frame, text="Gula Darah (mg/dL)",
    bg="white", font=("Arial", 10)
).grid(row=1, column=0, sticky="w", padx=8, pady=7)

E3 = tk.Entry(form_frame, bd=2, font=("Arial", 10))
E3.grid(row=1, column=1, sticky="ew", padx=8, pady=7, ipady=4)

tk.Label(
    form_frame, text="BMI",
    bg="white", font=("Arial", 10)
).grid(row=1, column=2, sticky="w", padx=8, pady=7)

E4 = tk.Entry(form_frame, bd=2, font=("Arial", 10))
E4.grid(row=1, column=3, sticky="ew", padx=8, pady=7, ipady=4)

tk.Label(
    form_frame,
    text="Riwayat Diabetes Orang Tua",
    bg="white",
    font=("Arial", 10)
).grid(row=2, column=0, sticky="w", padx=8, pady=7)

riwayat_var = tk.StringVar(value="")

combo_riwayat = ttk.Combobox(
    form_frame,
    textvariable=riwayat_var,
    values=("Ya", "Tidak"),
    state="readonly",
    font=("Arial", 10),
    width=18
)
combo_riwayat.grid(
    row=2, column=1, sticky="ew", padx=8, pady=7, ipady=3
)

for kolom in (1, 3):
    form_frame.grid_columnconfigure(kolom, weight=1)

# Warna hasil prediksi
warna_risiko = {
    "Sangat Tinggi": "#991b1b",
    "Tinggi": "#ea580c",
    "Sedang": "#d97706",
    "Waspada": "#ca8a04",
    "Rendah": "#15803d"
}

hasil_label = tk.Label(
    form_frame,
    text="Hasil Prediksi akan muncul di sini",
    font=("Arial", 11, "bold"),
    bg="#e2e8f0",
    fg="#334155",
    padx=10,
    pady=10
)
hasil_label.grid(
    row=3, column=0, columnspan=4,
    sticky="ew", padx=8, pady=(8, 4)
)

# Tabel riwayat pasien
riwayat_frame = tk.LabelFrame(
    body,
    text=" Riwayat Pasien Tersimpan ",
    font=("Arial", 11, "bold"),
    bg="white",
    fg="#1e293b",
    padx=10,
    pady=10
)
riwayat_frame.pack(fill="both", expand=True)

style = ttk.Style()
style.configure("Treeview", rowheight=25, font=("Arial", 9))
style.configure(
    "Treeview.Heading",
    font=("Arial", 9, "bold")
)

kolom_tabel = (
    "id", "nama_pasien", "usia", "gula_darah",
    "bmi", "riwayat_ortu", "hasil_prediksi"
)

tabel = ttk.Treeview(
    riwayat_frame,
    columns=kolom_tabel,
    show="headings",
    height=9
)

tabel.heading("id", text="ID")
tabel.heading("nama_pasien", text="Nama Pasien")
tabel.heading("usia", text="Usia")
tabel.heading("gula_darah", text="Gula Darah")
tabel.heading("bmi", text="BMI")
tabel.heading("riwayat_ortu", text="Riwayat Orang Tua")
tabel.heading("hasil_prediksi", text="Hasil Prediksi")

tabel.column("id", width=45, anchor="center")
tabel.column("nama_pasien", width=170, anchor="w")
tabel.column("usia", width=65, anchor="center")
tabel.column("gula_darah", width=105, anchor="center")
tabel.column("bmi", width=70, anchor="center")
tabel.column("riwayat_ortu", width=135, anchor="center")
tabel.column("hasil_prediksi", width=130, anchor="center")

tabel.grid(row=0, column=0, sticky="nsew")

scrollbar = ttk.Scrollbar(
    riwayat_frame,
    orient="vertical",
    command=tabel.yview
)
scrollbar.grid(row=0, column=1, sticky="ns")
tabel.configure(yscrollcommand=scrollbar.set)

riwayat_frame.grid_rowconfigure(0, weight=1)
riwayat_frame.grid_columnconfigure(0, weight=1)


# Menampilkan semua data dari database
def lihat_data():
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()

    cur.execute("""SELECT id, nama_pasien, usia, gula_darah, bmi,
                   riwayat_ortu, hasil_prediksi
                   FROM pasien ORDER BY id DESC""")

    data_pasien = cur.fetchall()
    con.close()

    tabel.delete(*tabel.get_children())

    for data in data_pasien:
        tabel.insert("", tk.END, values=data)


# Mengosongkan form
def kosongkan_form():
    E1.delete(0, tk.END)
    E2.delete(0, tk.END)
    E3.delete(0, tk.END)
    E4.delete(0, tk.END)
    combo_riwayat.set("")

    hasil_label.config(
        text="Hasil Prediksi akan muncul di sini",
        bg="#e2e8f0",
        fg="#334155"
    )

    E1.focus_set()


# Validasi, prediksi, dan simpan data
def simpan_data():
    nama = E1.get().strip()
    usia_text = E2.get().strip()
    gula_text = E3.get().strip()
    bmi_text = E4.get().strip()
    riwayat = riwayat_var.get()

    if not nama or not usia_text or not gula_text or not bmi_text or not riwayat:
        msg.showwarning(
            "Input Belum Lengkap",
            "Semua data harus diisi terlebih dahulu."
        )
        return

    if not usia_text.isdigit():
        msg.showwarning(
            "Input Tidak Valid",
            "Usia harus berupa angka bulat."
        )
        return

    if not gula_text.isdigit():
        msg.showwarning(
            "Input Tidak Valid",
            "Gula darah harus berupa angka bulat."
        )
        return

    usia = int(usia_text)
    gula_darah = int(gula_text)

    try:
        bmi = float(bmi_text)
    except ValueError:
        msg.showwarning(
            "Input Tidak Valid",
            "BMI harus berupa angka, misalnya 24.5."
        )
        return

    if usia <= 0 or gula_darah <= 0 or bmi <= 0:
        msg.showwarning(
            "Input Tidak Valid",
            "Usia, gula darah, dan BMI harus lebih dari 0."
        )
        return

    hasil = prediksi_risiko(gula_darah, bmi, riwayat)
    warna = warna_risiko[hasil]

    hasil_label.config(
        text="Hasil Prediksi: " + hasil,
        bg=warna,
        fg="white"
    )

    con = sqlite3.connect(DB_NAME)

    try:
        cur = con.cursor()

        cur.execute("""INSERT INTO pasien
            (nama_pasien, usia, gula_darah, bmi,
             riwayat_ortu, hasil_prediksi)
            VALUES (?, ?, ?, ?, ?, ?)""",
            (nama, usia, gula_darah, bmi, riwayat, hasil)
        )

        con.commit()

        msg.showinfo(
            "Berhasil",
            "Data pasien berhasil diprediksi dan disimpan."
        )

    except sqlite3.Error as e:
        msg.showerror(
            "Kesalahan Database",
            "Data gagal disimpan.\n" + str(e)
        )
        return

    finally:
        con.close()

    lihat_data()


# Tombol aplikasi
button_frame = tk.Frame(form_frame, bg="white")
button_frame.grid(
    row=4, column=0, columnspan=4, pady=(6, 0)
)

tk.Button(
    button_frame,
    text="Simpan & Prediksi",
    command=simpan_data,
    bg="#2563eb",
    fg="white",
    activebackground="#1d4ed8",
    activeforeground="white",
    font=("Arial", 10, "bold"),
    padx=14,
    pady=7,
    bd=0
).pack(side="left", padx=5)

tk.Button(
    button_frame,
    text="Lihat Data",
    command=lihat_data,
    bg="#0f766e",
    fg="white",
    activebackground="#115e59",
    activeforeground="white",
    font=("Arial", 10, "bold"),
    padx=14,
    pady=7,
    bd=0
).pack(side="left", padx=5)

tk.Button(
    button_frame,
    text="Kosongkan Form",
    command=kosongkan_form,
    bg="#64748b",
    fg="white",
    activebackground="#475569",
    activeforeground="white",
    font=("Arial", 10, "bold"),
    padx=14,
    pady=7,
    bd=0
).pack(side="left", padx=5)

# Tampilkan data yang sudah tersimpan
lihat_data()
E1.focus_set()

top.mainloop()