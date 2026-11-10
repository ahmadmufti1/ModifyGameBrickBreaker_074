🚀 Fitur & Modifikasi - Block Breaker (Neon Arcade Edition)

Proyek ini merupakan pengembangan dari game klasik Block Breaker berbasis Python menggunakan pustaka Pygame. Berbagai fitur modern, mekanisme interaktif, serta peningkatan visual telah ditambahkan untuk membuat permainan jauh lebih seru, kompetitif, dan menarik secara visual.
✨ Daftar Fitur & Modifikasi Utama
1. Sistem Blok & Kesehatan Variatif (Multi-Health Blocks)

    Blok Hijau (GREEN): Memiliki health 100 (hancur dalam 1 kali pukul) dan memberikan 5 poin.

    Blok Putih (WHITE): Memiliki health 200 (hancur dalam 2 kali pukul) dan memberikan 10 poin. Warnanya akan berubah menjadi hijau saat sisa health tinggal 100.

    Blok Merah (RED): Memiliki health tertinggi yaitu 300 (butuh 3 kali pukul) dan memberikan 15 poin. Warnanya akan berubah secara dinamis menjadi putih lalu hijau seiring berkurangnya health sebelum hancur.

2. Mekanisme Peluncuran Bola Manual (Standby & Launch)

    Bola tidak langsung bergerak otomatis saat permainan dimulai atau setelah nyawa berkurang.

    Bola akan menempel (standby) di atas papan pemukul (striker) dan baru akan meluncur ke atas arena ketika pemain menekan tombol Spasi.

3. Sistem Multi-Ball & Drop Power-Up

    Atribut Item Jatuh: Setiap kali balok hancur, terdapat peluang acak sebesar 30% bagi balok tersebut untuk menjatuhkan kotak power-up ke bawah.

    Klaim Item: Pemain harus menggerakkan striker untuk menangkap item yang jatuh agar efek power-up aktif. Jika item jatuh melewati batas bawah layar, item akan hilang.

    Variasi Item Berdasarkan Warna & Jenis:

        🟡 Kuning (B - Multi-Ball): Memunculkan bola tambahan baru di atas striker yang langsung aktif bergerak. Permainan baru akan kalah jika semua bola di layar habis jatuh.

        🔵 Cyan (W - Wide Paddle): Memperlebar ukuran papan pemukul (striker) secara sementara waktu selama 8 detik untuk memudahkan pertahanan.

        🟣 Ungu (+ - Extra Life): Menambahkan jumlah nyawa (lives) pemain sebanyak +1.

4. Navigasi & Alur Game Lengkap (UI/UX)

    Start Screen (Menu Utama): Menampilkan layar sambutan bertuliskan "NEON BLOCK BREAKER" dengan instruksi kontrol sebelum game dimulai.

    Victory Screen (Layar Kemenangan): Layar khusus yang muncul lengkap dengan total skor akhir jika pemain berhasil membersihkan seluruh balok di arena.

    Game Over Screen: Layar kekalahan saat seluruh nyawa habis, menyediakan opsi untuk mengulang permainan dengan menekan tombol Spasi.

    UI Real-Time: Informasi Skor, Nyawa (Lives), dan jumlah Bola Aktif (Balls) ditampilkan secara langsung di bagian atas layar permainan agar mudah dipantau.

5. Peningkatan Estetika Visual (Neon Arcade Style)

    Tema Visual Neon: Menggunakan latar belakang gelap kebiruan (#0A0A0F) dipadukan dengan palet warna neon yang kontras dan cerah ala mesin arcade modern.

    Efek Jejak Bola (Trail Effect / Motion Blur): Bola meninggalkan bayangan jejak cahaya di belakangnya saat bergerak untuk menciptakan kesan kecepatan yang dinamis.

    Desain Objek Presisi: Balok dan striker didesain menggunakan sudut melengkung (border radius) serta garis tepi (border) agar terlihat lebih berdimensi dan tidak datar.

🕹️ Panduan Kontrol Permainan

    Tombol Kiri / Kanan (← / →): Menggerakkan papan pemukul (striker).

    Tombol Spasi (SPACE): Meluncurkan bola dari atas striker di awal permainan / menghidupkan kembali game saat di menu Game Over/Victory.

    Tombol Escape (ESC): Keluar dari permainan.
