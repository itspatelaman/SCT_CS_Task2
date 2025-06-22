import numpy as np
from PIL import Image

def load_image(path):
    return Image.open(path)

def save_image(img, path):
    img.save(path)

def encrypt_shift(image, shift=50):
    img_array = np.array(image).astype(np.uint16)  # Use uint16 to prevent overflow
    encrypted_array = (img_array + shift) % 256
    return Image.fromarray(encrypted_array.astype(np.uint8))

def decrypt_shift(image, shift=50):
    img_array = np.array(image).astype(np.uint16)
    decrypted_array = (img_array - shift) % 256
    return Image.fromarray(decrypted_array.astype(np.uint8))

# Swap logic (already working)
def encrypt_swap(image, seed=42):
    np.random.seed(seed)
    img_array = np.array(image)
    flat = img_array.flatten()
    perm = np.random.permutation(len(flat))
    encrypted = flat[perm]
    return Image.fromarray(encrypted.reshape(img_array.shape))

def decrypt_swap(image, seed=42):
    np.random.seed(seed)
    img_array = np.array(image)
    flat = img_array.flatten()
    perm = np.random.permutation(len(flat))
    decrypted = np.empty_like(flat)
    decrypted[perm] = flat
    return Image.fromarray(decrypted.reshape(img_array.shape))
