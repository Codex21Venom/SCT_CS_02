# 🔐 Image Encryptor & Decryptor

A simple yet powerful GUI application built with Python and Tkinter to encrypt and decrypt images using custom pixel manipulation and key-based logic.

---

## ✨ Features

- 📁 Load and preview images (`.jpg`, `.jpeg`, `.png`)
- 🔒 Encrypt image using:
  - Pixel shuffling (randomized)
  - Color value transformation with a secure key
- 💾 Automatically save a key file during encryption
- 🔓 Decrypt the image using the saved key file
- 💡 Light & Dark mode toggle for better UX
- 💽 Save encrypted/decrypted images

---

## 🖥️ Technologies Used

- **Python 3.x**
- **Tkinter** - GUI framework
- **Pillow (PIL)** - Image processing
- **ttk** - Themed widgets

---

## 📦 Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/Image-Encryptor.git
   cd Image-Encryptor
2. **Install dependencies**

    ````bash
    pip install pillow
3. **Run the app**

    ```bash
    python gui_encryptor.py

## 📸 Usage

## 🔄 Encryption

- Click "📁 Load Image" to select an image.
- Click "🔒 Encrypt" to scramble the image.
- Save the generated .key file when prompted.
- Optionally save the encrypted image using "💾 Save".

## 🔓 Decryption

- Load an encrypted image using "📁 Load Image".
- Click "🔓 Decrypt" and select the correct .key file.
- The original image is restored.
- Save the decrypted image if needed.


## 🧠 How It Works

## Encryption:

- Randomly shuffles the pixel indices.
- Alters each RGB value using a modulo operation with a fixed key.
- Saves the shuffle order as a .key file.

## Decryption:

- Reverts the RGB transformation using the key.
- Reconstructs the original pixel order using the .key file.

Created by codex21venom as part of a cybersecurity internship @SkillCraft_Technology.