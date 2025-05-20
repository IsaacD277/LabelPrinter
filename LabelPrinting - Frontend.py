import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import os
from PIL import Image

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class ModernApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ETS Equipment Sheet Printing")
        self.root.attributes('-fullscreen', False)
        
        self.setting1 = tk.StringVar()
        self.setting2 = tk.StringVar()
        self.setting3 = tk.StringVar()
        self.checkbox_var = tk.BooleanVar(value=True)
        self.device_var = tk.StringVar(value="Normal")
        
        self.input_history = []
        self.history_index = None  # None = not currently navigating history

        self.root.bind("<Escape>", lambda event: self.toggle_fullscreen(full=True))
        self.root.bind("<F11>", lambda event: self.toggle_fullscreen(full=False))

        self.success_label = None
        
        self.create_main_frame()
        self.create_settings_frame()
        
        self.settings_frame.place_forget()

        self.laptop_icon = ctk.CTkImage(light_image=Image.open("laptop.png"), size=(24, 24))
        self.box_icon = ctk.CTkImage(light_image=Image.open("box.png"), size=(24, 24))
        
    def create_main_frame(self):
        self.main_frame = ctk.CTkFrame(self.root, corner_radius=0)
        self.main_frame.pack(fill="both", expand=True)
        
        header_frame = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(20, 0))
        
        title_label = ctk.CTkLabel(
            header_frame, 
            text="ETS Equipment Sheet Printing", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(side="left")
        
        # Settings Button
        self.settings_button = ctk.CTkButton(
            header_frame,
            text="Settings",
            width=80,
            height=40,
            corner_radius=10,
            command=self.toggle_settings
        )
        self.settings_button.pack(side="right")
        
        center_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        center_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        input_frame = ctk.CTkFrame(center_frame, fg_color="transparent")
        input_frame.pack(expand=True)
        
        input_label = ctk.CTkLabel(
            input_frame, 
            text="Enter Ticket Number:", 
            font=ctk.CTkFont(size=18)
        )
        input_label.pack(pady=(0, 10))
        
        self.input_entry = ctk.CTkEntry(
            input_frame,
            width=250,
            height=62,
            placeholder_text="0000000",
            font=ctk.CTkFont(size=36),
            justify="center"
        )
        self.input_entry.pack(pady=(0, 10))

        # Bind events to clean input as user types or pastes
        self.input_entry.bind("<KeyRelease>", lambda event: self.clean_input())
        self.input_entry.bind("<<Paste>>", lambda event: self.root.after(10, self.clean_input))
        self.input_entry.bind("<Up>", lambda event: self.navigate_history(up=True))
        self.input_entry.bind("<Down>", lambda event: self.navigate_history(up=False))


        device_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        device_frame.pack(expand=True, pady=(0, 10))
        
        self.device_selector = ctk.CTkSegmentedButton(
            device_frame,
            values=["Normal", "Laptop"],
            variable=self.device_var,
            command=lambda value: print(f"Device selected: {value}"),
        )
        self.device_selector.pack()
        self.device_selector.set("Normal")
        
        submit_button = ctk.CTkButton(
            input_frame,
            text="Submit",
            font=ctk.CTkFont(size=16),
            width=120,
            height=40,
            command=self.process_input
        )
        submit_button.pack(pady=(0, 10))
        
        # Success message label at bottom
        self.success_label = ctk.CTkLabel(
            self.main_frame,
            text="",
            font=ctk.CTkFont(size=14),
            text_color="green"
        )
        self.success_label.pack(side="bottom", pady=20)

        self.input_entry.bind("<Return>", lambda event: self.process_input())
        self.input_entry.focus_set()
        
    def create_settings_frame(self):
        self.settings_frame = ctk.CTkFrame(self.root, corner_radius=10)
        self.settings_frame.place(relx=0.5, rely=0.5, relwidth=0.8, relheight=0.8, anchor="center")
        
        settings_header = ctk.CTkFrame(self.settings_frame, corner_radius=0, fg_color="transparent")
        settings_header.pack(fill="x", padx=20, pady=20)
        
        settings_title = ctk.CTkLabel(
            settings_header, 
            text="Settings", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        settings_title.pack(side="left")
        
        close_button = ctk.CTkButton(
            settings_header,
            text="X",
            width=30,
            height=30,
            corner_radius=15,
            command=lambda: self.settings_frame.place_forget()
        )
        close_button.pack(side="right")
        
        settings_content = ctk.CTkFrame(self.settings_frame, fg_color="transparent")
        settings_content.pack(fill="both", expand=True, padx=30, pady=(0, 30))
        
        settings = [
            ("Printer Name:", self.setting1),
            ("API Public Key:", self.setting2),
            ("API Private Key:", self.setting3),
        ]
        
        for i, (label_text, var) in enumerate(settings):
            frame = ctk.CTkFrame(settings_content, fg_color="transparent")
            frame.pack(fill="x", pady=10)
            
            label = ctk.CTkLabel(frame, text=label_text, width=100, anchor="w")
            label.pack(side="left")
            
            entry = ctk.CTkEntry(frame, textvariable=var)
            entry.pack(side="left", fill="x", expand=True, padx=(10, 0))
        
        checkbox_frame = ctk.CTkFrame(settings_content, fg_color="transparent")
        checkbox_frame.pack(fill="x", pady=10)
        
        checkbox = ctk.CTkCheckBox(
            checkbox_frame, 
            text="Fullscreen Mode", 
            variable=self.checkbox_var,
            command=self.toggle_fullscreen
        )
        checkbox.pack(side="left")
        
        save_frame = ctk.CTkFrame(settings_content, fg_color="transparent")
        save_frame.pack(fill="x", pady=(20, 0))
        
        save_button = ctk.CTkButton(
            save_frame, 
            text="Save Settings",
            command=self.save_settings
        )
        save_button.pack(side="right")
    
    def toggle_settings(self):
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.py")
        try:
            # Read the current printer_name from config.py
            with open(config_path, "r") as file:
                for line in file:
                    if line.startswith("printer_name ="):
                        current_printer_name = line.split("=", 1)[1].strip().strip('"')
                        self.setting1.set(current_printer_name)
                        break
        except Exception as e:
            self.show_error(f"Failed to load settings: {e}")
    
        # Toggle the visibility of the settings frame
        if self.settings_frame.winfo_viewable():
            self.settings_frame.place_forget()
        else:
            self.settings_frame.place(relx=0.5, rely=0.5, relwidth=0.8, relheight=0.8, anchor="center")
    
    def toggle_fullscreen(self, full=None):
        if self.checkbox_var.get() and (full is None or full is False):
            self.root.attributes('-fullscreen', True)
            self.checkbox_var.set(True)
        else:
            self.root.attributes('-fullscreen', False)
            self.root.geometry("1000x700")
            self.checkbox_var.set(False)

    def show_success_message(self):
        self.success_label.configure(text="Ticket Number Processed Successfully")
        self.root.after(5000, lambda: self.success_label.configure(text=""))

    def clean_input(self):
        current = self.input_entry.get()
        cleaned = "".join(char for char in current if char.isdigit())
        if current != cleaned:
            self.input_entry.delete(0, "end")
            self.input_entry.insert(0, cleaned)

    def fill_last_input(self):
        if self.last_input:
            self.input_entry.delete(0, "end")
            self.input_entry.insert(0, self.last_input)

    
    def process_input(self):
        user_input = self.input_entry.get()
        if len(user_input) != 7 or not user_input.isdigit():
            self.show_error("Please enter a valid 7-digit Ticket Number")
            return
        
        # Add "L" prefix for Laptop tickets
        device_type = self.device_var.get()
        ticket_input = f"L{user_input}" if device_type == "Laptop" else user_input
        
        # Call backend processing
        from LabelPrintingBackend import process_ticket
        base_dir = os.path.dirname(os.path.abspath(__file__))
        success, message = process_ticket(ticket_input, device_type, base_dir)
        
        if success:
            self.input_history.append(user_input)
            self.history_index = None  # Reset history navigation
            self.input_entry.delete(0, tk.END)
            self.input_entry.focus_set()
            self.show_success_message()
        else:
            self.show_error(message)

    def navigate_history(self, up=True):
        if not self.input_history:
            return

        if self.history_index is None:
            self.history_index = len(self.input_history)

        if up:
            self.history_index = max(0, self.history_index - 1)
        else:
            self.history_index = min(len(self.input_history), self.history_index + 1)

        if self.history_index < len(self.input_history):
            value = self.input_history[self.history_index]
            self.input_entry.delete(0, "end")
            self.input_entry.insert(0, value)
        else:
            self.input_entry.delete(0, "end")  # Clear if past the end

            
    def save_settings(self):
        # Update the printer_name in config.py
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.py")
        try:
            with open(config_path, "r") as file:
                lines = file.readlines()
            
            # Check if public_key or private_key has been modified
            public_key_changed = False
            private_key_changed = False
            for line in lines:
                if self.setting2.get():  # Only check if setting2 is not empty
                    if line.startswith("public_key =") and f'"{self.setting2.get()}"' not in line:
                        public_key_changed = True
                if self.setting3.get():  # Only check if setting3 is not empty
                    if line.startswith("private_key =") and f'"{self.setting3.get()}"' not in line:
                        private_key_changed = True

            # If either key is changed, prompt for a password
            if public_key_changed or private_key_changed:
                password_window = tk.Toplevel(self.root)
                password_window.title("Password Required")
                password_window.geometry("300x150")
                password_window.resizable(False, False)

                frame = ctk.CTkFrame(password_window)
                frame.pack(fill="both", expand=True, padx=20, pady=20)

                label = ctk.CTkLabel(frame, text="Enter Password:", font=ctk.CTkFont(size=14))
                label.pack(pady=(0, 10))

                password_entry = ctk.CTkEntry(frame, show="*", width=200)
                password_entry.pack(pady=(0, 10))

                def verify_password():
                    if password_entry.get() == "etsAdmin":  # Replace with your actual password
                        password_window.destroy()
                        self._write_config_file(lines, public_key_changed, private_key_changed)
                    else:
                        self.show_error("Incorrect password. Changes not saved.")
                        password_window.destroy()

                submit_button = ctk.CTkButton(frame, text="Submit", command=verify_password)
                submit_button.pack(pady=(10, 0))

                return  # Exit the method until password is verified

            # If no keys were changed, save settings directly
            self._write_config_file(lines)

        except Exception as e:
            self.show_error(f"Failed to save settings: {e}")

    def _write_config_file(self, lines, public_key_changed=False, private_key_changed=False):
        """Helper method to write updated settings to config.py."""
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.py")
        with open(config_path, "w") as file:
            for line in lines:
                if line.startswith("printer_name ="):
                    file.write(f'printer_name = "{self.setting1.get()}"\n')
                    print(f"Printer Name: {self.setting1.get()}")
                elif line.startswith("public_key =") and public_key_changed:
                    file.write(f'public_key = "{self.setting2.get()}"\n')
                    print(f"Public Key: {self.setting2.get()}")
                    self.setting2.set("")  # Clear the entry after saving
                elif line.startswith("private_key =") and private_key_changed:
                    file.write(f'private_key = "{self.setting3.get()}"\n')
                    print(f"Private Key: {self.setting3.get()}")
                    self.setting3.set("")  # Clear the entry after saving
                else:
                    file.write(line)

        print("Settings saved successfully.")
        
        self.settings_frame.place_forget()

    def show_error(self, message):
        error_window = tk.Toplevel(self.root)
        error_window.title("Error")
        error_window.geometry("600x400")
        error_window.resizable(False, False)
        
        frame = ctk.CTkFrame(error_window)
        frame.pack(fill="both", expand=True)
        
        label = ctk.CTkLabel(
            frame,
            text=message,
            font=ctk.CTkFont(size=14),
            wraplength=250
        )
        label.pack(pady=(20, 10))
        
        button = ctk.CTkButton(
            frame,
            text="OK",
            width=80,
            command=error_window.destroy
        )
        button.pack(pady=(0, 10))

def main():
    root = ctk.CTk()
    app = ModernApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()