from datetime import datetime


class Buku:
    """Class untuk merepresentasikan data buku di perpustakaan."""

    nama_perpustakaan = "Perpustakaan Universitas Bina Bangsa"
    total_judul_buku = 0

    def __init__(self, kode_buku: str, judul: str, penulis: str, stok: int):
        self.kode_buku = kode_buku
        self.judul = judul
        self.penulis = penulis
        self.__stok = 0  # Encapsulation (private attribute)
        self.stok = stok  # Menggunakan setter untuk validasi awal
        Buku.total_judul_buku += 1

    @property
    def stok(self) -> int:
        """Property getter untuk mengakses atribut private __stok."""
        return self.__stok

    @stok.setter
    def stok(self, nilai: int):
        """Property setter dengan validasi agar stok tidak negatif."""
        if nilai < 0:
            raise ValueError("Stok buku tidak boleh kurang dari 0!")
        self.__stok = nilai

    def info_buku(self) -> str:
        """Instance method untuk menampilkan informasi buku."""
        return (
            f"[{self.kode_buku}] {self.judul} - {self.penulis} "
            f"(Stok tersedia: {self.stok})"
        )

    @classmethod
    def info_perpustakaan(cls) -> str:
        """Class method untuk menampilkan ringkasan koleksi perpustakaan."""
        return (
            f"{cls.nama_perpustakaan} | "
            f"Total judul buku terdaftar: {cls.total_judul_buku}"
        )

    @staticmethod
    def validasi_kode_buku(kode: str) -> bool:
        """Static method untuk memvalidasi format kode buku (contoh: BK-001)."""
        bagian = kode.split("-")
        return (
            len(bagian) == 2
            and bagian[0] == "BK"
            and len(bagian[1]) == 3
            and bagian[1].isdigit()
        )


class Anggota:
    """Class untuk merepresentasikan anggota perpustakaan dan transaksi pinjam."""

    denda_per_hari = 2000

    def __init__(self, nim: str, nama: str, prodi: str):
        self.nim = nim
        self.nama = nama
        self.prodi = prodi
        self.__daftar_pinjaman = []  # Encapsulation (private attribute)

    @property
    def daftar_pinjaman(self) -> list:
        """Property getter untuk melihat daftar buku yang sedang dipinjam."""
        return list(self.__daftar_pinjaman)

    @daftar_pinjaman.setter
    def daftar_pinjaman(self, daftar_baru: list):
        """Property setter untuk mengatur daftar pinjaman (maksimal 3 buku)."""
        if len(daftar_baru) > 3:
            raise ValueError("Maksimal peminjaman adalah 3 buku per anggota!")
        self.__daftar_pinjaman = list(daftar_baru)

    def pinjam_buku(self, buku: Buku):
        """Instance method untuk meminjam buku dari perpustakaan."""
        if len(self.__daftar_pinjaman) >= 3:
            print(f"Gagal: {self.nama} sudah mencapai batas maksimal pinjaman.")
            return
        if buku.stok <= 0:
            print(f"Gagal: Stok buku '{buku.judul}' sedang habis.")
            return

        buku.stok -= 1
        self.__daftar_pinjaman.append(buku.judul)
        print(f"Berhasil: {self.nama} meminjam '{buku.judul}'.")

    def kembalikan_buku(self, buku: Buku):
        """Instance method untuk mengembalikan buku ke perpustakaan."""
        if buku.judul not in self.__daftar_pinjaman:
            print(f"Gagal: {self.nama} tidak sedang meminjam '{buku.judul}'.")
            return

        buku.stok += 1
        self.__daftar_pinjaman.remove(buku.judul)
        print(f"Berhasil: {self.nama} mengembalikan '{buku.judul}'.")

    def info_anggota(self) -> str:
        """Instance method untuk menampilkan profil dan status pinjaman anggota."""
        pinjaman = ", ".join(self.__daftar_pinjaman) if self.__daftar_pinjaman else "Tidak ada"
        return f"NIM: {self.nim} | Nama: {self.nama} ({self.prodi}) | Pinjaman: {pinjaman}"

    @classmethod
    def ubah_tarif_denda(cls, tarif_baru: int):
        """Class method untuk memperbarui tarif denda keterlambatan."""
        if tarif_baru >= 0:
            cls.denda_per_hari = tarif_baru

    @staticmethod
    def hitung_denda(hari_terlambat: int) -> int:
        """Static method untuk menghitung total denda keterlambatan."""
        if hari_terlambat <= 0:
            return 0
        return hari_terlambat * Anggota.denda_per_hari


if __name__ == "__main__":
    print("=== SISTEM PERPUSTAKAAN (UTS PBO - PYTHON) ===")
    print(f"Waktu Eksekusi: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}\\n")

    # 1. Demonstrasi Static Method validasi kode buku
    print("Validasi Kode 'BK-001':", Buku.validasi_kode_buku("BK-001"))
    print("Validasi Kode 'B-12'  :", Buku.validasi_kode_buku("B-12"))
    print()

    # 2. Pembuatan Object dari class Buku
    buku1 = Buku("BK-001", "Pemrograman Python OOP", "Andika Purnama", 3)
    buku2 = Buku("BK-002", "Matematika Diskrit", "Rinaldi Munir", 2)

    # 3. Demonstrasi Class Method
    print(Buku.info_perpustakaan())
    print(buku1.info_buku())
    print(buku2.info_buku())
    print()

    # 4. Pembuatan Object dari class Anggota & transaksi peminjaman
    anggota1 = Anggota("310125001", "Arul", "Ilmu Komputer")
    anggota1.pinjam_buku(buku1)
    anggota1.pinjam_buku(buku2)
    print(anggota1.info_anggota())
    print("Stok setelah dipinjam ->", buku1.info_buku())
    print()

    # 5. Demonstrasi pengembalian & Static Method hitung denda
    anggota1.kembalikan_buku(buku1)
    print("Stok setelah dikembalikan ->", buku1.info_buku())
    print("Simulasi denda telat 3 hari: Rp", Anggota.hitung_denda(3))
