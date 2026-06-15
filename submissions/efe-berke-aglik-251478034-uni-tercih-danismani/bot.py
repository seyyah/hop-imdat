import socket
import json
import os
from functools import lru_cache

# Veri dosyaları yolları
BILGI_DOSYASI = "bilgi.json"
ONBELLEK_DOSYASI = "onbellek.json"

# JSON dosyalarını okuma fonksiyonu
def json_oku(dosya_yolu):
    if not os.path.exists(dosya_yolu):
        return {}
    try:
        with open(dosya_yolu, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}

# JSON dosyalarına yazma fonksiyonu
def json_yaz(dosya_yolu, veri):
    try:
        with open(dosya_yolu, "w", encoding="utf-8") as f:
            json.dump(veri, f, ensure_ascii=False, indent=4)
    except IOError as e:
        print(f"Dosya yazma hatası: {e}")

# Verileri yükle
data = json_oku(BILGI_DOSYASI)
mesaj_onbellek = json_oku(ONBELLEK_DOSYASI)

# Levenshtein Mesafe Algoritması (lru_cache ile memoized — O(m×n))
@lru_cache(maxsize=None)
def levenshtein_mesafesi(mesaj, anahtar):
    if not mesaj: return len(anahtar)
    if not anahtar: return len(mesaj)
    if mesaj[0] == anahtar[0]:
        return levenshtein_mesafesi(mesaj[1:], anahtar[1:])
    return 1 + min(
        levenshtein_mesafesi(mesaj[1:], anahtar),    # silme
        levenshtein_mesafesi(mesaj, anahtar[1:]),    # ekleme
        levenshtein_mesafesi(mesaj[1:], anahtar[1:]) # değiştirme
    )

# Verilen mesaja en yakın data anahtarını ve Levenshtein mesafesini döndürür
def en_yakin_anahtari_bul(mesaj, anahtarlar):
    en_yakin, minimum = None, 999
    for anahtar in anahtarlar:
        mesafe = levenshtein_mesafesi(mesaj, anahtar)
        if mesafe < minimum:
            minimum = mesafe
            en_yakin = anahtar
    return en_yakin, minimum

# Bottan (istemci) uzmana (sunucu) mesajı ilet ve yanıtı al
def uzman_bot_iletisim(mesaj):
    talep = f"[BOT] Öğrenciden gelen '{mesaj}' mesajı için cevap vermem uygun olmaz. Nasıl yanıt vermeliyim?"
    client_socket.sendall(talep.encode('utf-8'))  # Bot talebini istemciden sunucuya gönder
    yanit = client_socket.recv(1024)  # Sunucudan gelen yanıtı al
    if yanit:
        yanit_str = yanit.decode('utf-8')
        mesaj_onbellek[mesaj] = yanit_str  # Hafızada güncelle
        json_yaz(ONBELLEK_DOSYASI, mesaj_onbellek)  # Kalıcı belleğe kaydet (onbellek.json)
        return yanit_str
    return None

# Uzmandan (sunucudan) alınan yanıtın mantıksal kontrolleri
def yanit_kontrol(mesaj):
    yanit_str = uzman_bot_iletisim(mesaj)
    if yanit_str:
        print(f"[UZMAN GÖRÜŞÜ]: {yanit_str}")
    else:
        print(f"Bot: Şu an için isteğinizi yerine getiremiyorum.")

# Socket oluşturma
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Sunucuya bağlanma
client_socket.connect(('localhost', 65435))

# Ana döngü
try:
    while True:
        minimum = 999
        mesaj = input("Öğrenci: ").lower()
        mevcut_anahtar, minimum = en_yakin_anahtari_bul(mesaj, data.keys())
        if mesaj_onbellek.get(mesaj):  # Mesaj önceden kaydedilmiş mi kontrol et
            print(f"Bot: {mesaj_onbellek[mesaj]}")
        elif minimum == 0:
            print(f"Bot: {data[mevcut_anahtar]}")
        elif minimum <= 3:
            while True:
                onay = input(f"Bot: Bunu mu demek istediniz '{mevcut_anahtar}'? [E/H]: ")
                if onay.lower() in ["e", "evet"]:
                    print(f"Bot: {data[mevcut_anahtar]}")
                    break
                elif onay.lower() in ["h", "hayır"]:
                    yanit_kontrol(mesaj)  # Öğrenci 'hayır' derse mesajı uzmana ilet
                    break
                else:
                    print(f"Bot: Size yardımcı olabilmem için lütfen doğru şekilde yanıtlayın.")
        else:
            yanit_kontrol(mesaj)
except KeyboardInterrupt:
    print("\nBağlantı kapatılıyor...")
finally:
    client_socket.close()

    

