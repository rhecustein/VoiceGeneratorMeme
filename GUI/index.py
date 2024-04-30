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
left_frame = tk.Frame(root, width=1220, bg="#c3cfd9")
left_frame.pack_propagate(False)
left_frame.pack(side="left", fill="y")

# Membuat frame untuk diver di atas text area box
divider = tk.Frame(left_frame, height=10, bg="#c3cfd9")
divider.pack(side="top", pady=10, fill="x")

# Membuat text area box di bagian kiri
text_area = tk.Text(left_frame, height=20, width=50, bg="white", fg="black")
text_area.pack(side="left", padx=20)

# Membuat button submit di samping text box
submit_button = tk.Button(left_frame, text="Submit", command=show_text, bg="white", fg="black")
submit_button.pack(side="left", padx=10)

# Membuat select card di bagian kiri
ref_joke_label = tk.Label(left_frame, text="Reference Joke List", font=("Arial", 16), fg="yellow", bg="#c3cfd9")
ref_joke_label.pack(side="bottom", pady=10)

# Membuat select card 1
select_card1 = tk.Label(left_frame, text="Joke 1", bg="yellow", fg="black", font=("Arial", 12))
select_card1.pack(side="bottom", pady=5)

# Membuat select card 2
select_card2 = tk.Label(left_frame, text="Joke 2", bg="yellow", fg="black", font=("Arial", 12))
select_card2.pack(side="bottom", pady=5)

# Membuat select card 3
select_card3 = tk.Label(left_frame, text="Joke 3", bg="yellow", fg="black", font=("Arial", 12))
select_card3.pack(side="bottom", pady=5)

# Membuat select card 4
select_card4 = tk.Label(left_frame, text="Joke 4", bg="yellow", fg="black", font=("Arial", 12))
select_card4.pack(side="bottom", pady=5)

# Membuat select card 5
select_card5 = tk.Label(left_frame, text="Joke 5", bg="yellow", fg="black", font=("Arial", 12))
select_card5.pack(side="bottom", pady=5)

# Menjalankan program
root.mainloop()