# 15-Puzzle-Branch-and-Bound
Program pencari solusi dari 15-Puzzle dengan algoritma branch and bound.
Dibuat untuk memenuhi tugas kecil 3 mata kuliah IF2211 Strategi Algoritma dengan menggunakan bahasa pemrograman Python.

## Menjalankan Program
1. Clone repository ini atau ekstrak file jika didownload dalam bentuk zip.
2. Jalankan file `main.py`. 
3. Jika ingin membaca puzzle yang di-generate secara random, pilih opsi 1.
4. Jika ingin membaca puzzle dari file, pilih opsi 2.
6. Masukkan nama file (sertakan .txt). ex: **input1.txt** <br/>
Persoalan yang dapat diselesaikan: **input1.txt, input2.txt, input3.txt**. <br/>
Persoalan yang tidak dapat diselesaikan: **input4.txt, input5.txt**.
6. Solusi dari puzzle akan ditampilkan.

## Catatan
Fungsi heuristik pada algoritma branch and bound yang digunakan kurang optimal sehingga tidak dijamin untuk dapat menyelesaikan seluruh persoalan dalam waktu yang singkat. Kasus ini dapat terjadi saat membaca puzzle yang di-generate secara random atau dari masukan puzzle yang solusinya membutuhkan lebih dari 20 langkah pergerakan.

## Author
13520002 - Muhammad Fikri Ranjabi - K02