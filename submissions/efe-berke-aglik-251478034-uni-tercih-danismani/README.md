# Üniversite Tercih Danışmanı Botu

> ⚠️ Bu proje gerçek bir ürün değildir. İnsan-Makine Döngüsü (Human-in-the-Loop) kavramını ve otomasyon seviyelerini pratik olarak incelemek amacıyla hazırlanmış **akademik bir araştırma çalışmasıdır.**

---

## Amaç

Bu çalışma, bir chatbot sisteminde **insanın karar sürecine ne ölçüde dahil edilmesi gerektiği** sorusunu araştırmaktadır. Sistem, otomatik eşleştirme ile uzman müdahalesini tek bir akışta birleştirerek üniversite tercih danışmanlığı senaryosu üzerinden somutlaştırılmıştır.

---

## Nasıl Çalışır?

Sistem iki ana bileşen ve iki veri dosyasından oluşur:

- **`bot.py`** — Öğrenciyle diyalog kuran bileşen. `bilgi.json` dosyasındaki anahtar–yanıt eşleşmelerini ve Levenshtein mesafe algoritmasını kullanarak girilen mesajlara en yakın yanıtı üretir. Eşleşme bulunamazsa uzmana sorar ve yanıtı `onbellek.json` dosyasına kaydederek kalıcı olarak önbelleğe alır.
- **`expert.py`** — Uzman paneli. Botun yanıt üretemediği mesajlar için uzmanın görüşünü alır ve socket üzerinden bota iletir.

`bot.py` ile `expert.py` arasındaki iletişim **TCP socket** (varsayılan port: `65435`) üzerinden gerçekleşir.

Botun bilgi tabanı (`bilgi.json`) JSON formatında, `"anahtar": "yanıt"` eşleşmeleri içerir. Levenshtein mesafesi sıfır ise kesin eşleşme, 3 veya altında ise "Bunu mu demek istediniz?" öneri akışı, daha yüksekse uzman yönlendirmesi devreye girer.

---


## Çalıştırma

```bash
# Önce expert.py'yi ayrı bir terminalde başlatın
python expert.py

# Ardından bot.py'yi başlatın
python bot.py
```

`bot.py` başlatıldığında `expert.py`'nin zaten çalışıyor ve bağlantı bekliyor olması gerekir.

---

## Dosya Yapısı

```
AI-Human-Decision-Bot-Example/
├── bot.py          # Ana bot mantığı: Levenshtein eşleştirme + socket istemcisi + JSON yönetimi
├── expert.py       # Uzman paneli: socket sunucusu
├── bilgi.json      # Anahtar-yanıt bilgi tabanı (JSON formatında)
├── onbellek.json   # Uzmandan öğrenilen yanıtların kalıcı önbelleği (JSON formatında)
├── SPEC.md         # Sistem spesifikasyonu
├── rapor.pdf       # Araştırma raporu
├── README.md
└── arastirma/      # Referans ekran görüntüleri
    ├── humworkai_mainpage.png
    ├── hireahuman_launch_linkedin.png
    └── hireahuman_maintenance.png
```

---

## Performans

Levenshtein mesafe fonksiyonu saf özyineleme ile implement edildiğinde **O(3ⁿ)** üstel zaman karmaşıklığına sahipti: aynı `(mesaj[i:], anahtar[j:])` alt sorunları defalarca yeniden hesaplanıyordu.

`functools.lru_cache` dekoratörü eklenerek her `(mesaj, anahtar)` çifti **yalnızca bir kez** hesaplanıp önbelleğe alınır. Bu sayede karmaşıklık **O(m × n)** düzeyine iner (m ve n, karşılaştırılan stringlerin uzunlukları).

| Durum | Zaman Karmaşıklığı |
|---|---|
| Memoization yok (saf özyineleme) | O(3ⁿ) |
| `lru_cache` ile memoized | O(m × n) |

---

## Kısıtlamalar

Bu proje kavramsal düzeyde bir prototiptir; üretim ortamı için tasarlanmamıştır:

- Bilgi tabanı statik ve sınırlıdır; gerçek bir NLP/LLM motoru içermez.
- Levenshtein algoritması özyinelemeli olarak implement edilmiştir; `functools.lru_cache` ile memoize edildiğinden tekrarlanan alt sorunlar önbellekten döndürülür (bkz. **Performans** bölümü).
- Süreçler arası iletişim socket tabanlıdır; hata yönetimi ve güvenlik katmanları minimumda tutulmuştur.

