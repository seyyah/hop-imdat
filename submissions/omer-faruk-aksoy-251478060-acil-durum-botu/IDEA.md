# S12 - Acil Durum ve İlk Yardım Botu

## 1. Motivasyon ve Felsefe
Acil durumlar (patlama, yangın, yaralanma) dijital ortamda çözülebilen yazılımsal hatalar değil, tamamen fiziksel müdahale gerektiren hayati krizlerdir. Bu projede, yapay zekanın "çözücü" değil "hızlı bir yönlendirici" olması gerektiği fikrinden yola çıkılmıştır. 

Projenin mimarisi **HireAHuman.ai** felsefesine dayanmaktadır. Yapay zeka fiziksel bir kargo taşıyamayacağı veya bir hastaya kalp masajı yapamayacağı gibi, acil durumlarda şahsen orada bulunamaz. Bu nedenle sistem; sıradan durumlarda yapay zekanın hızını ve bilgi süzme kapasitesini kullanırken (HOOTL), can güvenliğinin söz konusu olduğu fiziksel kriz anlarında inisiyatifi otomatik olarak gerçek bir insan operatöre (HOTL) devreder.

## 2. Kapsam
Sistem iki farklı kullanıcı arayüzü ve bir ortak veri kuyruğu üzerinden çalışır:
* **Kullanıcı Botu (`bot.py`):** Kullanıcıyla etkileşime giren, basit durumlara cevap veren ve risk anında çağrıyı yönlendiren yüz.
* **Operatör Terminali (`operator.py`):** Botun risk bulup kuyruğa yazdığı çağrıları eşzamanlı olarak ekrana basan arka plan servisi.
* **Veri Yönetimi:** `bilgi.txt` (Tavsiye veritabanı) ve `kuyruk.txt` (Bot ve operatör arası iletişim köprüsü). Dış kütüphane veya veritabanı kullanılmadan saf metin dosyası operasyonları ile veri akışı sağlanmıştır.

## 3. Başarı Kriterleri (Success Criteria)
1.  **Doğru Filtreleme:** "Tava alev aldı" gibi müdahale edilebilir olaylarda botun kendi başına doğru cevabı `bilgi.txt` üzerinden bulması ve operatörü meşgul etmemesi.
2.  **Otomatik İnisiyatif (HOTL Tetiklemesi):** Kullanıcı panik halinde "patlama", "yaralı" gibi kırmızı alarm kelimeleri girdiğinde, botun soru sormayı veya tavsiye vermeyi kesip doğrudan `kuyruk.txt` dosyasına yazması.
3.  **İzole Haberleşme:** `operator.py` dosyasının `bot.py` işleyişini kilitlemeden, kuyruktaki mesajları eşzamanlı olarak operatör ekranına düşürmesi.
4.  **Fallback (Güvenlik Ağı):** Sistemde tanımlı olmayan bir girdi (örn: "kedi ağaçta kaldı") geldiğinde botun yanlış yönlendirme yapmak yerine "Anlayamadım" yanıtını vermesi.
