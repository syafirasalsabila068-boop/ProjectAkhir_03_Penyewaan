import requests
from data import muat_data_dari_file, simpan_data_ke_file
from datetime import datetime, timedelta

data_rental_kasir = muat_data_dari_file()

print("""
██╗██████╗ ██╗  ██╗ ██████╗ ███╗   ██╗███████╗ ██████╗ ██████╗
██║██╔══██╗██║  ██║██╔═══██╗████╗  ██║██╔════╝██╔═████╗╚════██╗
██║██████╔╝███████║██║  ██║██╔██╗ ██║█████╗  ██║██╔██║ █████╔╝
██║██╔═══╝ ██╔══██║██║  ██║██║╚██╗██║██╔══╝  ████╔╝██║ ╚═══██╗
██║██║     ██║  ██║╚██████╔╝██║ ╚████║███████╗╚██████╔╝██████╔╝
╚═╝╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚═════╝
""")

# Menu utama
def tampilkan_menu_kasir():
    print("\n=== Menu Kasir Rental iPhone ===")
    print("-" * 35)
    print("1. Lihat Daftar Harga")
    print("2. Sewa iPhone")
    print("3. Tambah iPhone")
    print("4. Perbarui iPhone")
    print("5. Lihat Semua Sewaan")
    print("6. Cetak Struk")
    print("7. Kembalikan iPhone")
    print("8. Lihat Stok per Model")
    print("9. Keluar")
    print("-" * 35)
    pilihan_menu = input("Pilih nomor: ")
    if pilihan_menu == '1':
        lihat_daftar_harga()
    elif pilihan_menu == '2':
        proses_sewa_iphone()
    elif pilihan_menu == '3':
        tambah_iphone_baru()
    elif pilihan_menu == '4':
        perbarui_iphone_harga()
    elif pilihan_menu == '5':
        lihat_semua_sewaan_pelanggan()
    elif pilihan_menu == '6':
        cetak_struk_sewaan()
    elif pilihan_menu == '7':
        kembalikan_iphone()
    elif pilihan_menu == '8':
        lihat_jumlah_stok_per_model()
    elif pilihan_menu == '9':
        simpan_data_ke_file(data_rental_kasir)
        print("Data disimpan. Selamat tinggal!")
        exit()
    tampilkan_menu_kasir()

# Parse NIK dari API
def parse_nik_dari_api(nomor_nik_masuk):
    url_api_nik = "https://parse1337.vercel.app/api/nik/parse?nik=" + nomor_nik_masuk
    respons_api = requests.get(url_api_nik)
    if respons_api.status_code == 200:
        data_json = respons_api.json()
        if data_json['status'] == 'success':
            data_nik = data_json['data']
            print("\n=== Informasi dari NIK ===")
            print("-" * 30)
            print("Provinsi:", data_nik['provinsi'])
            print("Kabupaten/Kota:", data_nik['kotakab'])
            print("Kecamatan:", data_nik['kecamatan'])
            print("Kode Pos:", data_nik['tambahan']['kodepos'])
            print("-" * 30)
            print("Tanggal Lahir:", data_nik['lahir'])
            print("Tahun Lahir:", data_nik['tambahan']['tahunLahir'])
            print("Kelamin:", data_nik['kelamin'])
            print("-" * 30)
            return nomor_nik_masuk
    print("NIK tidak valid atau kesalahan API.")
    return None

#stok awal,  dengan jumlah unit
def inisialisasi_stok_iphone_awal():
    daftar_iphone_stok = data_rental_kasir['daftar_iphone_stok']
    if not daftar_iphone_stok:
        print("\nStok iPhone kosong. tambahkan iPhone minimal satu")
        print("-" * 50)
        while True:
            jumlah_unit_raw = input("Jumlah unit: ")
            if not jumlah_unit_raw.isdigit():
                print("Jumlah harus angka.")
                continue
            jumlah_unit = int(jumlah_unit_raw)
            if jumlah_unit <= 0:
                print("Ga boleh 0 bang")
                continue
            model_iphone_baru = input("Model iPhone: ")
            kelengkapan_iphone_baru = input("Kelengkapan: ")
            harga_harian_iphone = input("Harga per hari: ")
            if not harga_harian_iphone.isdigit():
                print("Harga harus angka.")
                continue
            harga_harian_iphone = int(harga_harian_iphone)
            
            id_awal = len(daftar_iphone_stok) + 1
            
            # Menyiapkan list untuk ID yang ditambahkan
            id_yang_ditambahkan = []
            
            for i in range(jumlah_unit):
                id_iphone_baru = id_awal + i
                daftar_iphone_stok.append({
                    'id': id_iphone_baru,
                    'model': model_iphone_baru,
                    'harga_per_hari': harga_harian_iphone,
                    'tersedia': True,
                    'kelengkapan': kelengkapan_iphone_baru,
                    'stok': 1
                })
                id_yang_ditambahkan.append(id_iphone_baru) #Menyimpan daftar ID yang baru aja dibuat
            
            simpan_data_ke_file(data_rental_kasir) #penyimpanan permanen
            
            # Baris cetak ID baru dihilangkan sesuai permintaan
            
            print("-" * 30)
            lanjut_tambah = input("Tambah lagi? (y/t): ")
            if lanjut_tambah.lower() != 'y':
                break
        print("Stok siap!")
inisialisasi_stok_iphone_awal()

# Lihat jumlah stok per model
def lihat_jumlah_stok_per_model():
    print("\n=== Jumlah Stok per Model ===")
    print("-" * 50)
    if not data_rental_kasir['daftar_iphone_stok']:
        print("Stok kosong.")
    else:
        # Hitung stok per model
        stok_model_map = {}
        for iphone in data_rental_kasir['daftar_iphone_stok']:
            nama_model = iphone['model']
            if nama_model not in stok_model_map:
                stok_model_map[nama_model] = 0
            stok_model_map[nama_model] = stok_model_map[nama_model] + 1
        for nama_model in stok_model_map:
            print("Model:", nama_model, "| Stok:", stok_model_map[nama_model])
    print("-" * 50)
    input("Tekan enter...")

#LIHAT DAFTAR HARGA
def lihat_daftar_harga():
    print("\n=== Daftar Harga Rental iPhone ===")
    print("-" * 85)
    daftar_iphone_stok = data_rental_kasir['daftar_iphone_stok']
    if not daftar_iphone_stok:
        print("Stok kosong.")
    else:
        nomor_urut = 1
        #grup berdasarkan model untuk menampilkan stok per model dan harga
        grup_per_model = {}
        for iphone in daftar_iphone_stok:
            nama_model = iphone['model']
            if nama_model not in grup_per_model:
                grup_per_model[nama_model] = {
                    'harga_per_hari': iphone['harga_per_hari'], #yang awal buat 
                    'list_unit': [] #nyimpan unit sama
                }
        for model_key in grup_per_model:
            data_model = grup_per_model[model_key]
            harga_hari = data_model['harga_per_hari']
            stok = len(data_model['list_unit'])
            
            id_display = str(nomor_urut)
            
            print("ID : " + id_display + " | " + model_key + " | Hari: Rp " + str(harga_hari) + " | Stok: " + str(stok))
            
            nomor_urut = nomor_urut + 1

    print("-" * 85)
    input("Tekan enter...")

# Proses sewa iPhone
def proses_sewa_iphone():
    nama_penyewa = input("Nama penyewa: ")
    nomor_nik_penyewa = input("Nomor NIK: ")
    info_nik = parse_nik_dari_api(nomor_nik_penyewa)
    if info_nik is None:
        input("Tekan enter...")
        return
    nomor_ktp_penyewa = nomor_nik_penyewa;

    jumlah_tersedia = 0
    for iphone in data_rental_kasir['daftar_iphone_stok']:
        if iphone['tersedia']:
            jumlah_tersedia = jumlah_tersedia + 1
    if jumlah_tersedia == 0:
        print("Tidak ada stok tersedia.")
        input("Tekan enter...")
        return

    # Kelompokkan data berdasarkan Model
    stok_per_model = {}
    for iphone in data_rental_kasir['daftar_iphone_stok']:
        if iphone['tersedia']:
            nama_model = iphone['model']
            if nama_model not in stok_per_model:
                stok_per_model[nama_model] = {
                    'harga': iphone['harga_per_hari'],
                    'kelengkapan': iphone['kelengkapan'],
                    'list_id_asli': [] #simpan id yang sama model nya
                }
            stok_per_model[nama_model]['list_id_asli'].append(iphone['id']) 

    print("\n=== Daftar iPhone Tersedia ===")
    print("-" * 85)

    map_pilihan_ke_model = {}
    nomor_urut = 1

    for model_key in stok_per_model:
        data_model = stok_per_model[model_key]
        harga_hari = data_model['harga']
        stok_model = len(data_model['list_id_asli'])

        map_pilihan_ke_model[nomor_urut] = model_key
        print("ID : " + str(nomor_urut) + " | " + model_key + " | Hari: Rp " + str(harga_hari) + " | Stok: " + str(stok_model))
        nomor_urut = nomor_urut + 1
    print("-" * 85)

    #ubah nama variabel input mentah menjadi input pilihan
    input_pilihan = input("Masukkan ID pilihan: ")
    if not input_pilihan.isdigit():
        print("Input harus angka.")
        input("Tekan enter...")
        return
    id_pilihan = int(input_pilihan)

    if id_pilihan not in map_pilihan_ke_model:
        print("ID pilihan tidak valid.")
        input("Tekan enter...")
        return

    model_dipilih = map_pilihan_ke_model[id_pilihan]
    data_terpilih = stok_per_model[model_dipilih]
    id_iphone_asli = data_terpilih['list_id_asli'][0]

    iphone_ditemukan = None
    for iphone in data_rental_kasir['daftar_iphone_stok']:
        if iphone['id'] == id_iphone_asli:
            iphone_ditemukan = iphone
            break

    print("\nAnda memilih:", iphone_ditemukan['model'])
    print("Kelengkapan:", iphone_ditemukan['kelengkapan'])
    print("Harga per hari: Rp", iphone_ditemukan['harga_per_hari'])

    jumlah_hari_input = input("Jumlah hari sewa: ")
    if not jumlah_hari_input.isdigit():
        print("Harus angka.")
        input("Tekan enter...")
        return
    jumlah_hari = int(jumlah_hari_input)

    if jumlah_hari <= 0:
        print("ga bisa 0.")
        input("Tekan enter...")
        return

    total_harga_sewa = iphone_ditemukan['harga_per_hari'] * jumlah_hari

    if jumlah_hari >= 3:
        diskon = total_harga_sewa * 0.10
        total_harga_sewa = total_harga_sewa - diskon
        print("Diskon 10%: Rp", int(diskon))

    iphone_ditemukan['tersedia'] = False
    data_rental_kasir['daftar_sewaan_pelanggan'].append({
        'nama_pelanggan': nama_penyewa,
        'nomor_ktp': nomor_ktp_penyewa,
        'id_iphone': id_iphone_asli,
        'tanggal_mulai_sewa': str(datetime.now()),
        'jumlah_hari': jumlah_hari,
        'total_harga': total_harga_sewa,
        'tanggal_kembali': None,
        'denda': 0
    })
    simpan_data_ke_file(data_rental_kasir)
    print("Berhasil! Hari:", jumlah_hari, "Harga Total: Rp", int(total_harga_sewa))
    input("Tekan enter...")

# Perbarui iPhone
def perbarui_iphone_harga():
    print("\n=== Perbarui iPhone ===")
    print("-" * 50)
    daftar_iphone_stok = data_rental_kasir['daftar_iphone_stok']
    if not daftar_iphone_stok:
        print("Stok kosong.")
        input("Tekan enter...")
        return
    print("Daftar iPhone:")
    print("-" * 50)
    for iphone in daftar_iphone_stok:
        print("ID:", iphone['id'], "| Model:", iphone['model'], "| Harga: Rp", iphone['harga_per_hari'])
    print("-" * 50)
    id_perbarui_raw = input("ID yang diperbarui: ")
    if not id_perbarui_raw.isdigit():
        print("Input harus angka.")
        input("Tekan enter...")
        return
    id_perbarui = int(id_perbarui_raw)
    iphone_ditemukan = None
    for iphone in daftar_iphone_stok:
        if iphone['id'] == id_perbarui:
            iphone_ditemukan = iphone
            break
    if not iphone_ditemukan:
        print("ID tidak ditemukan.")
        input("Tekan enter...")
        return

    print("1. Perbarui harga/kelengkapan")
    print("2. Tambah stok untuk model ini")
    pilihan_perbarui = input("Pilih: ")
    if pilihan_perbarui == '1':
        harga_baru_raw = input("Harga baru per hari: ")
        if not harga_baru_raw.isdigit():
            print("Harga harus angka.")
        else:
            harga_baru = int(harga_baru_raw)
            kelengkapan_baru = input("Kelengkapan baru: ")
            iphone_ditemukan['harga_per_hari'] = harga_baru
            iphone_ditemukan['kelengkapan'] = kelengkapan_baru
            print("Perbarui berhasil untuk ID:", id_perbarui)
    elif pilihan_perbarui == '2':
        jumlah_tambah_raw = input("Jumlah tambah: ")
        if not jumlah_tambah_raw.isdigit():
            print("Jumlah harus angka.")
        else:
            jumlah_tambah = int(jumlah_tambah_raw)
            if jumlah_tambah <= 0:
                print("Jumlah gak bole 0.")
            else:
                id_awal = len(daftar_iphone_stok) + 1
                model_iphone = iphone_ditemukan['model']
                kelengkapan_iphone = iphone_ditemukan['kelengkapan']
                harga_harian = iphone_ditemukan['harga_per_hari']
                for i in range(jumlah_tambah):
                    id_baru = id_awal + i
                    daftar_iphone_stok.append({
                        'id': id_baru,
                        'model': model_iphone,
                        'harga_per_hari': harga_harian,
                        'tersedia': True,
                        'kelengkapan': kelengkapan_iphone,
                        'stok': 1
                    })
                print("Ditambahkan", jumlah_tambah, "stok untuk model", model_iphone)
    else:
        print("Pilihan tidak valid.")
    simpan_data_ke_file(data_rental_kasir)
    input("Tekan enter...")

# Lihat semua sewaan
def lihat_semua_sewaan_pelanggan():
    print("\n=== Daftar Semua Sewaan ===")
    print("-" * 100)
    daftar_sewaan_saat_ini = data_rental_kasir['daftar_sewaan_pelanggan']
    if not daftar_sewaan_saat_ini:
        print("Belum ada sewaan.")
    else:
        print("No | Nama | KTP | Model | Mulai | Hari | Total | Status")
        print("-" * 100)
        nomor_urut = 1
        for sewaan in daftar_sewaan_saat_ini:
            model_iphone_sewa = None
            for iphone in data_rental_kasir['daftar_iphone_stok']:
                if iphone['id'] == sewaan['id_iphone']:
                    model_iphone_sewa = iphone['model']
                    break
            status = "Belum Dikembalikan" if sewaan['tanggal_kembali'] is None else "Sudah Dikembalikan"
            print(str(nomor_urut), "|", sewaan['nama_pelanggan'], "|", sewaan['nomor_ktp'], "|", str(model_iphone_sewa), "|", sewaan['tanggal_mulai_sewa'], "|", str(sewaan['jumlah_hari']), "| Rp", str(sewaan['total_harga']), "|", status)
            nomor_urut = nomor_urut + 1
    print("-" * 100)
    input("Tekan enter...")

# Tambah iPhone
def tambah_iphone_baru():
    print("\n=== Tambah iPhone Baru ===")
    daftar_iphone_stok = data_rental_kasir['daftar_iphone_stok']
    jumlah_unit_raw = input("Jumlah unit: ")
    if not jumlah_unit_raw.isdigit():
        print("Jumlah harus angka.")
        input("Tekan enter...")
        return
    jumlah_unit = int(jumlah_unit_raw)
    if jumlah_unit <= 0:
        print("ga boleh 0 / min.")
        input("Tekan enter...")
        return
    model_iphone_baru = input("Model: ")
    kelengkapan_iphone_baru = input("Kelengkapan: ")
    harga_harian_baru_raw = input("Harga per hari: ")
    if not harga_harian_baru_raw.isdigit():
        print("Harga harus angka.")
        input("Tekan enter...")
        return
    harga_harian_baru = int(harga_harian_baru_raw)
    id_awal = len(daftar_iphone_stok) + 1
    for i in range(jumlah_unit):
        id_iphone_baru = id_awal + i
        daftar_iphone_stok.append({
            'id': id_iphone_baru,
            'model': model_iphone_baru,
            'harga_per_hari': harga_harian_baru,
            'tersedia': True,
            'kelengkapan': kelengkapan_iphone_baru,
            'stok': 1
        })
    simpan_data_ke_file(data_rental_kasir)
    print("Berhasil menambahkan", jumlah_unit, "unit", model_iphone_baru)

    input("Tekan enter...")

# Kembalikan iPhone
def kembalikan_iphone():
    daftar_sewaan_aktif = []
    for sewaan in data_rental_kasir['daftar_sewaan_pelanggan']:
        if sewaan['tanggal_kembali'] is None:
            daftar_sewaan_aktif.append(sewaan)
    if not daftar_sewaan_aktif:
        print("Tidak ada sewaan aktif.")
        input("Tekan enter...")
        return
    print("\n=== Daftar Sewaan Aktif ===")
    print("-" * 70)
    for nomor_urut, sewaan in enumerate(daftar_sewaan_aktif, 1):
        model_iphone_sewa = None
        for iphone in data_rental_kasir['daftar_iphone_stok']:
            if iphone['id'] == sewaan['id_iphone']:
                model_iphone_sewa = iphone['model']
                break
        print(str(nomor_urut) + ". Nama: " + sewaan['nama_pelanggan'] + " - Model: " + model_iphone_sewa + " - Mulai: " + sewaan['tanggal_mulai_sewa'])
    print("-" * 70)
    nomor_sewa_pilih_raw = input("Nomor sewaan: ")
    if not nomor_sewa_pilih_raw.isdigit():
        print("Nomor tidak valid.")
        input("Tekan enter...")
        return
    nomor_sewa_pilih = int(nomor_sewa_pilih_raw) - 1
    if 0 <= nomor_sewa_pilih < len(daftar_sewaan_aktif):
        sewaan_terpilih = daftar_sewaan_aktif[nomor_sewa_pilih]
        # parsing tanggal mulaina
        if '.' in sewaan_terpilih['tanggal_mulai_sewa']:
            tanggal_mulai = datetime.strptime(sewaan_terpilih['tanggal_mulai_sewa'], '%Y-%m-%d %H:%M:%S.%f')
        else:
            tanggal_mulai = datetime.strptime(sewaan_terpilih['tanggal_mulai_sewa'], '%Y-%m-%d %H:%M:%S')
        tanggal_kembali = datetime.now()
        harian_up = (tanggal_kembali - tanggal_mulai).days
        if harian_up < 0:
            harian_up = 0
        hari_lebih = harian_up - sewaan_terpilih['jumlah_hari']
        if hari_lebih < 0:
            hari_lebih = 0
        # Untuk menghindari pembagian dengan 0 jika jumlah_hari 0 
        denda = 0
        if sewaan_terpilih['jumlah_hari'] > 0:
            denda = hari_lebih * (sewaan_terpilih['total_harga'] / sewaan_terpilih['jumlah_hari']) * 1.5
        sewaan_terpilih['tanggal_kembali'] = str(tanggal_kembali)
        sewaan_terpilih['denda'] = denda
        sewaan_terpilih['total_harga'] = sewaan_terpilih['total_harga'] + denda

        # Update stok
        for iphone in data_rental_kasir['daftar_iphone_stok']:
            if iphone['id'] == sewaan_terpilih['id_iphone']:
                iphone['tersedia'] = True
                break

        simpan_data_ke_file(data_rental_kasir)

        model_terpilih = None
        for iphone in data_rental_kasir['daftar_iphone_stok']:
             if iphone['id'] == sewaan_terpilih['id_iphone']:
                 model_terpilih = iphone['model']
                 break

        print("\nPengembalian iPhone Berhasil!")
        print("Model:", model_terpilih)
        print("Penyewa:", sewaan_terpilih['nama_pelanggan'])
        print("Hari Aktual Sewa:", harian_up, "hari")
        if hari_lebih > 0:
            print("Keterlambatan:", hari_lebih, "hari. Denda: Rp", int(denda))
        print("Total Biaya Akhir: Rp", int(sewaan_terpilih['total_harga']))


    else:
        print("Nomor tidak valid.")
    input("Tekan enter...")

# Cetak struk sewaan
def cetak_struk_sewaan():
    daftar_sewaan_aktif = []
    for sewaan in data_rental_kasir['daftar_sewaan_pelanggan']:
        if sewaan['tanggal_kembali'] is None:
            daftar_sewaan_aktif.append(sewaan)
    if not daftar_sewaan_aktif:
        print("Tidak ada sewaan aktif.")
        input("Tekan enter...")
        return
    print("\n=== Daftar Sewaan Aktif ===")
    print("-" * 50)
    for nomor_urut, sewaan in enumerate(daftar_sewaan_aktif, 1):
        model_iphone_sewa = None
        for iphone in data_rental_kasir['daftar_iphone_stok']:
            if iphone['id'] == sewaan['id_iphone']:
                model_iphone_sewa = iphone['model']
                break
        print(str(nomor_urut) + ". Nama: " + sewaan['nama_pelanggan'] + " - Model: " + model_iphone_sewa + " - Total: Rp " + str(sewaan['total_harga']))
    print("-" * 50)
    nomor_struk_pilih_raw = input("Nomor struk: ")
    if not nomor_struk_pilih_raw.isdigit():
        print("Nomor tidak valid.")
        input("Tekan enter...")
        return
    nomor_struk_pilih = int(nomor_struk_pilih_raw) - 1
    if 0 <= nomor_struk_pilih < len(daftar_sewaan_aktif):
        sewaan_terpilih = daftar_sewaan_aktif[nomor_struk_pilih]
        model_terpilih = None
        for iphone in data_rental_kasir['daftar_iphone_stok']:
            if iphone['id'] == sewaan_terpilih['id_iphone']:
                model_terpilih = iphone['model']
                break
        #cetak struk
        print("\n=== STRUK PENYEWAAN IPHONE ===")
        print("-" * 40)
        print("Nama Penyewa:", sewaan_terpilih['nama_pelanggan'])
        print("Nomor KTP:", sewaan_terpilih['nomor_ktp'])
        print("Model iPhone:", model_terpilih)
        print("Tanggal Mulai Sewa:", sewaan_terpilih['tanggal_mulai_sewa'])
        print("Estimasi Selesai: Mulai tanggal di atas +", sewaan_terpilih['jumlah_hari'], "hari")
        print("Jumlah Hari Sewa:", sewaan_terpilih['jumlah_hari'])
        print("Total Harga Sewa: Rp", sewaan_terpilih['total_harga'])
        print("Terima kasih!")
        print("-" * 40)
    else:
        print("Nomor tidak valid.")
    input("Tekan enter...")
 
tampilkan_menu_kasir()