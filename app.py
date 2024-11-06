from PIL import Image, ImageDraw, ImageFilter
import numpy as np
import random

def add_noise(image, intensity=30):
    np_img = np.array(image)
    noise = np.random.randint(-intensity, intensity, np_img.shape, dtype='int16')
    noisy_img = np.clip(np_img + noise, 0, 255).astype('uint8')
    return Image.fromarray(noisy_img)

def add_stripe_pattern(image, stripe_width=2, opacity=50):
    draw = ImageDraw.Draw(image)
    for y in range(0, image.height, stripe_width * 2):
        draw.rectangle([0, y, image.width, y + stripe_width], fill=(255, 255, 255, opacity))
    return image

def add_chromatic_aberration(image, shift=8, blur_radius=10, noise_level=3):
    r, g, b = image.split()
    
    r = np.array(r)
    g = np.array(g)
    b = np.array(b)
    
    noise_r = np.random.randint(-noise_level, noise_level, r.shape)  # Noise saluran merah
    noise_b = np.random.randint(-noise_level, noise_level, b.shape)  # Noise saluran biru
    
    r = np.roll(r + noise_r, shift, axis=1)  
    b = np.roll(b + noise_b, -shift, axis=1)
    
    r = np.clip(r, 0, 255)
    b = np.clip(b, 0, 255)
    
    r = Image.fromarray(r.astype('uint8')).filter(ImageFilter.GaussianBlur(blur_radius))
    g = Image.fromarray(g.astype('uint8'))  
    b = Image.fromarray(b.astype('uint8')).filter(ImageFilter.GaussianBlur(blur_radius))
    
    return Image.merge("RGB", (r, g, b))

from PIL import Image, ImageFilter, ImageEnhance, ImageDraw
import numpy as np

def create_focus_effect(image, shift=5, blur_radius=10, noise_level=3, brightness_factor=1.5, focus_area=(0.5, 0.5), focus_radius=0.1):
    r, g, b = image.split()
    
    r = np.array(r)
    g = np.array(g)
    b = np.array(b)
    
    noise_r = np.random.randint(-noise_level, noise_level, r.shape)  
    noise_b = np.random.randint(-noise_level, noise_level, b.shape) 
    
    r = np.roll(r + noise_r, shift, axis=1)  
    b = np.roll(b + noise_b, -shift, axis=1)
    
    r = np.clip(r, 0, 255)
    b = np.clip(b, 0, 255)
    
    r = Image.fromarray(r.astype('uint8')).filter(ImageFilter.GaussianBlur(blur_radius))
    g = Image.fromarray(g.astype('uint8')) 
    b = Image.fromarray(b.astype('uint8')).filter(ImageFilter.GaussianBlur(blur_radius))
    
    final_image = Image.merge("RGB", (r, g, b))
    
    enhancer = ImageEnhance.Brightness(final_image)
    final_image = enhancer.enhance(brightness_factor)
    
    width, height = final_image.size
    mask = Image.new("L", final_image.size, 0)
    
    focus_center_x = int(width * focus_area[0])
    focus_center_y = int(height * focus_area[1])
    focus_radius_pixels = int(min(width, height) * focus_radius)
    
    draw = ImageDraw.Draw(mask)
    draw.ellipse([focus_center_x - focus_radius_pixels, focus_center_y - focus_radius_pixels,
                  focus_center_x + focus_radius_pixels, focus_center_y + focus_radius_pixels], fill=255)
    
    final_image = Image.composite(final_image, final_image.filter(ImageFilter.GaussianBlur(20)), mask)
    
    return final_image


input_image_path = "input.jpg"
output_image_path = "output.jpg" # Nama file output
image = Image.open(input_image_path).convert("RGB")

image_with_noise = add_noise(image)
image_with_stripes = add_stripe_pattern(image_with_noise)
final_image = add_chromatic_aberration(image_with_stripes)

final_image.save(output_image_path)
print("Gambar dengan efek tersimpan di:", output_image_path)
