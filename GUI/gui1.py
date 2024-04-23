from tkinter import filedialog as FD
import customtkinter

try:
    from openai import OpenAI
    from transformers import AutoProcessor, BarkModel
    import torch
except Exception as e:
    print(" [+] Installing dependency...")
    dependeny = ["openai"]
    for i in dependeny:
        os.system("python -m pip install " + i)
        os.system("pip install git+https://github.com/huggingface/transformers.git")
        sys.exit(
            "Please manually install PyTorch -- https://pytorch.org/get-started/locally/"
        )

    try:
        from openai import OpenAI
        from transformers import AutoProcessor, BarkModel
        import torch
    except:
        print(" [!] Failed to install dependency")
        input(" [!] Error, please check internet connection")
        sys.exit()



class GUI:
    def __init__(self):
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("blue")
        self._app = customtkinter.CTk()
        self._app.geometry("520x700")
        self._app.title("GUI 1")

    def start(self):
        # self.frame1()
        self._app.grid_columnconfigure(4, weight=1)
        self.grid1()
        # self.gridtest()
        self._app.mainloop()

    def grid1(self):
        self.grid1_container_chat()
        self.grid1_textbox_prompt()
        self.grid1_btn_prompt()

    def grid1_textbox_prompt(self):
        self.g_grid1_textbox_prompt = customtkinter.CTkTextbox(
            master=self._app,
            width=360,
            height=80,
            # font=("Lucida Console", 12),
            state="normal",
        )
        self.g_grid1_textbox_prompt.grid(
            row=1,
            column=0,
            padx=20,
            pady=20,
            columnspan=3,
        )
        self.g_grid1_textbox_prompt.insert("0.0", f"box")

    def grid1_btn_prompt(self):
        self.g_grid1_btn_prompt = customtkinter.CTkButton(
            master=self._app,
            width=80,
            height=80,
            text="Send",
            # command=self.btn_outputdir,
            # state="disabled",
        )
        # self.g_grid1_btn_outputdir.pack(pady=10, padx=10)
        self.g_grid1_btn_prompt.grid(row=1, column=3, padx=20, pady=20)

    def grid1_container_chat(self):
        self.g_grid1_container_chat = customtkinter.CTkScrollableFrame(
            master=self._app,
            width=460,
            height=500,
        )
        self.grid_rowconfigure(5, weight=1)  # configure grid system
        self.grid_columnconfigure(3, weight=1)
        self.g_grid1_container_chat.grid(
            row=0, column=0, padx=20, pady=20, columnspan=4
        )


def main():
    app = GUI()
    app.start()


if __name__ == "__main__":
    main()
