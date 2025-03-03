import os
import datetime
from PIL import Image, ImageDraw, ImageFont

def main():
    # ==============================
    # KULLANICIDAN VERİ AL
    # ==============================
    base_dir = input("Fotoğrafların bulunduğu ANA DİZİN yolunu girin (örnek: C:\\Users\\United\\Desktop\\Category\\Whatsapp): ").strip()
    output_dir = input("İşlenmiş fotoğrafların kaydedileceği ÇIKIŞ DİZİN yolunu girin (örnek: D:\\sonuc): ").strip()
    adres = input("Fotoğrafın üzerine yazılacak ADRES bilgisini girin (örnek: Somerset): ").strip()
    tarih_str = input("Fotoğrafın üzerine yazılacak TARİH bilgisini girin (örnek: 01/01/2023): ").strip()

    # ==============================
    # SABİT / ÖN TANIMLI AYARLAR
    # ==============================
    logo_dosyasi = "logo.png"               # Sol alt köşeye eklenecek logo dosyası
    font_dosyasi = "Audiowide-Regular.ttf"  # Metin fontu
    font_boyutu = 36                        # Metin boyutu

    logo_oran = 0.2       # Logonun resmin genişliğine göre kaplayacağı oran (örn: %20)
    logo_margin = 10      # Logonun resmin sol-altından kenar boşluğu
    yazi_margin = 20      # Metnin resmin sağ-altından kenar boşluğu

    # ==============================
    # LOGOYU YÜKLE
    # ==============================
    try:
        logo = Image.open(logo_dosyasi).convert("RGBA")
        logo_w, logo_h = logo.size
    except FileNotFoundError:
        print(f"HATA: Logo dosyası '{logo_dosyasi}' bulunamadı. Uygulama sonlandırılıyor.")
        return

    # ==============================
    # ÇIKIŞ KLASÖRÜNÜ HAZIRLA
    # ==============================
    # İşlenmiş görüntüleri 'islenmis' adlı bir alt klasöre kaydediyoruz
    cikti_klasoru = os.path.join(output_dir, "islenmis")
    os.makedirs(cikti_klasoru, exist_ok=True)

    # ==============================
    # FOTOĞRAFLARI İŞLE
    # ==============================
    print(f"\nKaynak klasör: {base_dir}")
    print(f"Çıkış klasörü: {cikti_klasoru}")
    print(f"Adres: {adres}, Tarih: {tarih_str}\n")

    # Sayaç - SEO uyumlu isimlendirme için
    foto_sayaci = 1

    # Klasördeki dosyaları tara
    for dosya in os.listdir(base_dir):
        # Sadece resim formatları
        if dosya.lower().endswith(('.png', '.jpg', '.jpeg')):
            foto_path = os.path.join(base_dir, dosya)

            try:
                img = Image.open(foto_path).convert("RGBA")
            except Exception as e:
                print(f"{dosya} açılamadı ({e}), geçiliyor...")
                continue

            w, h = img.size

            # ==============================
            # LOGO EKLE (SOL ALT)
            # ==============================
            yeni_logo_w = int(w * logo_oran)
            yeni_logo_h = int(yeni_logo_w * (logo_h / logo_w))
            logo_kucuk = logo.resize((yeni_logo_w, yeni_logo_h), Image.LANCZOS)

            logo_x = logo_margin
            logo_y = h - logo_kucuk.size[1] - logo_margin
            img.paste(logo_kucuk, (logo_x, logo_y), logo_kucuk)

            # ==============================
            # METİN EKLE (SAĞ ALT)
            # ==============================
            # Yazılacak tam metin: "Adres, Tarih"
            metin = f"{adres}, {tarih_str}"
            draw = ImageDraw.Draw(img)

            try:
                font = ImageFont.truetype(font_dosyasi, font_boyutu)
            except:
                font = ImageFont.load_default()

            x0, y0, x1, y1 = draw.textbbox((0, 0), metin, font=font)
            text_w, text_h = x1 - x0, y1 - y0

            text_x = w - text_w - yazi_margin
            text_y = h - text_h - yazi_margin
            draw.text((text_x, text_y), metin, fill="white", font=font)

            # ==============================
            # DOSYA ADI SEO UYUMLU YAP
            # ==============================
            # Adresi, küçük harfe çevirip boşluk yerine tire koyalım
            adres_slug = adres.strip().lower().replace(' ', '-')

            # Örn: "somerset-001.jpg"
            yeni_dosya_adi = f"{adres_slug}-{foto_sayaci:03d}.jpg"

            kayit_yolu = os.path.join(cikti_klasoru, yeni_dosya_adi)
            img.convert("RGB").save(kayit_yolu)

            print(f"{dosya} -> {yeni_dosya_adi}")

            foto_sayaci += 1

    print("\nTüm fotoğraflar başarıyla işlendi!")

if __name__ == "__main__":
    main()
