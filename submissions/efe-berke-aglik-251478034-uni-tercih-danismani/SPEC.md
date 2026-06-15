# Üniversite Tercih Danışmanı

Öğrenci sınav sonucunu, hedeflerini, ilgi alanlarını, bulunduğu şehri ve benzer bilgileri bota yazar; bot ise girdiyi `bilgi.json` dosyasındaki anahtarlarla Levenshtein mesafe algoritması kullanarak eşleyip en uygun cevabı verir. Eşleşme bulunamazsa `expert.py` üzerinden uzman danışmandan görüş alır.

## Hedef Kitle

Hedef kitle, üniversite adayı öğrencilerdir. Bu öğrenciler, üniversite sınavı sonuçlarının açıklanmasının ardından isteklerine en uygun ve doğru tercih listesini elde edebilmek için bu botu kullanır.

## Çalışma Mantığı

Sistem tek bir çalıştırmayla yürütülür; ayrı mod argümanı gerekmez.

Bot, öğrenciden gelen her girdiyi `bilgi.json` dosyasındaki anahtarlarla Levenshtein mesafe algoritması aracılığıyla karşılaştırır:

- **Mesafe = 0** → Kesin eşleşme; karşılık gelen yanıt doğrudan verilir.
- **Mesafe ≤ 3** → Yakın eşleşme; "Bunu mu demek istediniz?" öneri akışı devreye girer.
- **Mesafe > 3** → Eşleşme yok; talep TCP socket (varsayılan port: `65435`) aracılığıyla `expert.py`'ye iletilir. Uzman `[Öneri]:` satırına yanıtını girer, yanıt bota döner ve `onbellek.json` dosyasına kaydedilerek önbelleğe alınır. Aynı mesaj tekrar geldiğinde uzmana sorulmadan önbellekteki yanıt kullanılır.

## Performans

`levenshtein_mesafesi` fonksiyonu saf özyinelemeli olarak yazıldığında her çağrı üç alt çağrı açar; aynı `(mesaj[i:], anahtar[j:])` alt sorunları tekrar tekrar hesaplanır.

`functools.lru_cache(maxsize=None)` dekoratörü ile her `(mesaj, anahtar)` string çifti yalnızca bir kez hesaplanır ve önbelleğe alınır:

| Durum | Zaman Karmaşıklığı |
|---|---|
| Memoization yok (saf özyineleme) | O(3ⁿ) |
| `lru_cache` ile memoized | O(m × n) |

`lru_cache` yalnızca hashable tipler üzerinde çalışır; Python stringleri immutable ve hashable olduğundan bu kullanım için doğal uyumludur.
