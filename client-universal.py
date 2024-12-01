import requests
import os
from tkinter import filedialog, Tk
from tqdm import tqdm

# Komandaları Azərbaycan dilində göstərir
def show_help():
    print("Əmrlər:")
    print("list - Serverdə olan faylları göstər")
    print("download <nömrə> - Seçilmiş faylı yüklə")
    print("upload - Faylı serverə yüklə")
    print("help - Komanda siyahısını göstər")

# Fayl yükləmə
def download_file(base_url, filename):
    url = f"{base_url}/download/{filename}"
    response = requests.get(url, stream=True)
    save_path = filedialog.asksaveasfilename(initialfile=filename)
    if not save_path:
        print("Yükləmə ləğv edildi.")
        return
    total_size = int(response.headers.get('content-length', 0))
    with open(save_path, 'wb') as file, tqdm(
        desc=f"{filename} yüklənir",
        total=total_size,
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in response.iter_content(chunk_size=1024):
            file.write(data)
            bar.update(len(data))
    print("Yükləmə tamamlandı.")

# Fayl yükləmə serverə
def upload_file(base_url):
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    if not file_path:
        print("Yükləmə ləğv edildi.")
        return
    file_name = os.path.basename(file_path)
    url = f"{base_url}/upload"
    with open(file_path, 'rb') as file, tqdm(
        desc=f"{file_name} yüklənir",
        total=os.path.getsize(file_path),
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        response = requests.post(url, files={"file": file})
        bar.update(os.path.getsize(file_path))
    if response.status_code == 200:
        print("Fayl uğurla yükləndi.")
    else:
        print("Yükləmə uğursuz oldu.")

# Əsas funksional
def main():
    server_ip = input("Serverin IP adresini daxil edin: ")
    base_url = f"http://{server_ip}:8080"
    while True:
        command = input("Komanda daxil edin (help kömək üçün): ").strip()
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
                    download_file(base_url, files[file_number - 1])
                else:
                    print("Seçilmiş nömrə mövcud deyil.")
            except (ValueError, IndexError):
                print("Komanda düzgün deyil. Misal: download 1")
        elif command == "upload":
            upload_file(base_url)
        else:
            print("Bilinməyən komanda. 'help' yazaraq komandaları görə bilərsiniz.")

if __name__ == "__main__":
    main()
