def tambah_target(targets):
    print("\n=== Tambah Target ===")
    nama = input("Nama target: ")

    if nama in targets:
        print("Target sudah ada!")
        return

    try:
        total_jam = int(input("Total jam yang dibutuhkan: "))
        deadline = int(input("Deadline (dalam hari): "))
    except ValueError:
        print("Input harus berupa angka!")
        return

    targets[nama] = {"total_jam": total_jam, "deadline": deadline}

    print(f"Target '{nama}' berhasil ditambahkan!")


def lihat_target(targets):
    print("\n=== Daftar Target ===")

    if not targets:
        print("Belum ada target.")
        return

    for nama, data in targets.items():
        print(f"- {nama} | {data['total_jam']} jam | {data['deadline']} hari")


def hitung_rencana(targets):
    print("\n=== Hitung Rencana Belajar ===")

    if not targets:
        print("Belum ada target.")
        return

    try:
        waktu_luang = float(input("Waktu luang per hari (jam): "))
    except ValueError:
        print("Input harus angka!")
        return

    total_kebutuhan = 0

    for nama, data in targets.items():
        jam_per_hari = data["total_jam"] / data["deadline"]
        total_kebutuhan += jam_per_hari
        print(f"{nama}: {jam_per_hari:.2f} jam/hari")

    print(f"\nTotal kebutuhan: {total_kebutuhan:.2f} jam/hari")

    if total_kebutuhan <= waktu_luang:
        print("✅ Jadwal realistis!")
    else:
        print("⚠️ Jadwal terlalu padat!")


def hapus_target(targets):
    print("\n=== Hapus Target ===")
    nama = input("Nama target yang ingin dihapus: ")

    if nama in targets:
        del targets[nama]
        print("Target berhasil dihapus.")
    else:
        print("Target tidak ditemukan.")


def menu():
    print("\n==== SMART STUDY PLANNER ====")
    print("1. Tambah Target")
    print("2. Lihat Target")
    print("3. Hitung Rencana")
    print("4. Hapus Target")
    print("5. Keluar")


def main():
    targets = {}

    while True:
        menu()
        pilihan = input("Pilih menu (1-5): ")

        if pilihan == "1":
            tambah_target(targets)
        elif pilihan == "2":
            lihat_target(targets)
        elif pilihan == "3":
            hitung_rencana(targets)
        elif pilihan == "4":
            hapus_target(targets)
        elif pilihan == "5":
            print("Terima kasih sudah menggunakan Smart Study Planner!")
            break
        else:
            print("Pilihan tidak valid!")


if __name__ == "__main__":
    main()