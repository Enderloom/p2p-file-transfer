# Server və Müştəri Tətbiqi

Bu layihə, server və müştəri tətbiqləri ilə faylları yükləmək, siyahıya salmaq və endirmək üçün istifadə edilə bilər. Tətbiqlər Azərbaycan dilində interfeys təqdim edir.

## Əsas Tələblər

- Python 3.7 və ya daha yüksək versiya
- İnternet bağlantısı (serverə qoşulmaq üçün)

## Quraşdırma

1. **Depoları klonlayın və ya faylları yükləyin:**

   Terminalda və ya Komanda Satırında:

   ```bash
   git clone <repo_url>
   cd <repo_folder>
   ```

2. **Tələb olunan kitabxanaları quraşdırın:**

   Əgər `requirements.txt` faylınız varsa, aşağıdakı əmr ilə kitabxanaları quraşdırın:

   ```bash
   pip install -r requirements.txt
   ```

3. **Tələb olunan kitabxanaları əl ilə quraşdırmaq istəyirsinizsə:**

   ```bash
   pip install flask requests tqdm
   ```

## Tətbiqdən İstifadə

### Server Tərəfi

1. `server.py` faylını işə salmaq üçün aşağıdakı əmrdən istifadə edin:

   ```bash
   python server.py
   ```

2. Terminalda serverin IP ünvanını və portunu (adətən `8080`) görə bilərsiniz.

3. Server avtomatik olaraq 10 dəqiqədən uzun müddət saxlanılan faylları silir.

### Müştəri Tərəfi

1. `client.py` faylını işə salmaq üçün:

   ```bash
   python client.py
   ```

2. İlk olaraq serverin IP ünvanını daxil edin.

3. Müştəridə istifadə edə biləcəyiniz komandalar:
   - **`list`**: Serverdə saxlanılan bütün faylları siyahıya alır.
   - **`download <nömrə>`**: Siyahıdan faylı endirir və kompüterinizdə bir yer seçməyiniz üçün pəncərə açılır.
   - **`upload`**: Fayl yükləmək üçün pəncərə açır və fayl seçməyinizə imkan verir.
   - **`help`**: Bütün mövcud komandaları göstərir.

### Fayl Siyahısını Göstərmək

Komanda:
```bash
list
```

### Fayl Yükləmək

Komanda:
```bash
upload
```

### Fayl Endirmək

Komanda:
```bash
download <nömrə>
```

Misal:
```bash
download 1
```

---

## Layihə haqqında

Bu layihə Python istifadəçilərinə faylların idarə edilməsi və server/müştəri konsepsiyasını öyrənmək üçün əla bir nümunədir.

--- 

Uğurlar! 😊