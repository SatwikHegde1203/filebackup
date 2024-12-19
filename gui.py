
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar
import threading
from backup import BackupManager

# GUI for the backup process
class BackupApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Backup Utility")

        self.source_dir = tk.StringVar()
        self.backup_dir = tk.StringVar()
        self.backup_manager = BackupManager()
        self.thread = None

        # Layout
        tk.Label(root, text="Source Directory:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        tk.Entry(root, textvariable=self.source_dir, width=50).grid(row=0, column=1, padx=10, pady=5)
        tk.Button(root, text="Browse", command=self.select_source_dir).grid(row=0, column=2, padx=10, pady=5)

        tk.Label(root, text="Backup Directory:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        tk.Entry(root, textvariable=self.backup_dir, width=50).grid(row=1, column=1, padx=10, pady=5)
        tk.Button(root, text="Browse", command=self.select_backup_dir).grid(row=1, column=2, padx=10, pady=5)

        self.progress_bar = Progressbar(root, orient="horizontal", length=400, mode="determinate")
        self.progress_bar.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

        self.status_label = tk.Label(root, text="Status: Idle")
        self.status_label.grid(row=3, column=0, columnspan=3, padx=10, pady=5)

        self.start_button = tk.Button(root, text="Start Backup", command=self.start_backup, bg="green", fg="white")
        self.start_button.grid(row=4, column=0, pady=10)

        self.pause_button = tk.Button(root, text="Pause", command=self.pause_backup, state="disabled")
        self.pause_button.grid(row=4, column=1, pady=10)

        self.cancel_button = tk.Button(root, text="Cancel", command=self.cancel_backup, state="disabled", bg="red", fg="white")
        self.cancel_button.grid(row=4, column=2, pady=10)

    def select_source_dir(self):
        self.source_dir.set(filedialog.askdirectory(title="Select Source Directory"))

    def select_backup_dir(self):
        self.backup_dir.set(filedialog.askdirectory(title="Select Backup Directory"))

    def start_backup(self):
        source = self.source_dir.get()
        backup = self.backup_dir.get()
        if not source or not backup:
            messagebox.showerror("Error", "Both source and backup directories must be selected.")
            return

        self.start_button.config(state="disabled")
        self.pause_button.config(state="normal")
        self.cancel_button.config(state="normal")
        self.thread = threading.Thread(target=self.run_backup, args=(source, backup))
        self.thread.start()

    def run_backup(self, source, backup):
        def progress_callback(status, progress):
            self.status_label.config(text=f"Status: {status} ({progress}%)")
            self.progress_bar["value"] = progress

        try:
            result = self.backup_manager.backup_files(source, backup, progress_callback)
            messagebox.showinfo("Result", result)
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            self.reset_ui()

    def pause_backup(self):
        if self.backup_manager.paused:
            self.backup_manager.unpause()
            self.pause_button.config(text="Pause")
        else:
            self.backup_manager.pause()
            self.pause_button.config(text="Unpause")

    def cancel_backup(self):
        self.backup_manager.cancel()
        self.reset_ui()

    def reset_ui(self):
        self.start_button.config(state="normal")
        self.pause_button.config(state="disabled")
        self.cancel_button.config(state="disabled")
        self.progress_bar["value"] = 0
        self.status_label.config(text="Status: Idle")


# Initialize the application
root = tk.Tk()
app = BackupApp(root)
root.mainloop()
