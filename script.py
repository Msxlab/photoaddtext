import os
import random
import datetime
from PIL import Image, ImageDraw, ImageFont

# ==============================
#  AYARLAR
# ==============================
base_dir = r"C:\Users\United\Desktop\Category\Whatsapp"

logo_dosyasi = "logo.png"            # Sol alt köşeye eklenecek logo
font_dosyasi = "Audiowide-Regular.ttf"  # Metin fontu
font_boyutu = 36                     # Metin boyutu

# 18 adet şehir (Kitchen klasörleri 36 tane, bu listeyi döngüsel kullanıyoruz)
sehir_listesi = [
    "Millburn",
    "Saddle River",
    "Somerset",
    "Somerville",
    "Monmouth Beach Borough",
    "Essex Fells",
    "Spring Lake",
    "BernardsVille",
    "Mendham",
    "Warren",
    "Livingston",
    "Hillsborough",
    "Branchburg",
    "hopewell",
    "Hoboken",
    "Basking Ridge",
    "Somervile",
    "Hillsborough"  # 18. şehir
]

# Logo / metin konum ve ölçek ayarları
logo_oran = 0.2       # Resmin genişliğine göre logo %20 ölçek
logo_margin = 10      # Logonun sol-alt kenar boşluğu
yazi_margin = 20      # Metnin sağ-alt kenar boşluğu

# Rastgele üretilecek tarihler için aralık
start_date = datetime.date(2020, 1, 1)
end_date = datetime.date(2024, 12, 12)

# Kitchen klasör sayısı
klasor_sayisi = 36

# ==============================
#  LOGO YÜKLE
# ==============================
try:
    logo = Image.open(logo_dosyasi).convert("RGBA")
    logo_w, logo_h = logo.size
except FileNotFoundError:
    print(f"Logo dosyası '{logo_dosyasi}' bulunamadı. Kod durduruluyor.")
    exit(1)

# ==============================
#  36 ADET RASTGELE TARİH ÜRET VE SIRALA
# ==============================
delta = end_date - start_date
gun_farki = delta.days

random_dates = []
for _ in range(klasor_sayisi):
    rastgele_gun = random.randrange(gun_farki + 1)
    rastgele_tarih = start_date + datetime.timedelta(days=rastgele_gun)
    random_dates.append(rastgele_tarih)

# Artan sırada sıralıyoruz: Kitchen 1 en erken, Kitchen 36 en geç
random_dates.sort()

# ==============================
#  ANA DÖNGÜ: KITCHEN 1 -> KITCHEN 36
# ==============================
for i in range(1, klasor_sayisi + 1):
    # Şehir seçimi (18 şehir -> 36 klasör, mod alarak tekrar)
    sehir = sehir_listesi[(i - 1) % len(sehir_listesi)]

    # Sıradaki tarih (sıralanmış listedeki i-1 indeksli)
    secilen_tarih = random_dates[i - 1]

    # Tarih formatı: Ay/Gün/Yıl (MM/DD/YYYY)
    tarih_str = secilen_tarih.strftime("%m/%d/%Y")

    # Resmin sağ altına yazılacak metin
    metin = f"{sehir}, {tarih_str}"

    # Kitchen klasörü (örneğin: "Kitchen 1", "Kitchen 2" ...)
    folder_name = f"Kitchen {i}"
    foto_klasoru = os.path.join(base_dir, folder_name)

    # Klasör yoksa atla
    if not os.path.isdir(foto_klasoru):
        print(f"{folder_name} klasörü bulunamadı, geçiliyor...")
        continue

    # İşlenmiş çıktıları kaydedeceğimiz klasör: "islenmis/Kitchen 1" vb.
    cikti_klasoru = os.path.join(base_dir, "islenmis", folder_name)
    os.makedirs(cikti_klasoru, exist_ok=True)

    print(f"\n=== {folder_name} klasörü işleniyor... ===")

    # Fotoğraf sayacı (SEO dosya adı için)
    foto_sayaci = 1

    # Klasördeki fotoğrafları al
    for dosya in os.listdir(foto_klasoru):
        if dosya.lower().endswith(('.png', '.jpg', '.jpeg')):
            foto_path = os.path.join(foto_klasoru, dosya)

            try:
                img = Image.open(foto_path).convert("RGBA")
            except Exception as e:
                print(f"'{dosya}' dosyası açılamadı ({e}), geçiliyor...")
                continue

            w, h = img.size

            # ==============================
            # LOGO EKLEME (SOL ALT)
            # ==============================
            yeni_logo_w = int(w * logo_oran)
            yeni_logo_h = int(yeni_logo_w * (logo_h / logo_w))
            logo_kucuk = logo.resize((yeni_logo_w, yeni_logo_h), Image.LANCZOS)

            logo_x = logo_margin
            logo_y = h - logo_kucuk.size[1] - logo_margin
            img.paste(logo_kucuk, (logo_x, logo_y), logo_kucuk)

            # ==============================
            # METİN EKLEME (SAĞ ALT)
            # ==============================
            draw = ImageDraw.Draw(img)
            try:
                font = ImageFont.truetype(font_dosyasi, font_boyutu)
            except:
                font = ImageFont.load_default()

            # Metnin boyutunu ölç
            x0, y0, x1, y1 = draw.textbbox((0, 0), metin, font=font)
            text_w, text_h = x1 - x0, y1 - y0

            text_x = w - text_w - yazi_margin
            text_y = h - text_h - yazi_margin

            draw.text((text_x, text_y), metin, fill="white", font=font)

            # ==============================
            # DOSYA ADINI SEO UYUMLU HALE GETİRME
            # ==============================
            # Şehir adını küçük harf ve boşlukları '-' ile değiştirmek
            sehir_slug = sehir.lower().replace(' ', '-')
            # Tarihi yyyymmdd formatına dönüştürelim
            tarih_yyyymmdd = secilen_tarih.strftime("%Y%m%d")

            # Örnek dosya adı formatı:
            # "somerset-kitchen-1-20231208-001.jpg"
            yeni_dosya_adi = f"{sehir_slug}-kitchen-{i}-{tarih_yyyymmdd}-{foto_sayaci:03d}.jpg"

            kayit_yolu = os.path.join(cikti_klasoru, yeni_dosya_adi)

            # RGBA -> RGB kaydet
            img.convert("RGB").save(kayit_yolu)

            print(f"{dosya} -> {yeni_dosya_adi}")

            foto_sayaci += 1

    print(f"=== {folder_name} klasörü işlemi tamamlandı. ===")

print("\nTüm klasörlerin işlemi sıralı tarihlerle ve SEO uyumlu dosya adlarıyla tamamlandı!")
