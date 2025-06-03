import tkinter as tk
import customtkinter as ctk
import os
import LabelPrinting_Backend as backend

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class LabelPrinterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ETS Equipment Sheet Printing")
        self.root.geometry("1000x700")
        self.root.attributes('-fullscreen', False)
        
        self.setting1 = tk.StringVar()
        self.setting2 = tk.StringVar()
        self.setting3 = tk.StringVar()
        self.setting4 = tk.StringVar()
        self.setting5 = tk.StringVar()
        self.setting6 = tk.StringVar()
        self.checkbox_var = tk.BooleanVar(value=True)
        self.device_var = tk.StringVar(value="Normal")
        
        # Sets up the up and down arrow history navigation
        self.input_history = []
        self.history_index = None

        self.root.bind("<Escape>", lambda event: self.toggle_fullscreen(full=True))

        self.success_label = None
        
        self.create_main_frame()
        self.create_settings_frame()
        
        self.settings_frame.place_forget()

        baseUrl, headers, baseDir = backend.initialize()
        
    def create_main_frame(self):
        self.main_frame = ctk.CTkFrame(self.root, corner_radius=10)
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
            placeholder_text="3965678",
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
        self.settings_frame = ctk.CTkFrame(self.root, corner_radius=10, fg_color="#494949")
        self.settings_frame.place(relx=0.5, rely=0.5, relwidth=0.8, relheight=0.8, anchor="center")
        
        settings_header = ctk.CTkFrame(self.settings_frame, corner_radius=10, fg_color="transparent")
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
            corner_radius=10,
            command=lambda: self.settings_frame.place_forget()
        )
        close_button.pack(side="right")
        
        settings_content = ctk.CTkFrame(self.settings_frame, fg_color="transparent")
        settings_content.pack(fill="both", expand=True, padx=30, pady=(0, 30))
        
        settings = [
            ("Printer Name:", self.setting1),
            ("Laptop Template Name:", self.setting4),
            ("Normal Template Name:", self.setting5),
            ("Completed File Name:", self.setting6),
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
            fullscreen_mode = self.root.attributes('-fullscreen')
            self.checkbox_var.set(fullscreen_mode)  # Sync checkbox with actual fullscreen state

            # Read the current settings from config.py
            with open(config_path, "r") as file:
                for line in file:
                    if line.startswith("printerName ="):
                        current_printer_name = line.split("=", 1)[1].strip().strip('"')
                        self.setting1.set(current_printer_name)
                    elif line.startswith("templateNormal ="):
                        current_template_normal = line.split("=", 1)[1].strip().strip('"')
                        self.setting5.set(current_template_normal)
                    elif line.startswith("templateLaptop ="):
                        current_template_laptop = line.split("=", 1)[1].strip().strip('"')
                        self.setting4.set(current_template_laptop)
                    elif line.startswith("templateFilled ="):
                        current_template_filled = line.split("=", 1)[1].strip().strip('"')
                        self.setting6.set(current_template_filled)
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

    def process_input(self):
        user_input = self.input_entry.get()
        if len(user_input) != 7 or not user_input.isdigit():
            self.show_error("Please enter a valid 7-digit Ticket Number")
            return
        
        # Add "L" prefix for Laptop tickets
        device_type = self.device_var.get()
        ticket_input = f"L{user_input}" if device_type == "Laptop" else user_input
        
        # Call backend processing
        success, message = backend.process_ticket(self.baseUrl, self.headers, self.baseDir, user_input, device_type == "Laptop")
        
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
            
            # Check if publicKey or privateKey has been modified
            public_key_changed = False
            private_key_changed = False
            for line in lines:
                if self.setting2.get():  # Only check if setting2 is not empty
                    if line.startswith("publicKey =") and f'"{self.setting2.get()}"' not in line:
                        public_key_changed = True
                if self.setting3.get():  # Only check if setting3 is not empty
                    if line.startswith("privateKey =") and f'"{self.setting3.get()}"' not in line:
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
                if line.startswith("printerName ="):
                    file.write(f'printerName = "{self.setting1.get()}"\n')
                    print(f"Printer Name: {self.setting1.get()}")
                elif line.startswith("publicKey =") and public_key_changed:
                    file.write(f'publicKey = "{self.setting2.get()}"\n')
                    print(f"Public Key: {self.setting2.get()}")
                    self.setting2.set("")  # Clear the entry after saving
                elif line.startswith("privateKey =") and private_key_changed:
                    file.write(f'privateKey = "{self.setting3.get()}"\n')
                    print(f"Private Key: {self.setting3.get()}")
                    self.setting3.set("")  # Clear the entry after saving
                elif line.startswith("templateLaptop ="):
                    file.write(f'templateLaptop = "{self.setting4.get()}"\n')
                    print(f"Laptop Template: {self.setting4.get()}")
                elif line.startswith("templateNormal ="):
                    file.write(f'templateNormal = "{self.setting5.get()}"\n')
                    print(f"Normal Template: {self.setting5.get()}")
                elif line.startswith("templateFilled ="):
                    file.write(f'templateFilled = "{self.setting6.get()}"\n')
                    print(f"Completed File Name: {self.setting6.get()}")
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
    app = LabelPrinterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()