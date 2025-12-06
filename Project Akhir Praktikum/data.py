import json
import os

nama_file_data_rental = 'data_rental.json'
# Fungsi untuk memuat data dari file JSON
def muat_data_dari_file():
    if os.path.exists(nama_file_data_rental):
        with open(nama_file_data_rental, 'r') as file_data_json:
            data_dari_file = json.load(file_data_json)
            return data_dari_file
    else:
        # Data kosong awal
        data_kosong = {
            'daftar_iphone_stok': [],
            'daftar_sewaan_pelanggan': []
        }
        simpan_data_ke_file(data_kosong)
        return data_kosong

# Fungsi untuk menyimpan data ke file JSON
def simpan_data_ke_file(data_untuk_disimpan):
    with open(nama_file_data_rental, 'w') as file_data_json:
        json.dump(data_untuk_disimpan, file_data_json, indent=4)