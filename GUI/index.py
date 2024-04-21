import tkinter as tk

# Membuat fungsi untuk menampilkan teks saat tombol ditekan
def show_text():
    label.config(text="Hello, World!")

# Membuat instance Tkinter
root = tk.Tk()

# Menentukan ukuran jendela
root.geometry("1820x800")

# Mengatur warna latar belakang root menjadi hitam
root.configure(bg="#c3cfd9")

# Membuat frame untuk bagian kiri
left_frame = tk.Frame(root, width=1220, bg="black")
left_frame.pack_propagate(False)
left_frame.pack(side="right")

# Membuat frame untuk garis pemisah
separator = tk.Frame(root, width=3, bg="white")
separator.pack(side="right", fill="y")

# Membuat frame untuk bagian kanan
right_frame = tk.Frame(root, width=1200, bg="black")
right_frame.pack_propagate(False)
right_frame.pack(side="right")

# Membuat label di bagian kiri
label = tk.Label(left_frame, text="Welcome to my GUI", font=("Arial", 24), fg="white", bg="black")
label.pack(pady=40)

# Membuat tombol di bagian kiri
button = tk.Button(left_frame, text="Click Me!", command=show_text, bg="white", fg="black")
button.pack()

# Menjalankan program
root.mainloop()
