#to do:
#pengaturan akun -> ganti nama, ganti pass, ganti email
#lupa password
#delete pesanan json ikut keprint soal e
#- sama = -> sama rata
#encryption
#potongan biaya pesanan
#kapan daftar member ?
#kapan registrasi ?

'''
DOKUMENTASI
1. List Function dan atau lambda
printHeader -> print ----Billing iCafe----
validateEmail -> cek apakah format email valid atau tidak
formatRupiah -> mengubah angka atau float ke bentuk rupiah

printTable -> output list 2 dimensi ke dalam bentuk tabel

printNota(data, typeP=0):
output list 2 dimensi ke dalam bentuk nota
paramteter data :
isi list 2 dimensi
contoh :
printNota([["Nama", "Riezqu Ibnanta"], ["Biaya", 200000]])
parameter typeP :
typeP = 0 -> dengan datetime sekarang
typeP = 1 -> tanpa datetime sekarang

openJSON_as_dict(filename):
membuka file json dengan argumen filename, dan akan mengembalikan dalam bentuk json

writeJSON(data, file):
menulis 'file'.json dengan data dari parameter data

page_membership(data, email):
Halaman untuk mengolah cek membership.

page_transaksi(data,email):
Halaman untuk mengolah pembuatan transaksi.

page_data_transaksi_rincian(index, data, email):
Halaman untuk mengoutputkan rincian transaksi

page_data_transaksi(data, email):
Halaman untuk mengolah data transaksi

mainMenu(data, email):
Halaman untuk mengolah mainmenu ketika user sudah berhasil login

login(data):
Halaman untuk mengolah bagian login

register(data):
Halaman untuk mengolah bagian pendaftaran

main(data):
Halaman yang ditampilkan pertama kali

page_pengaturanAkun(data, email):
Halaman untuk mengolah pengaturan akun
'''

from datetime import datetime as dt
import json
import os
import re

filename = 'customer.json'

#harga
hargaMembership = 30000
hargaBilling = [
["Standard", 4000],
["VIP", 6000],
["VVIP", 9000]
]
dictHargaBilling = {
	"Standard":4000,
	"VIP":6000,
	"VVIP":9000
}

#see page_transaksi, biar bisa milih by index
hargaMakananMinuman = [
    ["Mie",5000],
    ["Roti",2000],
    ["Teh",2500],
    ["Cola",5000],
    ["Jus",6000]
]
#biar bisa panggil harga by key
dictHargaMakananMinuman = {
	"Mie":5000,
	"Roti":2000,
	"Teh":2500,
	"Cola":5000,
	"Jus":6000
}

#potongan
potonganOpening = 0.1
maxPotonganOpening = 10**4

jamNightTime = 21
potonganNightTime = 0.1
maxPotonganNightTime = 10**4

printHeader = lambda : print('------------------Billing iCafe------------------')
validateEmail = lambda email : re.match(r"[^@]+@[^@]+\.[^@]+", email)
formatRupiah = lambda angka : "Rp {:0,.0f}".format(angka)

def printTable(data):
    s = [[str(e) for e in row] for row in data]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    print('\n'.join(table))

#printNota typeP 0 -> ada datetime, typeP 1 -> ngga ada datetime
def printNota(data, typeP=0):
	os.system("cls")
	printHeader()
	if not(typeP):
		print(dt.now())
	key = [i[0] for i in data]
	maxLen = max([len(i) for i in key])
	for i in data:
		print("{p[0]:<{0}} : {p[1]}".format(maxLen, p=i))
	print('-------------------TERIMAKASIH-------------------')
	print('(tekan apa saja untuk lanjut)')
	input()

def openJSON_as_dict(filename):
    with open(filename, 'r') as f: return json.load(f)

def writeJSON(data, file) :
    with open(file, 'w') as f : json.dump(data, f, indent=4)

#pages
def page_membership(data, email):
	global filename

	os.system("cls")
	printHeader()

	if data[email]['isMember']:
		print('{0:^48s}'.format('Anda SUDAH terdaftar sebagai member.'))
		print('(tekan enter untuk kembali)')
		input()

	else:
		print('{0:^48s}'.format('Anda BELUM terdaftar sebagai member.'))
		while True :
			print('{0:^48s}'.format('Pembuatan member dikenanakan biaya ' + formatRupiah(hargaMembership)))
			print("1. Buat member")
			print("0. Kembali")
			print()
			pilihan = input("Pilih Menu : ")
			if pilihan == '1':
				data[email]['isMember'] = True
				writeJSON(data, filename)
				printNota([
					["Pesan", 'Selamat! Member anda berhasil dibuat.'], 
					["Biaya Membership", formatRupiah(hargaMembership)]
				])
				return
			elif pilihan == '0':
				return
			else:
				print('Nomor yang anda masukkan tidak ada dalam menu.')

def page_transaksi(data, email):
	global potonganOpening
	global maxPotonganOpening

	global jamNightTime
	global potonganNightTime
	global maxPotonganOpening

	global filename

	#yang disimpen di json udah kena effect membership ok
	newT = dict()
	newT['Tanggal'] = '{}'.format(dt.now())
	newT['isMember'] = data[email]['isMember']
	while True:
		try:
			print("Jenis Billing")
			for i,j in enumerate(hargaBilling):
				print("{}. {:<10s} : {}/jam".format(i+1, j[0], j[1]))
			print()
			jn = int(input("Pilih baris jenis billing : "))

			newT['Jenis Billing'] = hargaBilling[jn-1][0]
			break
		except ValueError:
			print("Angka tidak valid.")
		except KeyError:
			print("Jenis billing tidak tersedia.")
	#durasi
	while True:
		try:
			it = int(input("Durasi Billing (jam) : "))
			if it <= 0:
				print("Minimal durasi billing 1 jam.")
			elif it > 24:
				print("Durasi billing maksimal 24 jam.")
			else:
				newT['Durasi Billing'] = it
				break
		except ValueError:
			print("Angka tidak valid.")


	#calculate biaya raw
	biayaRaw = hargaBilling[jn-1][1] * it

	#membership effect
	if data[email]['isMember']:
		if jn > 1:
			biayaRaw = hargaBilling[jn-2][1] * it
	newT['Biaya'] = biayaRaw

	#calculate diskon opening
	potongan_1 = potongan_2 = 0
	if it > 4:
		potongan_1 = int(biayaRaw * potonganOpening)
		if potongan_1 > maxPotonganOpening:
			potongan_1 = maxPotonganOpening

	#calculate diskon nightTime
	if dt.now().hour >= jamNightTime:
		potongan_2 = int(biayaRaw * potonganNightTime)
		if potongan_2 > maxPotonganNightTime:
			potongan_2 = maxPotonganNightTime

	newT['Diskon Opening'] = potongan_1
	newT['Diskon Night Time'] = potongan_2

	newT['Pesanan'] = dict()

	#pesanan
	while True:
		pilihan = input("Apakah anda ingin memesan makanan / minuman ? [y/t] ")
		if pilihan == 'y':
			#pesen makanan, gak tak jadiin fungsi
			isPesan = 'y'
			while True:
				if isPesan == 'y':
					print("Daftar Harga")
					for i, j in enumerate(hargaMakananMinuman):
						print("{}. {:<5s} : {}".format(i + 1, j[0], j[1]))
					print()
					try:
						pilihan_2 = int(input("Silahkan pilih : "))
						if pilihan_2 < 1 :
							print("Angka tidak valid.")
							continue
						print()
						pilihan_3 = int(input("Jumlah : "))
						if pilihan_3 < 1 :
							print("Angka tidak valid")
					except ValueError:
						print("Angka tidak valid.")
						continue
					except IndexError:
						print("Pilihan tidak valid.")
						continue
					#cek sebelumnya jika emang udah pesen (nambah quantity)
					if hargaMakananMinuman[pilihan_2 - 1][0] in newT['Pesanan']:
						newT['Pesanan'][hargaMakananMinuman[pilihan_2 - 1][0]] += pilihan_3
					else:
						newT['Pesanan'][hargaMakananMinuman[pilihan_2 - 1][0]] = pilihan_3
					print("{} sebanyak {} berhasil ditambahkan dengan total harga Rp {:0,.0f}".format(hargaMakananMinuman[pilihan_2 - 1][0], pilihan_3, pilihan_3 * hargaMakananMinuman[pilihan_2 - 1][1]))
					
				elif isPesan == 't':
					break
				else:
					print("Input tidak valid.")
				isPesan = input("Apakah ada pesanan lagi ? [y/t] ")
			break
		elif pilihan == 't':
			break
		else:
			print("Input salah.")
	
	#nota
	nota = [
		["Nama", data[email]['Nama']],
		["Jenis Billing", newT['Jenis Billing']],
		["Durasi Billing",str(newT["Durasi Billing"]) + " jam"],
		["Membership", data[email]['isMember']],
		['Biaya', formatRupiah(biayaRaw)],
		['Diskon Opening', formatRupiah(potongan_1)],
		['Diskon Night Time', formatRupiah(potongan_2)]
	]

	#pesanan
	#to do diskon makanan
	totalHargaMakanan = 0
	if newT['Pesanan']:
		nota.append(['Pesanan', ''])
		for i in newT['Pesanan'].keys():
			nota.append([i, formatRupiah(dictHargaMakananMinuman[i] * newT['Pesanan'][i])])
			totalHargaMakanan += dictHargaMakananMinuman[i] * newT['Pesanan'][i]
	else:
		nota.append(['Pesanan', 'Tidak ada'])

	newT['Biaya'] += totalHargaMakanan - potongan_1 - potongan_2

	nota.append(['Total', formatRupiah(newT['Biaya'])])

	#add to json
	data[email]['Transaksi'].append(newT)
	writeJSON(data, filename)
	printNota(nota)


def page_data_transaksi_rincian(index, data, email):
	nota = [
	["Nama", data[email]['Nama']]
	]
	for i in data[email]['Transaksi'][index].keys():
		if i != 'Pesanan':
			if i == 'Durasi Billing':
				nota.append([i, str(data[email]['Transaksi'][index][i]) + " jam"])
				#add biaya billing di nota
				#effect membership
				basePrice = dictHargaBilling[data[email]['Transaksi'][index]['Jenis Billing']]
				if data[email]['Transaksi'][index]['isMember']:
					#need better approach
					if data[email]['Transaksi'][index]['Jenis Billing'] == 'VIP':
						basePrice = dictHargaBilling['Standard']
					elif data[email]['Transaksi'][index]['Jenis Billing'] == 'VVIP':
						basePrice = dictHargaBilling['VIP']

				nota.append(['Biaya Billing', formatRupiah(data[email]['Transaksi'][index][i] * basePrice)])
			elif i == 'Biaya':
				#biaya di akhir
				continue
			else:
				temp = data[email]['Transaksi'][index][i]
				if type(data[email]['Transaksi'][index][i]) == type(0) or type(data[email]['Transaksi'][index][i]) == type(0.1):
					if data[email]['Transaksi'][index][i] > 99:
						temp = formatRupiah(data[email]['Transaksi'][index][i])
				nota.append([i, temp])
	if data[email]['Transaksi'][index]['Pesanan']:
		nota.append(["Pesanan",""])
		for i in data[email]['Transaksi'][index]['Pesanan'].keys():
			nota.append([i, formatRupiah(dictHargaMakananMinuman[i] * data[email]['Transaksi'][index]['Pesanan'][i]) ])
	#finally, biaya
	nota.append(["Total", formatRupiah(data[email]['Transaksi'][index]['Biaya'])])
	printNota(nota, typeP=1)

def page_data_transaksi(data, email):
	os.system("cls")

	if not(data[email]['Transaksi']):
		print("Anda belum pernah melakukan transaksi.")
		print("(tekan enter untuk kembali")
		input()
		return

	printHeader()
	print("-"*22 + "History Transaksi" + "-"*22)
	#simpen value
	listTransaksi = [[x[t] for t in x.keys()] for x in data[email]['Transaksi']]
	#simpen key
	table = [[x for x in data[email]['Transaksi'][0].keys()]]
	#tambahin key no
	table[0].insert(0, "No")

	#formatrupiah, harusnya ada better aproach
	for i in range(len(listTransaksi)):
		for j in range(len(listTransaksi[i])):
			if type(listTransaksi[i][j]) == type(0) or type(listTransaksi[i][j]) == type(0.1):
				if listTransaksi[i][j] > 99:
					listTransaksi[i][j] = formatRupiah(listTransaksi[i][j])
	for i, x in enumerate(listTransaksi):
		#tambahin no
		x.insert(0, i+1)
		table.append(x)
	printTable(table)

	while True:
		print()
		print("1. Lihat rincian transaksi")
		print("0. Kembali")
		print()
		pilihan = input("Pilih Menu : ")
		print()
		if pilihan == '1':
			while True:
				try:
					print('Tekan CTRL + C untuk kembali')
					index = int(input("Pilih baris : "))
					temp = data[email]['Transaksi'][index-1]
					break
				except ValueError:
					print("Angka tidak valid")
				except IndexError:
					print("Baris tidak tersedia")
				except KeyboardInterrupt:
					return
			page_data_transaksi_rincian(index-1, data, email)
		elif pilihan == '0':
			return
		else:
			print('Nomor yang anda masukkan tidak ada dalam menu.')

#page pengaturan akun
def page_pengaturanAkun_gNama(data, email):
	global filename

	os.system("cls")
	printHeader()
	print("============== Ganti Nama ==============")
	print('Tekan CTRL + C untuk membatalkan')
	print("{:<19} : {}".format('Nama sekarang', data[email]['Nama']))
	try:
		namaBaru = input("{:<19} : ".format('Nama baru'))
		while True:
			confirm = input("Nama akan diganti menjadi {}, apakah anda yakin ? [y/t] ".format(namaBaru))
			if confirm == 'y':
				data[email]['Nama'] = namaBaru
				writeJSON(data, filename)
				print("Nama telah berhasil diganti.")
				input('(tekan enter untuk kembali)')
				return
			elif confirm == 't':
				print("Ganti nama dibatalkan")
				input('(tekan enter untuk kembali)')
				return
			else:
				print("Input tidak valid.")
	except KeyboardInterrupt:
		print("Ganti nama dibatalkan.")
		input('(tekan enter untuk kembali)')
		return

def page_pengaturanAkun_gPassword(data, email):
	global filename

	os.system("cls")
	printHeader()
	print("============== Ganti Password ==============")
	print('Tekan CTRL + C untuk membatalkan')
	try:
		while True:
			passBaru = input("{:<26} : ".format('Password baru'))
			konfirmasiPassBaru = input("{:<26} : ".format('Konfirmasi Password baru'))
			if passBaru == konfirmasiPassBaru:
				data[email]['Password'] = passBaru
				writeJSON(data, filename)
				print("Password berhasil diperbarui.")
				input('(tekan enter untuk kembali)')
				return
			else:
				print("Password tidak sama.")
	except KeyboardInterrupt:
		print("Ganti password dibatalkan.")
		input('(tekan enter untuk kembali)')
		return

def page_pengaturanAkun_gEmail(data, email):
	global filename

	os.system("cls")
	printHeader()
	print("============== Ganti Email ==============")
	print('Tekan CTRL + C untuk membatalkan')
	try:
		while True:
			emailBaru = input("{:<26} : ".format('Email baru'))
			if emailBaru in data:
				print("Email telah digunakan. Silahkan cari yang berbeda.")
				continue
			konfirmasiEmailBaru = input("{:<26} : ".format('Konfirmasi Email baru'))
			if emailBaru == konfirmasiEmailBaru:
				data[emailBaru] = data[email]
				del data[email]
				writeJSON(data, filename)
				print("Email berhasil diperbarui.")
				input('(tekan enter untuk kembali)')
				return emailBaru
			else:
				print("Email tidak sama.")
	except KeyboardInterrupt:
		print("Ganti email dibatalkan.")
		input('(tekan enter untuk kembali)')
		return email

def page_pengaturanAkun_hAkun(data, email):
	global filename

	os.system("cls")
	printHeader()
	print("============== Hapus Akun ==============")
	print('Tekan CTRL + C untuk membatalkan')
	try:
		while True:
			yakin = input('Apakah anda yakin untuk menghapus akun ? [y/t] ')
			if yakin == 'y':
				del data[email]
				writeJSON(data, filename)
				print("Akun berhasil dihapus.")
				input('(tekan enter untuk kembali)')
				data = openJSON_as_dict(filename)
				main(data)
			elif yakin == 't':
				print("Hapus akun dibatalkan.")
				input('(tekan enter untuk kembali)')
				return
			else:
				print("Input tidak valid.")
	except KeyboardInterrupt:
		print("Hapus akun dibatalkan.")
		input('(tekan enter untuk kembali)')
		return

def page_pengaturanAkun(data, email):
	while True:
		os.system("cls")
		printHeader()
		txt = "============== Pengaturan Akun =============="
		print(txt)
		print('{0:^{1}s}'.format("Data akun", len(txt)))
		print('{:<19s} : {}'.format('Nama', data[email]['Nama']))
		print('{:<19s} : {}'.format('Email', email))
		print('{:<19s} : {}'.format('Tanggal Registrasi', data[email]['Tanggal Daftar']))
		print()
		print("1. Ganti nama")
		print("2. Ganti password")
		print("3. Ganti email")
		print("4. Hapus akun")
		print("0. Kembali")
		print()
		pilihan = input("Pilih Menu : ")
		print()

		if pilihan == '1':
			page_pengaturanAkun_gNama(data, email)
		elif pilihan == '2':
			page_pengaturanAkun_gPassword(data, email)
		elif pilihan == '3':
			email = page_pengaturanAkun_gEmail(data, email)
		elif pilihan == '4':
			page_pengaturanAkun_hAkun(data, email)
		elif pilihan == '0':
			return email
		else:
			print("Input tidak valid.")

def mainMenu(data, email):
	while True:
		name = data[email]['Nama']
		os.system("cls")
		printHeader()
		print("============== SELAMAT DATANG %s =============="%(name.upper()))
		print('{0:^48s}'.format('-'*22 + 'MENU' + '-'*22))
		print("1. Cek Membership")
		print("2. Lakukan Transaksi")
		print("3. Lihat Data Transaksi")
		print("4. Pengaturan Akun")
		print("0. Keluar")
		print()

		pilihan = input("Pilih Menu : ")

		if pilihan == '1':
			page_membership(data, email)
		elif pilihan == '2':
			page_transaksi(data, email)
		elif pilihan == '3':
			page_data_transaksi(data, email)
		elif pilihan == '4':
			#we need to monitor email changes
			email = page_pengaturanAkun(data, email)
		elif pilihan == '0':
			return
		else:
			print('Nomor yang anda masukkan tidak ada dalam menu.')

def login(data):
	while True:
		try:
			os.system("cls")
			printHeader()
			print('------------------Login------------------')
			print('Tekan CTRL + C untuk keluar dari halaman login')
			email = input("Email : ")
			if not(email in data): 
				print("Email tidak terdaftar.")
				continue
			while True:
				password = input("Pass : ")
				if password != data[email]['Password']:
					print("Password salah")
				else:
					break
			break
		except KeyboardInterrupt:
			return
	mainMenu(data, email)

#register
def register(data):
	while True:
		try:
			os.system("cls")
			printHeader()
			print('------------------Registrasi------------------')
			print('Tekan CTRL + C untuk keluar dari halaman registrasi')

			dataBaru = dict()
			email = input("Email : ")
			if not(validateEmail(email)):
				print("Email tidak valid")
			if email in data:
				print("Email sudah terdaftar.")
				continue

			dataBaru['Nama'] = input("Nama : ")
			dataBaru['Password'] = input("Password : ")
			dataBaru['isMember'] = False
			dataBaru['Tanggal Daftar'] = '{}'.foramt(dt.now())
			dataBaru['Transaksi'] = list()
			data[email] = dataBaru
			writeJSON(data, filename)
			print("Registrasi berhasil !")
			print("(tekan enter untuk lanjut)")
			input()
			return
		except KeyboardInterrupt:
			return

def main(data):
	while True:
		os.system("cls")
		printHeader()
		print("1. Login")
		print("2. Daftar")
		print("0. Keluar")
		print()
		pilihan = input("Silahkan pilih : ")
		if pilihan == '1':
			login(data)
		elif pilihan == '2':
			register(data)
		elif pilihan == '0':
			exit()
		else:
			print("Menu tidak tersedia")

if __name__ == '__main__':
	data = openJSON_as_dict(filename)
	main(data)