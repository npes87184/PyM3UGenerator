import os
import sys
import tkinter as tk
import unicodedata
import webbrowser
from tkinter import filedialog, messagebox


class M3uGenerator(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.master = master
        self.pack()
        self.init_widget()
        self.selected_folder = None

    def init_widget(self):
        self.path_label = tk.Label(self,
                                   text=r'Please select music folder',
                                   font=('', 20),
                                   wraplength=500)
        self.path_label.grid(row=1,
                             columnspan=5,
                             sticky=tk.N,
                             ipadx=15,
                             padx=15,
                             pady=15)

        self.select_button = tk.Button(self,
                                       text='Select folder',
                                       font=('', 22),
                                       command=self.selection_folder)
        self.select_button.grid(row=2, column=1, pady=5)

        self.gen_button = tk.Button(self,
                                    text='Go',
                                    font=('', 22),
                                    command=self._gen_m3u)
        self.gen_button.grid(row=2, column=3, pady=5)

        self.fork_me_label = tk.Label(self,
                                      text=r'Fork me here',
                                      font=('', 18),
                                      fg='blue',
                                      cursor='hand2')
        self.fork_me_label.grid(row=3, columnspan=5, sticky=tk.S, pady=15)
        self.fork_me_label.bind('<Button-1>', self._fork_me)

    def _fork_me(self, *_):
        webbrowser.open_new_tab(r'https://github.com/npes87184/PyM3UGenerator')

    def selection_folder(self):
        self.selected_folder = filedialog.askdirectory(initialdir=r'./')

        if os.path.exists(self.selected_folder):
            self.path_label['text'] = self.selected_folder
        else:
            self.path_label['text'] = r'Please select music folder first'

    def _gen_m3u(self):
        if not self.selected_folder or not os.path.isdir(self.selected_folder):
            messagebox.showwarning(r'Warning',
                                   r'Please select music folder first')
            return

        def is_music(path):
            support_extension = {
                '.mp3', '.m3u', '.wma', '.flac', '.wav', '.mc', '.aac', '.m4a',
                '.ape', '.dsf', '.dff'
            }
            filename, extension = os.path.splitext(path)
            if extension.lower() in support_extension:
                return True
            return False

        def create_playList(selected_folder):
            m3u_list = []

            for root, subdirs, files in os.walk(selected_folder):
                for filename in files:
                    rel_dir = os.path.relpath(root, selected_folder)
                    if rel_dir == '.':
                        path = filename
                    else:
                        path = os.path.join(rel_dir, filename)
                    if is_music(path):
                        m3u_list.append(path)

            return m3u_list

        m3u_path = os.path.join(
            self.selected_folder,
            os.path.basename(self.selected_folder) + '.m3u8')

        if os.path.exists(m3u_path):
            is_overwrite = messagebox.askyesno(
                'Already exist',
                'The m3u8 file already exists in the output folder. Do you want to overwrite it?'
            )
            if not is_overwrite:
                return

        m3u_list = create_playList(self.selected_folder)

        with open(m3u_path, 'w', encoding='utf-8') as f:
            for music in m3u_list:
                f.write('{}\n'.format(unicodedata.normalize('NFC', music)))

        messagebox.showinfo(r'Successfully generated', m3u_path)


if __name__ == '__main__':
    root = tk.Tk()
    root.minsize(640, 250)
    root.title(r'M3uGenerator')
    app = M3uGenerator(master=root)
    app.mainloop()
