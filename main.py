from encryptor import (
    load_image, save_image,
    encrypt_shift, decrypt_shift,
    encrypt_swap, decrypt_swap
)

def test_image_encryption(image_path):
    print("[*] Loading image...")
    img = load_image(image_path)

    print("[*] Encrypting using pixel shift...")
    encrypted_shift = encrypt_shift(img, shift=50)
    save_image(encrypted_shift, "shift_encrypted.png")

    print("[*] Decrypting pixel shift...")
    decrypted_shift = decrypt_shift(encrypted_shift, shift=50)
    save_image(decrypted_shift, "shift_decrypted.png")

    print("[*] Encrypting using pixel swap...")
    encrypted_swap = encrypt_swap(img, seed=42)
    save_image(encrypted_swap, "swap_encrypted.png")

    print("[*] Decrypting pixel swap...")
    decrypted_swap = decrypt_swap(encrypted_swap, seed=42)
    save_image(decrypted_swap, "swap_decrypted.png")

    print("[+] All operations complete. Check the output images.")

if __name__ == "__main__":
    test_image_encryption("input.jpg")  # Make sure this file exists in the same folder
