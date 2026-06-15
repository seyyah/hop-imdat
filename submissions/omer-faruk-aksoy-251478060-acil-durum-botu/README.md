# S12 - Acil Durum ve İlk Yardım Botu

## 📌 Proje Hakkında
Bu proje, acil durumlarda kullanıcılara ilk yardım tavsiyeleri veren ve hayati risk algıladığında inisiyatifi alarak çağrıyı anında gerçek bir insan operatöre aktaran melez (Yapay Zeka + İnsan) bir sistemidir. Temel motivasyonunu **HireAHuman.ai** platformunun "fiziksel dünyada insanın gerekliliği" felsefesinden almaktadır.

## ⚙️ Özellikler ve Çalışma Mantığı
Sistem, risk durumuna göre iki farklı modda çalışır:
* **HOOTL (Sadece Bot):** "Gaz kokusu" veya "alev alan tava" gibi müdahale edilebilir durumlarda bot, veri tabanından (`bilgi.txt`) doğru tavsiyeyi bularak kullanıcıyı hızlıca yönlendirir.
* **HOTL (İnsana Havale):** "Patlama", "yaralı" gibi kırmızı alarm durumlarında bot anında susar ve inisiyatifi insan operatöre devreder.

Mevcut mimaride (v1) `bot.py` ve `operator.py` dosyaları birbirleriyle izole bir şekilde çalışır ve haberleşme köprüsü olarak `kuyruk.txt` dosyası kullanılır.
