import subprocess
import threading
import time
import tkinter as tk
from tkinter import scrolledtext

def run_windows_command(text_widget):
    cmd_script = 'FOR /L %i IN (1,1,100) DO dir /s /b'
    
    process = subprocess.Popen(
        ['cmd.exe', '/c', cmd_script],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    buffer = []
    last_update = time.time()

    for line in process.stdout:
        clean_line = line.replace(r'\e[32m', '').replace('\033[32m', '')
        buffer.append(clean_line)

        if time.time() - last_update > 0.05:
            output_text = "".join(buffer)
            text_widget.after(0, lambda t=output_text: update_gui(text_widget, t))
            buffer.clear()
            last_update = time.time()
            
    if buffer:
        output_text = "".join(buffer)
        text_widget.after(0, lambda t=output_text: update_gui(text_widget, t))

    process.stdout.close()
    process.wait()

def update_gui(text_widget, text):
    text_widget.insert(tk.END, text)
    
    try:
        num_lines = int(text_widget.index('end-1c').split('.')[0])
        if num_lines > 5000:
            text_widget.delete('1.0', f'{num_lines - 5000}.0')
    except Exception:
        pass
        
    text_widget.see(tk.END)

root = tk.Tk()
root.title("OthGUI")

root.geometry("800x500")
root.configure(bg="black")

text_area = scrolledtext.ScrolledText(
    root, 
    wrap=tk.WORD, 
    bg="black", 
    fg="#00FF00", 
    insertbackground="white", 
    font=("Courier", 11)
)
text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

thread = threading.Thread(target=run_windows_command, args=(text_area,), daemon=True)
thread.start()

root.mainloop()
