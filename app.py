import os
import shutil
import datetime
import zipfile
import re

from pathlib import Path
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import askdirectory

import ttkbootstrap as ttk
from ttkbootstrap.scrolled import ScrolledText
from ttkbootstrap.constants import *

_PATH_FROM = 'C:/PhotoWork/From'
_PATH_TO = 'C:/PhotoWork/To'

_SCREEN_MIN_WIDTH = 700
_SCREEN_MIN_HEIGHT = 900

class Screen():
    def __init__(self):
        self.auto_mode = False
        
        self.root = ttk.Window('BKP')

        self.sv_path_copy_from = ttk.StringVar(value='C:/Users/ROK/Downloads/DCIM')
        self.sv_path_copy_to = ttk.StringVar(value=f'{_PATH_FROM}/Temp')

        self.sv_path_split_from = ttk.StringVar(value=_PATH_FROM)
        self.sv_path_split_to = ttk.StringVar(value=_PATH_TO)

        self.sv_path_zip_from = ttk.StringVar(value=_PATH_TO)
        self.sv_path_zip_to = ttk.StringVar(value=f'{_PATH_TO}/ZIP')
        self.sv_path_zip_copy = ttk.StringVar(value='C:/PhotoWork/HDD')
        
        screen_width = _SCREEN_MIN_WIDTH
        screen_height = _SCREEN_MIN_HEIGHT
        screen_x = int((self.root.winfo_screenwidth() / 2) - (screen_width / 2))
        screen_y = 50

        self.root.title('Backup photos...')
        self.root.geometry('{}x{}+{}+{}'.format(screen_width, screen_height, screen_x, screen_y))
        self.root.minsize(width=_SCREEN_MIN_WIDTH, height=_SCREEN_MIN_HEIGHT)
        self.root.resizable(True, True)
        self.root.protocol('WM_DELETE_WINDOW', lambda: self.root.destroy())
        
        self.render_screen_default()
        self.render_screen_tab1()
        
    def render_screen_default(self):
        frame_top = ttk.Frame(self.root)
        frame_top.pack(fill=BOTH, expand=YES, anchor=N+W, padx=(5,5), pady=(5,5))
        
        self.nb = ttk.Notebook(frame_top)
        self.nb.pack(fill=X, anchor=N+W)
        
        lf = ttk.Labelframe(frame_top, text='Log')
        lf.pack(fill=BOTH, expand=YES, anchor=S+W, pady=(5,0))
        
        self.log = ScrolledText(lf, height=6, autohide=True)
        self.log.pack(fill=BOTH, expand=YES, anchor=N+W, padx=(5,5), pady=(5,5))
        
        frame_bottom = ttk.Frame(self.root)
        frame_bottom.pack(fill=X, anchor=W, side=BOTTOM)
        
        self.prb = ttk.Floodgauge(frame_bottom, mode=DETERMINATE, bootstyle=SUCCESS)
        self.prb.pack(fill=X, anchor=W, side=TOP, padx=(5,5), pady=(5,0))
        
        self.stb = ttk.Label(frame_bottom, relief=SUNKEN, border=1)
        self.stb.pack(fill=X, anchor=W, side=BOTTOM, pady=(5,0))
        
        self.prb.step(0)
    
    def render_screen_tab1(self):
        frame = ttk.Frame(self.nb)

        self.render_screen_tab1_step1(frame)
        self.render_screen_tab1_step2(frame)
        self.render_screen_tab1_step3(frame)
        self.render_screen_tab1_step4(frame)
        
        # Add main frame to tab
        self.nb.add(frame, text='COPY')

    def render_screen_tab1_step1(self, frame):
        lf = ttk.Labelframe(frame, text='STEP 1 - Copy')
        lf.pack(fill=X, padx=(5,5), pady=(5,0))

        lbl = ttk.Label(lf, text='From Path:', width=12)
        lbl.grid(row=0, column=0, sticky=W, padx=(5,5), pady=(5,0))

        ent = ttk.Entry(lf, textvariable=self.sv_path_copy_from, width=40)
        ent.grid(row=0, column=1, sticky=W, padx=(5,5), pady=(5,0))

        btn = ttk.Button(lf, text='Browse', width=8, command=lambda: self.file_browser(self.sv_path_copy_from))
        btn.grid(row=0, column=2, sticky=W, padx=(5,5), pady=(5,0))

        lbl = ttk.Label(lf, text='To Path:', width=12)
        lbl.grid(row=1, column=0, sticky=W, padx=(5,5), pady=(5,0))

        ent = ttk.Entry(lf, textvariable=self.sv_path_copy_to, width=40)
        ent.grid(row=1, column=1, sticky=W, padx=(5,5), pady=(5,0))

        btn = ttk.Button(lf, text='Browse', width=8, command=lambda: self.file_browser(self.sv_path_copy_to))
        btn.grid(row=1, column=2, sticky=W, padx=(5,5), pady=(5,0))

        lbl = ttk.Label(lf, text="If you are ready to copy the files, click the 'Copy' button.", bootstyle=INFO)
        lbl.grid(row=2, column=0, columnspan=2, sticky=W, padx=(5,5), pady=(5,0))

        btn = ttk.Button(lf, text='Copy', width=8, bootstyle='success-outline', command=lambda: self.copy_files(self.sv_path_copy_from.get(), self.sv_path_copy_to.get()))
        btn.grid(row=2, column=2, sticky=W, padx=(5,5), pady=(5,0))

        lbl = ttk.Label(lf, text="If you want to rename the copied files, click the 'Rename' button.", bootstyle=INFO)
        lbl.grid(row=3, column=0, columnspan=2, sticky=W, padx=(5,5), pady=(5,0))

        btn = ttk.Button(lf, text='Rename', width=8, bootstyle='warning-outline', command=lambda: self.rename_files(self.sv_path_copy_to.get()))
        btn.grid(row=3, column=2, sticky=W, padx=(5,5), pady=(5,5))

    def render_screen_tab1_step2(self, fr_main):
        lf = ttk.Labelframe(fr_main, text='STEP 2 - Split')
        lf.pack(fill=X, padx=(5,5), pady=(5,0))

        lbl = ttk.Label(lf, text='From Path :', width=12)
        lbl.grid(row=0, column=0, sticky=W, padx=(5,5), pady=(5,0))

        ent = ttk.Entry(lf, text=self.sv_path_split_from, width=40)
        ent.grid(row=0, column=1, sticky=W, padx=(5,5), pady=(5,0))

        btn = ttk.Button(lf, text='Browse', width=8, command=lambda: self.file_browser(self.sv_path_split_from))
        btn.grid(row=0, column=2, sticky=W, padx=(5,5), pady=(5,0))

        lbl = ttk.Label(lf, text='To Path :', width=12)
        lbl.grid(row=1, column=0, sticky=W, padx=(5,5), pady=(5,0))

        ent = ttk.Entry(lf, text=self.sv_path_split_to, width=40)
        ent.grid(row=1, column=1, sticky=W, padx=(5,5), pady=(5,0))

        btn = ttk.Button(lf, text='Browse', width=8, command=lambda: self.file_browser(self.sv_path_split_to))
        btn.grid(row=1, column=2, sticky=W, padx=(5,5), pady=(5,0))

        lbl = ttk.Label(lf, text="If you want to move the files to monthly dir., click the 'Split' button.", bootstyle=INFO)
        lbl.grid(row=2, column=0, columnspan=2, sticky=W, padx=(5,5), pady=(5,0))

        btn = ttk.Button(lf, text='Split', width=8, bootstyle='success-outline', command=lambda: self.split_files(self.sv_path_split_from.get(),  self.sv_path_split_to.get()))
        btn.grid(row=2, column=2, padx=(5,5), pady=(5,5))

    def render_screen_tab1_step3(self, fr_main):
        lf = ttk.Labelframe(fr_main, text='STEP 3 - Compress')
        lf.pack(fill=X, padx=(5,5), pady=(5,0))

        lbl = ttk.Label(lf, text='From Path :', width=12)
        lbl.grid(row=0, column=0, sticky=W, padx=(5,5), pady=(5,0))

        ent = ttk.Entry(lf, text=self.sv_path_zip_from, width=40)
        ent.grid(row=0, column=1, sticky=W, padx=(5,5), pady=(5,0))

        btn = ttk.Button(lf, text='Browse', width=8, command=lambda: self.file_browser(self.sv_path_zip_from))
        btn.grid(row=0, column=2, sticky=W, padx=(5,5), pady=(5,0))

        lbl = ttk.Label(lf, text='To Path :', width=12)
        lbl.grid(row=1, column=0, sticky=W, padx=(5,5), pady=(5,0))

        ent = ttk.Entry(lf, text=self.sv_path_zip_to, width=40)
        ent.grid(row=1, column=1, sticky=W, padx=(5,5), pady=(5,0))

        btn = ttk.Button(lf, text='Browse', width=8, command=lambda: self.file_browser(self.sv_path_zip_to))
        btn.grid(row=1, column=2, sticky=W, padx=(5,5), pady=(5,0))

        lbl = ttk.Label(lf, text='Copy Path :', width=12)
        lbl.grid(row=2, column=0, sticky=W, padx=(5,5), pady=(5,0))

        ent = ttk.Entry(lf, text=self.sv_path_zip_copy, width=40)
        ent.grid(row=2, column=1, sticky=W, padx=(5,5), pady=(5,0))

        btn = ttk.Button(lf, text='Browse', width=8, command=lambda: self.file_browser(self.sv_path_zip_copy))
        btn.grid(row=2, column=2, sticky=W, padx=(5,5), pady=(5,0))

        lbl = ttk.Label(lf, text="If you want to compress the folders monthly, click the 'ZIP' button.", bootstyle=INFO)
        lbl.grid(row=3, column=0, columnspan=2, sticky=W, padx=(5,5), pady=(5,0))

        btn = ttk.Button(lf, text='ZIP', width=8, bootstyle='success-outline', command=lambda: self.compress_files(self.sv_path_zip_from.get(), self.sv_path_zip_to.get()))
        btn.grid(row=3, column=2, padx=(5,5), pady=(5,0))

        lbl = ttk.Label(lf, text="If you want to copy the generated zip files, click the 'Copy' button.", bootstyle=INFO)
        lbl.grid(row=4, column=0, columnspan=2, sticky=W, padx=(5,5), pady=(5,0))

        btn = ttk.Button(lf, text='Copy', width=8, bootstyle='warning-outline', command=lambda: self.copy_files(self.sv_path_zip_to.get(), self.sv_path_zip_copy.get()))
        btn.grid(row=4, column=2, padx=(5,5), pady=(5,5))

    def render_screen_tab1_step4(self, fr_main):
        lf = ttk.Labelframe(fr_main, text='STEP 4 - Auto')
        lf.pack(fill=X, padx=(5,5), pady=(5,5))
        
        lbl = ttk.Label(lf, text="If all the settings are complete, please click the 'Auto' button.", bootstyle=INFO)
        lbl.grid(row=0, column=0, columnspan=2, sticky=W, padx=(5,5), pady=(5,0))

        btn = ttk.Button(lf, text='Auto', width=12, bootstyle='danger-outline', command=lambda: self.auto_proc())
        btn.grid(row=0, column=2, padx=(5,5), pady=(5,5))


    def copy_files(self, from_path, to_path):
        if from_path == '':
            self.show_status('The from path is blank.', done=True)
            return
        
        os.makedirs(to_path, exist_ok=True)

        list_file = self.build_list_file(from_path)
        list_len = len(list_file)
        
        for i, file in enumerate(list_file):
            self.copy_file(file, to_path, prb_len=list_len, prb_step=i)
            
        self.show_status('The copy has been completed.', done=True)


    def rename_files(self, path):
        if path == '':
            self.show_status('The re name path is blank.', done=True)
            return
        
        list_file = os.listdir(path)
        list_len = len(list_file)
        
        for i, file in enumerate(list_file):
            if re.match(r'^\d{8}_\d{6}', file):
                continue
            
            file_path = self.path_join(path, file)
            file_basename, file_ext = os.path.splitext(file)

            modified_time = os.path.getmtime(file_path)
            modified_date = datetime.datetime.fromtimestamp(modified_time)

            file_name_new = f'{modified_date.strftime("%Y%m%d_%H%M%S")}{file_ext}'
            file_path_new = self.path_join(path, file_name_new)
            
            os.rename(file_path, file_path_new)
            self.show_status(f'[RENAME] {file_path} > {file_path_new}', prb_len=list_len, prb_step=i)
        
        self.show_status('The rename has been completed.', done=True)


    def split_files(self, from_home_path, to_home_path):
        if from_home_path == '' or to_home_path == '':
            self.show_status('The path is blank.', done=True)
            return
        
        list_file = []

        for path in Path(from_home_path).iterdir():
            if not path.is_dir():
                continue

            list_file.extend(self.build_list_file(path))

        list_len = len(list_file)
        
        to_path = ''
        last_month = ''
        for i, file in enumerate(list_file):
            file_path, file_name = os.path.split(file)

            if last_month != f'{file_name[0:4]}.{file_name[4:6]}':
                last_month = f'{file_name[0:4]}.{file_name[4:6]}'

                to_path = f'{to_home_path}/{last_month}'
                os.makedirs(to_path, exist_ok=True)

            self.copy_file(file, to_path, move=True, prb_len=list_len, prb_step=i)

        self.show_status('The split has been completed.', done=True)


    def compress_files(self, from_path, to_path):
        if from_path == '' or to_path == '':
            self.show_status('The path is blank.', done=True)
            return
        
        os.makedirs(to_path, exist_ok=True)

        for path in Path(from_path).iterdir():
            if not path.is_dir() or not re.match(r'\d{4}\.\d{2}', str(path)[-7:]):
                continue

            list_file = os.listdir(path)
            list_len = len(list_file)
            if list_len > 0:
                zip_path = f'{to_path}/{str(path)[-7:]}.zip'

                if os.path.exists(zip_path):
                    os.remove(zip_path)

                zip_file = zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED)
                for i, file_name in enumerate(list_file):
                    file_path = self.path_join(path, file_name)
                    zip_file.write(file_path, file_name)
                    
                    self.show_status(f'[ZIP] {file_path} > {zip_path}', prb_len=list_len, prb_step=i)
                    
                zip_file.close()

        self.show_status('The compress has been completed.', done=True)


    def copy_file(self, from_file, to_path, move=False, prb_len=0, prb_step=0):
        copy_file = True

        file_name = os.path.basename(from_file)
        to_file = self.path_join(to_path, file_name)

        if os.path.exists(to_file):
            from_file_size = os.path.getsize(from_file)
            to_file_size = os.path.getsize(to_file)

            if(from_file_size == to_file_size):
                # No need to copy the sames files
                copy_file = False
            else:
                check_file_name, check_file_ext = os.path.splitext(file_name)
                for i in range(1, 100):
                    check_file = f'{check_file_name}_{i:03d}{check_file_ext}'

                    if not os.path.exists(check_file):
                        # It'll be copied as a new file name
                        to_file = self.path_join(to_path, check_file)
                        break

        if copy_file:
            if(move):
                shutil.move(from_file, to_file)
                self.show_status(f'[MOVE] {from_file} > {to_file}', prb_len=prb_len, prb_step=prb_step)
            else:
                shutil.copy2(from_file, to_file)
                self.show_status(f'[COPY] {from_file} > {to_file}', prb_len=prb_len, prb_step=prb_step)


    def auto_proc(self):
        self.auto_mode = True
        
        # Step 1
        self.copy_files(self.sv_path_copy_from.get(), self.sv_path_copy_to.get())
        self.rename_files(self.sv_path_copy_to.get())
        
        # Step 2
        self.split_files(self.sv_path_split_from.get(),  self.sv_path_split_to.get())
        
        # Step 3
        self.compress_files(self.sv_path_zip_from.get(), self.sv_path_zip_to.get())
        self.copy_files(self.sv_path_zip_to.get(), self.sv_path_zip_copy.get())
        
        self.auto_mode = False
        self.show_status('All process has been completed.', done=True)
    
    
    def build_list_file(self, path):
        list_file = []
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = self.path_join(root, file)
                list_file.append(file_path)

        return list_file

    def delete_files(self, path):
        if not messagebox.askyesno('Confirm', f'Are you sure to delete all files in "{path}"?'):
            return

        for root, dirs, files in os.walk(path, topdown=False):
            for file_name in files:
                file_path = self.path_join(root, file_name)
                os.remove(file_path)
            for dir_name in dirs:
                dir_path = self.path_join(root, dir_name)
                shutil.rmtree(dir_path)


    def file_browser(self, sv_path):
        path = askdirectory(title='Browse directory')
        if path:
            sv_path.set(path)

    
    def path_join(self, file_path, file_name):
        return os.path.join(file_path, file_name).replace('\\', '/')
    
    
    def show_status(self, text, prb_len=0, prb_step=0, done=False):
        self.log.insert(END, f'[{datetime.datetime.now()}] {text}\n')
        self.log.see(END)
            
        if done:
            self.stb.config(text=text)
            self.prb.configure(value=100)

            if self.auto_mode is False:
                messagebox.showinfo('Info', text)
        else:
            self.prb.configure(value=int(prb_len / (prb_step+1)))
            

if __name__ == '__main__':
    screen = Screen()
    screen.root.mainloop()
