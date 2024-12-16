import requests
import os
import stat
import sys
from tkinter import filedialog, Tk
from tqdm import tqdm
from cryptography.fernet import Fernet
import io

KEY_FILE = 'key.key'

def secure_key_file(path):
    """
    Set file permissions to restrict access.
    On Unix-like systems: chmod 600 (owner read/write only).
    On Windows: Attempt chmod (may not fully restrict access) and print a warning.
    """
    if os.name == 'nt':
        # Windows environment
        # os.chmod in Windows doesn't fully enforce Unix-like permissions.
        # We'll set read/write for owner only, and remove other permissions if possible.
        # Note: This doesn't guarantee security on Windows. For real security, set ACLs.
        try:
            os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)
            print("Diqqət: Windows-da fayl icazələri tam etibarlı deyil. "
                  "Daha güclü təhlükəsizlik üçün ACL-lərdən istifadə edin.")
        except Exception as e:
            print("Windows-da icazə dəyişdirilməsi uğursuz oldu:", e)
            print("Faylın təhlükəsizliyini təmin etmək üçün əlavə tədbirlər görün.")
    else:
        # Unix-like system
        os.chmod(path, 0o600)

def load_or_create_key():
    # If a key file doesn't exist, generate one and save it.
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, 'wb') as kf:
            kf.write(key)
        print("Yeni şifrə açarı yaradıldı və 'key.key' faylında saxlanıldı.")
        # Change file permissions to restrict access
        secure_key_file(KEY_FILE)
    else:
        print("'key.key' faylı mövcuddur, açar yüklənir.")
        # Ensure the permissions are secure even if file exists
        secure_key_file(KEY_FILE)
    
    # Load the key from file
    with open(KEY_FILE, 'rb') as kf:
        key = kf.read()
    return Fernet(key)

def show_help():
    print("Əmrlər:")
    print("list - Serverdə olan faylları göstər")
    print("download <nömrə> - Seçilmiş faylı yüklə və deşifrə et")
    print("upload - Faylı şifrləyib serverə yüklə")
    print("help - Komanda siyahısını göstər")
    print("exit - Çıxış")

# Fayl yükləmə və deşifrə
def download_file(base_url, filename, fernet):
    url = f"{base_url}/download/{filename}"
    response = requests.get(url, stream=True)
    if response.status_code != 200:
        print("Fayl yüklənmədi. Server xətası və ya fayl mövcud deyil.")
        return

    # Faylın harada saxlanacağını seçirik
    save_path = filedialog.asksaveasfilename(initialfile=filename)
    if not save_path:
        print("Yükləmə ləğv edildi.")
        return

    # Şifrələnmiş verini yadda saxlayırıq
    encrypted_data = bytearray()
    total_size = int(response.headers.get('content-length', 0))

    with tqdm(
        desc=f"{filename} yüklənir (şifrəli)",
        total=total_size,
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for chunk in response.iter_content(chunk_size=1024):
            encrypted_data.extend(chunk)
            bar.update(len(chunk))

    # Faylı deşifrə edirik
    try:
        decrypted_data = fernet.decrypt(bytes(encrypted_data))
    except Exception as e:
        print("Deşifrə mümkün olmadı:", e)
        return

    # Deşifrə olunmuş faylı saxlayırıq
    with open(save_path, 'wb') as file:
        file.write(decrypted_data)

    print("Yükləmə və deşifrə tamamlandı.")

# Fayl şifrələyib serverə yükləmə
def upload_file(base_url, fernet):
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    if not file_path:
        print("Yükləmə ləğv edildi.")
        return
    file_name = os.path.basename(file_path)

    # Faylı oxuyub şifrələyirik
    with open(file_path, 'rb') as f:
        original_data = f.read()
    encrypted_data = fernet.encrypt(original_data)

    url = f"{base_url}/upload"

    # Şifrələnmiş fayl məlumatlarını yaddaşda saxlayırıq
    encrypted_file = io.BytesIO(encrypted_data)
    encrypted_file.name = file_name

    total_size = len(encrypted_data)
    with tqdm(
        desc=f"{file_name} yüklənir (şifrəli)",
        total=total_size,
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        response = requests.post(url, files={"file": (file_name, encrypted_file)})
        bar.update(total_size)

    if response.status_code == 200:
        print("Fayl uğurla (şifrəli şəkildə) yükləndi.")
    else:
        print("Yükləmə uğursuz oldu.")

def main():
    # Yüklə və ya yarat açarı
    fernet = load_or_create_key()

    server_ip = input("Serverin IP adresini daxil edin: ")
    base_url = f"http://{server_ip}:8080"

    while True:
        command = input("Komanda daxil edin (help kömək üçün): ").strip().lower()
        if command == "help":
            show_help()
        elif command == "list":
            response = requests.get(f"{base_url}/list")
            if response.status_code == 200:
                files = response.json().get("files", [])
                if files:
                    for i, file in enumerate(files, start=1):
                        print(f"{i}. {file}")
                else:
                    print("Serverdə heç bir fayl yoxdur.")
            else:
                print("Fayl siyahısını yükləmək mümkün olmadı.")
        elif command.startswith("download"):
            try:
                _, file_number = command.split()
                file_number = int(file_number)
                response = requests.get(f"{base_url}/list")
                files = response.json().get("files", [])
                if 1 <= file_number <= len(files):
                    download_file(base_url, files[file_number - 1], fernet)
                else:
                    print("Seçilmiş nömrə mövcud deyil.")
            except (ValueError, IndexError):
                print("Komanda düzgün deyil. Misal: download 1")
        elif command == "upload":
            upload_file(base_url, fernet)
        elif command == "exit":
            print("Çıxış edilir...")
            break
        else:
            print("Bilinməyən komanda. 'help' yazaraq komandaları görə bilərsiniz.")

if __name__ == "__main__":
    main()
