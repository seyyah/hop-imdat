import socket

# Socket oluşturma
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# IP ve Port bağlama
server_socket.bind(('localhost', 65435))

# Dinlemeye başlama
server_socket.listen()
print("Sunucu dinlemede... Bağlantı bekleniyor.")

# Bağlantıyı kabul etme
conn, addr = server_socket.accept()
print(f"Bağlantı kuruldu: {addr}")

with conn:
    while True:
        gelen_mesaj = conn.recv(1024) # 1024 byte'lık veri oku
        if not gelen_mesaj:
            break
        print(gelen_mesaj.decode('utf-8'))
        yanit = input("[Öneri]: ")
        conn.sendall(yanit.encode('utf-8'))  # Uzman önerisini sunucudan istemciye gönder
        print("Yanıtınız iletildi.")