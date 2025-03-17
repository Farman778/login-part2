import json
import os
import mogging

# Fayl adları
ius_file = "users.txt"
log_file = "activity_log.txt"
session_file = "session.txt"

# Log faylının konfiqurasiyası
logging.basicConfig(filename=log_file, level=logging.INFO, 
                    format='%(asctime)s - %(message)s')

# İstifadəçi məlumatlarını fayldan yükləmə funksiyası
def load_users():
    if os.path.exists(us_file):
        with open(us_file, "r") as file:
            return json.load(file)
    return {}

# İstifadəçi məlumatlarını fayla yazma funksiyası
def save_users(users):
    with open(us_file, "w") as file:
        json.dump(users, file, indent=4)

# Session yaratma funksiyası
def create_session(username):
    with open(session_file, "w") as file:
        file.write(username)

# Session yoxlama funksiyası
def get_session():
    if os.path.exists(session_file):
        with open(session_file, "r") as file:
            return file.read().strip()
    return None

# Sessionı silmə funksiyası
def clear_session():
    if os.path.exists(session_file):
        os.remove(session_file)

# Login funksiyası
def login(username, password):
    users = load_users()
    if username in users and users[username]["password"] == password:
        role = users[username]["role"]
        logging.info(f"{username} logged in with {role} role.")
        create_session(username)
        print(f"Daxil oldunuz! Sizin rolunuz: {role}")
        return role
    else:
        logging.warning(f"Failed login attempt for {username}.")
        print("İstifadəçi adı və ya şifrə yanlışdır.")
        return None

# İcazə yoxlama funksiyası
def check_access(role, resource):
    if role == "admin":
        print(f"Admin icazəsi ilə {resource} resursuna daxil olundu.")
        logging.info(f"Admin accessed {resource}.")
    elif role == "user":
        if resource == "admin_dashboard":
            print("İcazə rədd edildi: Normal istifadəçi admin panelinə daxil ola bilməz.")
            logging.warning("User tried to access admin_dashboard without permission.")
        else:
            print(f"İstifadəçi {resource} resursuna daxil oldu.")
            logging.info(f"User accessed {resource}.")
    else:
        print("Bilinməyən rol.")
        logging.warning(f"Access attempt with unknown role: {role}")

# Logout funksiyası
def logout():
    user = get_session()
    if user:
        logging.info(f"{user} logged out.")
        clear_session()
        print("Çıxış edildi.")
    else:
        print("Heç bir istifadəçi daxil olmayıb.")

# Əsas proqram axını
users = {"admin": {"password": "admin123", "role": "admin"}, "user1": {"password": "password123", "role": "user"}}
save_users(users)  # Əgər fayl yoxdursa, ilkin istifadəçiləri yazırıq

session_user = get_session()
if session_user:
    print(f"{session_user} artıq daxil olub.")
else:
    username = input("İstifadəçi adını daxil edin: ")
    password = input("Şifrəni daxil edin: ")
    role = login(username, password)
    
    if role:
        resource = input("Giriş etmək istədiyiniz resursu seçin (məsələn, 'user_profile', 'admin_dashboard'): ")
        check_access(role, resource)
        logout()
