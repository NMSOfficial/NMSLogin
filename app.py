import tkinter as tk
from tkinter import messagebox
import sqlite3
import bcrypt
import re
import random

def veritabanı_oluştur():
    conn = sqlite3.connect('kullanici_veri.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS kullanici (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        password TEXT)''')
    conn.commit()
    conn.close()

def sıralı_karakterler(var):
    for i in range(len(var) - 1):
        if ord(var[i]) + 1 == ord(var[i + 1]):
            return True
    return False

def şifre_güvenliğini_kontrol_et(password):
    if (len(password) < 8 or 
        not re.search("[a-z]", password) or 
        not re.search("[A-Z]", password) or 
        not re.search("[0-9]", password) or 
        not re.search("[!@#$%^&*(),.?\":{}|<>]", password)):
        return False
    return True

def kaydet():
    username = entry_kullanici_adi_kayit.get()
    password = entry_sifre_kayit.get().encode('utf-8')

    if not şifre_güvenliğini_kontrol_et(password.decode('utf-8')):
        messagebox.showerror("Hata", "Şifre en az 8 karakter olmalı, bir büyük harf, bir küçük harf, bir rakam ve bir özel karakter içermelidir!")
        return
    
    if sıralı_karakterler(password.decode('utf-8')):
        messagebox.showerror("Hata", "Şifre sıralı karakterler içermemelidir!")
        return

    if username.lower() == password.decode('utf-8').lower():
        messagebox.showerror("Hata", "Şifre, kullanıcı adıyla aynı olamaz!")
        return

    # Random tuz oluşturma (4-31 arası)
    random_tuz = random.randint(4, 31)
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt(random_tuz))
    
    try:
        conn = sqlite3.connect('kullanici_veri.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO kullanici (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        messagebox.showinfo("Başarılı", "Kayıt başarılı!")
        frame_kayit.pack_forget()  # Kayıt formunu gizle
        frame_giris.pack(pady=20)   # Giriş formunu göster
    except sqlite3.IntegrityError:
        messagebox.showerror("Hata", "Kullanıcı adı zaten mevcut!")
    finally:
        conn.close()


def giris():
    username = entry_kullanici_adi.get()
    password = entry_sifre.get().encode('utf-8')
    
    conn = sqlite3.connect('kullanici_veri.db')
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM kullanici WHERE username = ?", (username,))
    result = cursor.fetchone()
    
    if result and bcrypt.checkpw(password, result[0]):
        print("Giriş başarılı!")
    else:
        messagebox.showerror("Hata", "Kullanıcı adı veya şifre hatalı!")
    
    conn.close()

def goster_kayit():
    frame_giris.pack_forget()
    frame_kayit.pack(pady=20)

def goster_giris():
    frame_kayit.pack_forget()
    frame_giris.pack(pady=20)

def on_enter(e):
    e.widget['bg'] = '#D9D9D9'  # Hover rengi

def on_leave(e):
    e.widget['bg'] = '#f7f7f7'  # Normal rengi

def buton_animasyon(buton):
    buton['relief'] = 'sunken'
    buton.after(100, lambda: buton.config(relief='raised'))

veritabanı_oluştur()

pencere = tk.Tk()
pencere.title("NMS Login")
pencere.geometry("1366x768")  # Uygulama boyutu
pencere.configure(bg="#f7f7f7")

# Ana frame
frame = tk.Frame(pencere, bg="#f7f7f7")
frame.pack(expand=True)

# Logo
logo_image = tk.PhotoImage(file="logo.png")  # logo.png dosyasının doğru dizinde olduğundan emin olun
label_logo = tk.Label(frame, image=logo_image, bg="#f7f7f7")
label_logo.pack(pady=(20, 10))

# NMSLogin yazısı
label_nms = tk.Label(frame, text="NMSLogin", font=("Bahnschrift", 24), bg="#f7f7f7")
label_nms.pack(pady=(0, 20))

# Giriş Alanı
frame_giris = tk.Frame(frame, bg="#f7f7f7")
frame_giris.pack(pady=20)

# Giriş formu
tk.Label(frame_giris, text="Kullanıcı Adı:", bg="#f7f7f7", font=("Bahnschrift", 12)).pack()
entry_kullanici_adi = tk.Entry(frame_giris, borderwidth=5, relief="flat")
entry_kullanici_adi.pack(pady=5)

tk.Label(frame_giris, text="Şifre:", bg="#f7f7f7", font=("Bahnschrift", 12)).pack()
entry_sifre = tk.Entry(frame_giris, show='*', borderwidth=5, relief="flat")
entry_sifre.pack(pady=5)

btn_giris = tk.Button(frame_giris, text="Giriş Yap", command=lambda: (buton_animasyon(btn_giris), giris()), bg="#f7f7f7", fg="black", borderwidth=0, font=("Bahnschrift", 12))
btn_giris.pack(pady=10)
btn_giris.bind("<Enter>", on_enter)
btn_giris.bind("<Leave>", on_leave)

btn_kayit_goster = tk.Button(frame_giris, text="Kayıt Ol", command=goster_kayit, bg="#f7f7f7", fg="black", borderwidth=0, font=("Bahnschrift", 12))
btn_kayit_goster.pack(pady=5)
btn_kayit_goster.bind("<Enter>", on_enter)
btn_kayit_goster.bind("<Leave>", on_leave)

# Kayıt Alanı
frame_kayit = tk.Frame(frame, bg="#f7f7f7")

tk.Label(frame_kayit, text="Kullanıcı Adı:", bg="#f7f7f7", font=("Bahnschrift", 12)).pack()
entry_kullanici_adi_kayit = tk.Entry(frame_kayit, borderwidth=5, relief="flat")
entry_kullanici_adi_kayit.pack(pady=5)

tk.Label(frame_kayit, text="Şifre:", bg="#f7f7f7", font=("Bahnschrift", 12)).pack()
entry_sifre_kayit = tk.Entry(frame_kayit, show='*', borderwidth=5, relief="flat")
entry_sifre_kayit.pack(pady=5)

btn_kaydet = tk.Button(frame_kayit, text="Kaydet", command=lambda: (buton_animasyon(btn_kaydet), kaydet()), bg="#f7f7f7", fg="black", borderwidth=0, font=("Bahnschrift", 12))
btn_kaydet.pack(pady=10)
btn_kaydet.bind("<Enter>", on_enter)
btn_kaydet.bind("<Leave>", on_leave)

btn_geri_don = tk.Button(frame_kayit, text="Geri Dön", command=goster_giris, bg="#f7f7f7", fg="black", borderwidth=0, font=("Bahnschrift", 12))
btn_geri_don.pack(pady=5)
btn_geri_don.bind("<Enter>", on_enter)
btn_geri_don.bind("<Leave>", on_leave)

# Başlangıçta giriş formu gösteriliyor
frame_giris.pack(pady=20)

pencere.mainloop()
