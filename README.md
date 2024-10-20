---

# Bot Verifikasi Video Telegram

Ini adalah bot Telegram yang dirancang untuk verifikasi dan manajemen video. Bot ini memungkinkan pemilik untuk mengupload, menghapus, dan mengelola video, sementara pengguna dapat memverifikasi keanggotaan mereka dengan mengirimkan screenshot.

## Fitur

- Perintah pemilik untuk mengelola tautan verifikasi dan video.
- Perintah pengguna untuk mengonfirmasi keanggotaan dan mengakses video.
- Proses verifikasi screenshot.
- Fungsionalitas upload dan penghapusan video.

## Persyaratan

- Python 3.7+
- MongoDB
- Token Bot Telegram

## Instalasi

1. **Clone repositori**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Buat lingkungan virtual** (opsional tetapi disarankan):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Pada Windows gunakan `venv\Scripts\activate`
   ```

3. **Install paket yang dibutuhkan**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Siapkan variabel lingkungan**:
   Buat file `.env` di root proyek dan tambahkan variabel berikut:
   ```plaintext
   MONGO_URI=<mongodb_uri_anda>
   TELEGRAM_TOKEN=<token_bot_telegram_anda>
   OWNER_ID=<id_telegram_anda>
   VERIFICATION_LINK=<tautan_verifikasi_anda>
   ```

   - `MONGO_URI`: String koneksi untuk database MongoDB Anda.
   - `TELEGRAM_TOKEN`: Token yang Anda terima dari BotFather.
   - `OWNER_ID`: ID pengguna Telegram Anda (Anda dapat menemukannya menggunakan bot seperti @userinfobot).
   - `VERIFICATION_LINK`: Tautan ke grup yang harus diikuti oleh pengguna untuk verifikasi.

## Menjalankan Bot

1. **Mulai bot**:
   ```bash
   python your_bot_file.py
   ```

2. Bot akan berjalan dan mencatat statusnya ke konsol.

## Penggunaan

### Perintah Pemilik

- **Setel Tautan Verifikasi**: 
  ```
  /set_verification_link <tautan_baru>
  ```

- **Perintah Bantuan**: 
  ```
  /help
  ```

- **Upload Video**: 
  Gunakan tombol yang disediakan di dalam bot.

- **Hapus Video**: 
  Gunakan tombol yang disediakan di dalam bot.

### Perintah Pengguna

- **Mulai Interaksi**: 
  ```
  /start
  ```

- **Konfirmasi Keanggotaan**: 
  Klik tombol "Konfirmasi Bergabung".

- **Kirim Screenshot**: 
  Setelah mengonfirmasi keanggotaan, kirim screenshot keanggotaan grup Anda.

- **Daftar Video**: 
  Klik tombol "Lihat Video" untuk melihat video yang tersedia.

## Deploy Bot

Anda dapat melakukan deploy bot di server mana pun yang mendukung Python. Berikut adalah panduan sederhana menggunakan server cloud seperti DigitalOcean atau AWS.

### Langkah untuk Deploy

1. **Buat Server**: Siapkan server cloud baru dengan Ubuntu.

2. **SSH ke Server Anda**:
   ```bash
   ssh user_anda@ip_server_anda
   ```

3. **Install Python dan Pip** (jika belum terpasang):
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip
   ```

4. **Install MongoDB**:
   Ikuti instruksi di [panduan instalasi MongoDB](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/).

5. **Clone Repositori**:
   Ikuti langkah yang sama seperti di bagian instalasi.

6. **Siapkan Variabel Lingkungan**:
   Buat file `.env` seperti yang dijelaskan sebelumnya.

7. **Jalankan Bot**:
   Mulai bot Anda seperti yang ditunjukkan di bagian menjalankan.

8. **Menggunakan `screen` untuk Menjalankan Bot**:
   Anda dapat menggunakan alat seperti `screen` untuk menjaga bot tetap berjalan setelah Anda log out:
   ```bash
   sudo apt install screen
   screen
   python your_bot_file.py
   ```

9. **Mendetach dari Screen**: Tekan `Ctrl+A`, lalu `D` untuk mendetach.

## Pemecahan Masalah

- **Log**: Periksa output konsol untuk menemukan kesalahan.
- **Koneksi MongoDB**: Pastikan URI MongoDB Anda benar dan dapat diakses dari server Anda.
- **Masalah Bot Telegram**: Verifikasi bahwa token bot Anda benar dan bahwa Anda menggunakan perintah bot dengan benar.

## Lisensi

Proyek ini dilisensikan di bawah Lisensi MIT.

---
