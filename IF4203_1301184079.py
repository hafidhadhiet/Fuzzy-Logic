import pandas as pd
import math

# Penghasilan memiliki tiga linguistik. Miskin, menengah, dan kaya.
# Pengeluaran memiliki tiga linguistik. Hemat, sedang, dan boros.

# Membership function untuk linguisti kaya
def penghasilanKaya(penghasilan):
    if penghasilan >= 16:
        membership = 1
    elif penghasilan <= 6:
        membership = 0
    elif (penghasilan>6) and (penghasilan<16):
        skor = (penghasilan-6)/(16-6)
        membership = round(skor, 2)
    return membership

# Membership function untuk linguistik miskin
def penghasilanMiskin(penghasilan):
    if penghasilan >= 16:
        membership = 1
    elif penghasilan <= 6:
        membership = 0
    elif (penghasilan>6) and (penghasilan<16):
        skor = (penghasilan-6)/(16-6)
        membership = round(skor, 2)    
    return membership

# Membership function untuk linguistik menengah
def penghasilanMenengah(penghasilan):
    if (penghasilan>=10) and (penghasilan<=14):
        membership = 1
    elif (penghasilan>7) and (penghasilan<10):
        skor = (penghasilan-7)/(10-7)
        membership = round(skor, 2)
    elif (penghasilan>14) and (penghasilan<17):
        skor = (17-penghasilan)/(17-14)
        membership = round(skor, 2)
    elif (penghasilan<=7):
        membership = 0
    elif (penghasilan>=17):
        membership = 0
    return membership

# Membership function untuk linguistik Hemat
def pengeluaranHemat(pengeluaran):
    if pengeluaran<=5:
        membership = 1
    elif pengeluaran>=7:
        membership = 0
    elif (pengeluaran>5) and (pengeluaran<7):
        skor = (7-pengeluaran)/(7-5)
        membership = round(skor, 2)
    return membership

# Membership function untuk linguistik boros
def pengeluaranBoros(pengeluaran):
    if pengeluaran>=9:
        membership = 1
    elif pengeluaran<=5:
        membership = 0
    elif (pengeluaran>5) and (pengeluaran<9):
        skor = (pengeluaran-5)/(9-5)
        membership = round(skor, 2)
    return membership

# Membership function untuk linguistik sedang
def pengeluaranSedang(pengeluaran):
    if (pengeluaran>=6) and (pengeluaran<=8):
        membership = 1
    elif (pengeluaran>4) and (pengeluaran<6):
        skor = (pengeluaran-4)/(6-4)
        membership = round(skor, 2)
    elif (pengeluaran>8) and (pengeluaran<10):
        skor = (10-pengeluaran)/(10-8)
        membership = round(skor, 2)
    elif pengeluaran<=4:
        membership = 0
    elif pengeluaran>=10:
        membership = 0
    return membership

# Proses fuzzification dan inferensi
def fuzzificationInference(dataPenghasilan, dataPengeluaran):
    studentFuzzy = []
    i = 0
    while i<len(dataPengeluaran):
        kayaBoros = min(penghasilanKaya(dataPenghasilan[i]), pengeluaranBoros(dataPengeluaran[i]))
        kayaSedang = min(penghasilanKaya(dataPenghasilan[i]), pengeluaranSedang(dataPengeluaran[i]))
        kayaHemat = min(penghasilanKaya(dataPenghasilan[i]), pengeluaranHemat(dataPengeluaran[i]))
        
        menengahBoros = min(penghasilanMenengah(dataPenghasilan[i]), pengeluaranBoros(dataPengeluaran[i]))
        menengahSedang = min(penghasilanMenengah(dataPenghasilan[i]), pengeluaranSedang(dataPengeluaran[i]))
        menengahHemat = min(penghasilanMenengah(dataPenghasilan[i]), pengeluaranHemat(dataPengeluaran[i]))
        
        miskinBoros = min(penghasilanKaya(dataPenghasilan[i]), pengeluaranBoros(dataPengeluaran[i]))
        miskinSedang = min(penghasilanKaya(dataPenghasilan[i]), pengeluaranSedang(dataPengeluaran[i]))
        miskinHemat = min(penghasilanKaya(dataPenghasilan[i]), pengeluaranHemat(dataPengeluaran[i]))

        accepted = max(menengahBoros, miskinBoros, miskinHemat, miskinSedang)
        rejected = max(kayaSedang, kayaHemat)
        considered = max(kayaBoros, menengahSedang, menengahHemat)
        total = accepted+rejected+considered
        
        studentFuzzy.append([i, [rejected, considered, accepted], round(total, 2)])
        i = i+1
    
    return studentFuzzy

# Proses defuzzification menggunakan sugeno
# Rejected = 40
# Considered = 72
# Accepted = 100
def defuzzification(studentFuzzy):
    i = 0
    studentDefuzzy = []
    
    while i<len(studentFuzzy):
        if studentFuzzy[i][2] == 0:
            studentDefuzzy.append([i, 0])
        else:
            skorAkhir = ((40*studentFuzzy[i][1][0])+(72*studentFuzzy[i][1][1])+((100*studentFuzzy[i][1][2])))/(studentFuzzy[i][2])
            studentDefuzzy.append([i+1, round(skorAkhir, 2)])
        i = i+1
    return studentDefuzzy

# Menyeleksi 20 id terbaik yang direkomendasikan untuk diberikan bantuan
def outputProgram(studentDefuzzy):
    studentDefuzzy.sort(key = lambda x: x[1])  
    studentDefuzzy.reverse()
    i = 0
    hasil = []
    while i<20:
        hasil.append(studentDefuzzy[i][0])
        i = i+1
    return hasil

data = pd.read_excel("Mahasiswa.xls")
dataPenghasilan = data["Penghasilan"]
dataPengeluaran = data["Pengeluaran"]
fuzzy = fuzzificationInference(dataPenghasilan, dataPengeluaran)
defuzzy = defuzzification(fuzzy)
hasilAkhir = outputProgram(defuzzy)
dataExport = pd.DataFrame(hasilAkhir, columns=["Penerima Bantuan"])
dataExport.to_excel("Bantuan.xls", index=False, header=True)