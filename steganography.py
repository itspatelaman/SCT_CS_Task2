import numpy as np
from PIL import Image

def _message_to_bits(message):
    return ''.join(f"{ord(c):08b}" for c in message)

def _bits_to_message(bits):
    chars = [chr(int(bits[i:i+8], 2)) for i in range(0, len(bits), 8)]
    return ''.join(chars)

def hide_message(image, message):
    img_array = np.array(image)
    flat = img_array.flatten()

    message += '<<END>>'  # Delimiter to mark end of message
    bits = _message_to_bits(message)
    if len(bits) > len(flat):
        raise ValueError("Message too long to hide in this image.")

    for i in range(len(bits)):
        flat[i] = (int(flat[i]) & 0b11111110) | int(bits[i]) # LSB replacement

    new_array = flat.reshape(img_array.shape)
    return Image.fromarray(new_array.astype(np.uint8))

def extract_message(image):
    img_array = np.array(image)
    flat = img_array.flatten()

    bits = ''.join(str(pixel & 1) for pixel in flat)
    chars = _bits_to_message(bits)
    message = chars.split("<<END>>")[0]  # Extract until delimiter
    return message