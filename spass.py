import csv
import datetime
import io
import json
import os
import tkinter as tk
from base64 import b64decode
from tkinter import filedialog, messagebox

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def decrypt_file(encrypted_data_base64, passkey):
    # Constants
    salt_size = 20
    iterations = 70000
    key_length = 32  # 256 bits

    # Decode the Base64 encoded data
    encrypted_data = b64decode(encrypted_data_base64)

    # Extract the salt, IV, and ciphertext
    salt = encrypted_data[:salt_size]
    iv = encrypted_data[salt_size: salt_size + 16]  # AES block size is 16 bytes
    ciphertext = encrypted_data[salt_size + 16:]

    # Derive the key using PBKDF2HMAC
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=key_length,
        salt=salt,
        iterations=iterations,
        backend=default_backend(),
    )
    key = kdf.derive(passkey.encode())

    # Decrypt the ciphertext
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    # Unpad the plaintext
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
    return plaintext.decode("utf-8")


def dump_csv(table_content, table_name, output_folder):
    tbl = csv.DictReader(io.StringIO(table_content.lstrip().rstrip()), delimiter=";")
    field_names = tbl.fieldnames
    output_path = os.path.join(output_folder, f"table_{table_name}.csv")
    with open(output_path, "w") as csv_out:
        writer = csv.DictWriter(csv_out, fieldnames=field_names, dialect="excel")
        writer.writeheader()

        # Decode the columns
        for row in tbl:
            for column in field_names:
                row[column] = b64decode(row[column]).decode("utf-8")
            writer.writerow(row)


def dump_json(table_content, table_name, output_folder):
    tbl = csv.DictReader(io.StringIO(table_content.lstrip().rstrip()), delimiter=";")
    field_names = tbl.fieldnames
    table_rows = list(tbl)

    # Decode the columns
    for row in table_rows:
        for column in field_names:
            row[column] = b64decode(row[column]).decode("utf-8")

    output_path = os.path.join(output_folder, f"table_{table_name}.json")
    with open(output_path, "w") as json_out:
        json.dump(table_rows, json_out, indent=True)


def decode_backup(in_content, out_fmt, output_folder):
    counter = 0
    tables = {
        1: "passwords",
        2: "cards",
        3: "addresses",
        4: "notes",
    }
    for t in in_content.split("next_table")[1:]:  # Skip the crap before the actual table
        counter += 1
        suffix = tables[counter] if counter in tables else f"{counter}"
        if out_fmt == "csv":
            dump_csv(t, suffix, output_folder)
        else:
            dump_json(t, suffix, output_folder)


def decrypt_and_decode(fname, key, output_folder, out_fmt):
    try:
        with open(fname, "rb") as inf:
            encrypted_data_base64 = inf.read()
        decrypted_text = decrypt_file(encrypted_data_base64, key)
        output_dir = os.path.join(output_folder, f"spass-decode-{datetime.datetime.utcnow().timestamp()}")
        os.makedirs(output_dir, exist_ok=True)

        decode_backup(decrypted_text, out_fmt, output_dir)
        messagebox.showinfo("Success", "Decryption and decoding completed successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred during decryption: {str(e)}")


def select_file():
    filename = filedialog.askopenfilename(title="Select Encrypted File")
    file_entry.delete(0, tk.END)
    file_entry.insert(0, filename)


def select_output_folder():
    foldername = filedialog.askdirectory(title="Select Output Folder")
    output_folder_entry.delete(0, tk.END)
    output_folder_entry.insert(0, foldername)


def main():
    global file_entry, output_folder_entry

    root = tk.Tk()
    root.title("Samsung Pass .spass Decoder")

    # Instructions label
    instructions = (
        "Instructions:\n"
        "1. Select the encrypted .spass file.\n"
        "2. Choose the output folder for the decrypted files.\n"
        "3. Enter the decryption password which was set during the export.\n"
        "4. Select the desired output format (CSV or JSON).\n"
        "5. Click 'Decode' to start the process."
    )
    tk.Label(root, text=instructions, justify=tk.LEFT).grid(row=0, column=0, columnspan=3, padx=10, pady=10)

    tk.Label(root, text="The .spass file:").grid(row=1, column=0, padx=10, pady=10)
    file_entry = tk.Entry(root, width=50)
    file_entry.grid(row=1, column=1, padx=10, pady=10)
    tk.Button(root, text="Browse", command=select_file).grid(row=1, column=2, padx=10, pady=10)

    tk.Label(root, text="Output Folder:").grid(row=2, column=0, padx=10, pady=10)
    output_folder_entry = tk.Entry(root, width=50)
    output_folder_entry.grid(row=2, column=1, padx=10, pady=10)
    tk.Button(root, text="Browse", command=select_output_folder).grid(row=2, column=2, padx=10, pady=10)

    tk.Label(root, text="Password:").grid(row=3, column=0, padx=10, pady=10)
    key_entry = tk.Entry(root, width=50, show="*")
    key_entry.grid(row=3, column=1, padx=10, pady=10)

    btn_csv = tk.Button(
        root,
        text="Decode into CSV",
        command=lambda: decrypt_and_decode(
            file_entry.get(),
            key_entry.get(),
            output_folder_entry.get(),
            "csv",
        ),
    )
    btn_csv.grid(row=4, column=0, columnspan=3, pady=10)

    btn_json = tk.Button(
        root,
        text="Decode into JSON",
        command=lambda: decrypt_and_decode(
            file_entry.get(),
            key_entry.get(),
            output_folder_entry.get(),
            "json",
        ),
    )
    btn_json.grid(row=5, column=0, columnspan=3, pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()
