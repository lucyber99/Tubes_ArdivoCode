
# Diva Racing Bot – Greedy Diamond Collector

## Penjelasan Singkat Algoritma Greedy yang Diimplementasikan

Bot ini dirancang untuk bermain dalam game berbasis pengambilan diamond menggunakan pendekatan **Efficient Greedy Algorithm**. Tujuannya adalah untuk secara efisien mengumpulkan diamond dengan mempertimbangkan:

- Jarak ke diamond
- Efisiensi penggunaan teleport
- Keadaan inventori (jumlah diamond yang dibawa)
- Situasi khusus seperti waktu habis atau tombol merah aktif
- Musuh yang dapat diserang untuk mencuri diamond

Bot selalu memilih aksi terbaik dengan tidak mempertimbangkan jangka panjang (jarak terpendek atau peluang terbaik saat ini) dengan asumsi keputusan itu membawa hasil maksimal di akhir permainan. Ini sesuai dengan prinsip **greedy**, yaitu mengambil keputusan optimal di setiap langkah tanpa memikirkan konsekuensi jangka panjang.

---

## Requirements dan Instalasi

### Dependencies:

- Python 3.8+
- Docker desktop
- Node JS
- VsCode (atau IDE dan teks Editor lainnya)
- Modul internal dari game: `game.logic.base`, `game.models`, `util.get_direction`
- Game engine/server simulator dari pihak penyelenggara

### Instalasi:

ikuti langkah instalasi dari link berikut:
(https://docs.google.com/document/d/1L92Axb89yIkom0b24D350Z1QAr8rujvHof7-kXRAp7c/edit?tab=t.0)


Author by:
- Diva Amelia Saputri (123140212)
- Arta Eka Yuli Rajagukguk (123140209)
- Revolusi Al-Ghifari (123140199)
