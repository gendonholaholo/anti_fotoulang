from PIL import Image, ImageDraw, ImageFilter
import numpy as np
import random

# Fungsi untuk menambahkan noise halus
def add_noise(image, intensity=30):
    # Konversi gambar ke array NumPy
    np_img = np.array(image)
    # Membuat noise
    noise = np.random.randint(-intensity, intensity, np_img.shape, dtype='int16')
    # Menambahkan noise ke gambar asli
    noisy_img = np.clip(np_img + noise, 0, 255).astype('uint8')
    return Image.fromarray(noisy_img)

# Fungsi untuk menambahkan pola garis halus
def add_stripe_pattern(image, stripe_width=2, opacity=50):
    draw = ImageDraw.Draw(image)
    for y in range(0, image.height, stripe_width * 2):
        draw.rectangle([0, y, image.width, y + stripe_width], fill=(255, 255, 255, opacity))
    return image

# Fungsi untuk menambahkan efek chromatic aberration sederhana
# def add_chromatic_aberration(image, shift=5):
#     r, g, b = image.split()
#     r = r.offset(shift, 0) # Geser kanal merah
#     b = b.offset(-shift, 0) # Geser kanal biru
#     return Image.merge("RGB", (r, g, b))

def add_chromatic_aberration(image, shift=5):
    # Pisahkan gambar menjadi saluran R, G, dan B
    r, g, b = image.split()
    
    # Ubah masing-masing saluran menjadi array NumPy
    r = np.array(r)
    g = np.array(g)
    b = np.array(b)
    
    # Geser saluran merah dan biru
    r = np.roll(r, shift, axis=1)  # Geser saluran merah ke kanan
    b = np.roll(b, -shift, axis=1) # Geser saluran biru ke kiri
    
    # Pastikan hasilnya tetap berada dalam rentang [0, 255]
    r = np.clip(r, 0, 255)
    b = np.clip(b, 0, 255)
    
    # Kembali ke objek gambar Pillow setelah dimanipulasi
    r = Image.fromarray(r.astype('uint8'))
    g = Image.fromarray(g.astype('uint8'))
    b = Image.fromarray(b.astype('uint8'))
    
    # Gabungkan kembali saluran RGB menjadi gambar
    return Image.merge("RGB", (r, g, b))


# Membuka gambar asli
input_image_path = "input.jpg" # Ganti dengan path gambar asli
output_image_path = "output.jpg" # Nama file output
image = Image.open(input_image_path).convert("RGB")

# Menambahkan efek pada gambar
image_with_noise = add_noise(image)
image_with_stripes = add_stripe_pattern(image_with_noise)
final_image = add_chromatic_aberration(image_with_stripes)

# Simpan gambar hasil
final_image.save(output_image_path)
print("Gambar dengan efek tersimpan di:", output_image_path)
