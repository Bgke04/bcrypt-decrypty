import bcrypt
import threading

# Hash yang ingin di-brute force
hash_bcrypt = input("Bcrypt : ")
found = False
lock = threading.Lock()

# Fungsi untuk mengecek satu password
def check_password(password):
    global found
    if found:
        return  # Jika sudah ditemukan, hentikan semua thread lain
    password = password.strip().encode('utf-8')
    
    if bcrypt.checkpw(password, hash_bcrypt.encode('utf-8')):
        with lock:
            if not found:
                found = True
                print(f"[+] Password ditemukan: {password.decode()}")
    else:
        print(f"[-] Password gagal: {password.decode()}")

# Fungsi untuk brute-force menggunakan wordlist
def brute_force_bcrypt(passwords):
    threads = []
    for i in range(50):
        if len(passwords) == 0:
            break
        t = threading.Thread(target=check_password, args=(passwords.pop(0),))
        t.start()
        threads.append(t)

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    with open('pw2.txt', 'r') as wordlist:
        passwords = wordlist.readlines()

    while passwords and not found:
        brute_force_bcrypt(passwords)
