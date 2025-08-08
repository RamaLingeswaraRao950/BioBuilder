import tkinter as tk
from tkinter import messagebox
from datetime import date


class IntroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BioBuilder")

        # Get screen size and position the main window to the left
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        win_w, win_h = 600, 700
        x_pos = 50
        y_pos = (screen_h // 2) - (win_h // 2)
        self.root.geometry(f"{win_w}x{win_h}+{x_pos}+{y_pos}")
        self.root.resizable(False, False)

        # Themes
        self.light_theme = {
            "bg": "#ffffff", "fg": "#000000", "entry_bg": "#f0f0f0",
            "btn_bg": "#d0e6ff", "btn_hover": "#b0d4ff"
        }
        self.dark_theme = {
            "bg": "#2c2c2c", "fg": "#ffffff", "entry_bg": "#444444",
            "btn_bg": "#4a90e2", "btn_hover": "#357ab8"
        }

        self.current_theme = self.light_theme
        self.secondary_window = None

        self.create_widgets()
        self.apply_theme()

    def create_widgets(self):
        self.title_label = tk.Label(
            self.root, text="🧑‍💻 BioBuilder ", font=("Helvetica", 18, "bold"))
        self.title_label.pack(pady=20)

        self.form_frame = tk.Frame(self.root)
        self.form_frame.pack(pady=10)

        self.entries = {}
        self.fields = [
            "Name", "Age", "Father's Name", "Mother's Name",
            "City", "Profession", "Education", "Hobby", "Siblings"
        ]

        for i, field in enumerate(self.fields):
            label = tk.Label(
                self.form_frame, text=f"{field}:", font=("Helvetica", 12))
            label.grid(row=i, column=0, sticky="e", padx=10, pady=5)

            if field == "Siblings":
                entry = tk.Entry(
                    self.form_frame, font=("Helvetica", 12), width=30,
                    validate="key", validatecommand=(self.root.register(self.validate_siblings), "%P")
                )
            elif field == "Age":
                entry = tk.Entry(
                    self.form_frame, font=("Helvetica", 12), width=30,
                    validate="key", validatecommand=(self.root.register(self.validate_age), "%P")
                )
            else:
                entry = tk.Entry(self.form_frame, font=(
                    "Helvetica", 12), width=30)

            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entries[field.lower()] = entry

        self.main_button_frame = tk.Frame(self.root)
        self.main_button_frame.pack(pady=15)

        self.generate_btn = self.create_button(
            self.main_button_frame, "📝 Generate ", self.generate_intro)
        self.generate_btn.pack(side="left", padx=10)

        self.theme_btn = self.create_button(
            self.main_button_frame, "🌙 Mode", self.toggle_theme)
        self.theme_btn.pack(side="left", padx=10)

    def create_button(self, parent, text, command):
        btn = tk.Button(parent, text=text, command=command,
                        font=("Helvetica", 11, "bold"), relief="flat")
        btn.bind("<Enter>", lambda e, b=btn: self.on_button_hover(b))
        btn.bind("<Leave>", lambda e, b=btn: self.on_button_leave(b))
        btn.bind("<ButtonPress-1>", lambda e, b=btn: self.on_button_press(b))
        btn.bind("<ButtonRelease-1>", lambda e,
                 b=btn: self.on_button_release(b))
        return btn

    def on_button_hover(self, btn):
        btn.configure(bg=self.current_theme["btn_hover"])

    def on_button_leave(self, btn):
        btn.configure(bg=self.current_theme["btn_bg"], font=(
            "Helvetica", 11, "bold"))

    def on_button_press(self, btn):
        btn.configure(font=("Helvetica", 10, "bold"))

    def on_button_release(self, btn):
        btn.configure(font=("Helvetica", 11, "bold"))

    def validate_siblings(self, value):
        if value == "":
            return True
        if value.isdigit():
            if len(value) > 1 and value.startswith("0"):
                return False
            return int(value) < 15
        return False

    def validate_age(self, value):
        if value == "":
            return True
        if value.isdigit():
            if len(value) > 1 and value.startswith("0"):
                return False
            return int(value) < 90
        return False

    def apply_theme(self):
        theme = self.current_theme
        self.root.configure(bg=theme["bg"])
        self.title_label.configure(bg=theme["bg"], fg=theme["fg"])
        self.form_frame.configure(bg=theme["bg"])
        self.main_button_frame.configure(bg=theme["bg"])

        self.generate_btn.configure(bg=theme["btn_bg"], fg=theme["fg"])
        self.theme_btn.configure(bg=theme["btn_bg"], fg=theme["fg"])

        for widget in self.form_frame.winfo_children():
            if isinstance(widget, tk.Label):
                widget.configure(bg=theme["bg"], fg=theme["fg"])

        for entry in self.entries.values():
            entry.configure(
                bg=theme["entry_bg"], fg=theme["fg"], insertbackground=theme["fg"])

        if self.secondary_window and self.secondary_window.winfo_exists():
            self.secondary_window.configure(bg=theme["bg"])
            self.result_label.configure(bg=theme["bg"], fg=theme["fg"])
            self.copy_btn.configure(bg=theme["btn_bg"], fg=theme["fg"])
            self.close_btn.configure(bg=theme["btn_bg"], fg=theme["fg"])
            self.button_frame.configure(bg=theme["bg"])

    def toggle_theme(self):
        self.current_theme = self.dark_theme if self.current_theme == self.light_theme else self.light_theme
        self.apply_theme()

    def starts_with_capital(self, text):
        return text and text[0].isupper()

    def is_min_length(self, text, min_length=3):
        return len(text) >= min_length

    def generate_intro(self):
        data = {k: v.get().strip() for k, v in self.entries.items()}

        for field in self.fields:
            key = field.lower()
            if not data[key]:
                messagebox.showerror("Input Error", f"{field} is required.")
                return

        if not data["age"].isdigit() or int(data["age"]) >= 90 or (len(data["age"]) > 1 and data["age"].startswith("0")):
            messagebox.showerror(
                "Input Error", "Age must be an integer less than 90 and cannot have leading zeros.")
            return

        if not data["siblings"].isdigit() or int(data["siblings"]) >= 15 or (len(data["siblings"]) > 1 and data["siblings"].startswith("0")):
            messagebox.showerror(
                "Input Error", "Siblings must be an integer less than 15 and cannot have leading zeros.")
            return

        for field in self.fields:
            key = field.lower()
            if key not in ["age", "siblings"]:
                if not self.is_min_length(data[key]):
                    messagebox.showerror(
                        "Input Error", f"{field} must be at least 3 characters long.")
                    return
                if not self.starts_with_capital(data[key]):
                    messagebox.showerror(
                        "Input Error", f"{field} must start with a capital letter.")
                    return

        today = date.today().isoformat()
        intro = (
            f"Hello! My name is {data['name']}. I'm {data['age']} years old. "
            f"My father's name is {data['father\'s name']} and my mother's name is {data['mother\'s name']}. "
            f"I live in {data['city']} and work as a {data['profession']}. "
            f"I completed my education in {data['education']} and enjoy {data['hobby']}. "
            f"I have {data['siblings']} sibling(s). "
            f"Nice to meet you!\n\nLogged on: {today}"
        )

        self.show_secondary_window(intro)

    def show_secondary_window(self, intro_text):
        if self.secondary_window and self.secondary_window.winfo_exists():
            self.secondary_window.destroy()

        # Position preview window at right side
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        win_w, win_h = 500, 300
        x_pos = screen_w - win_w - 50
        y_pos = (screen_h // 2) - (win_h // 2)

        self.secondary_window = tk.Toplevel(self.root)
        self.secondary_window.title("📄 BioBuilder Preview")
        self.secondary_window.geometry(f"{win_w}x{win_h}+{x_pos}+{y_pos}")
        self.secondary_window.resizable(False, False)
        self.secondary_window.configure(bg=self.current_theme["bg"])

        self.result_label = tk.Label(
            self.secondary_window,
            text=intro_text,
            justify="left",
            font=("Courier New", 11),
            bg=self.current_theme["bg"],
            fg=self.current_theme["fg"],
            wraplength=480
        )
        self.result_label.pack(padx=10, pady=10, fill="both", expand=True)

        self.button_frame = tk.Frame(
            self.secondary_window, bg=self.current_theme["bg"])
        self.button_frame.pack(pady=5)

        self.copy_btn = self.create_button(
            self.button_frame, "📋 Copy ", lambda: self.copy_to_clipboard(
                intro_text)
        )
        self.copy_btn.pack(side="left", padx=10)

        self.close_btn = self.create_button(
            self.button_frame, "❌ Close ", self.close_both_windows
        )
        self.close_btn.pack(side="left", padx=10)

        self.apply_theme()

    def close_both_windows(self):
        if self.secondary_window and self.secondary_window.winfo_exists():
            self.secondary_window.destroy()
        self.root.destroy()

    def copy_to_clipboard(self, text):
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.root.update()
        messagebox.showinfo("Copied", "Intro copied to clipboard!")


if __name__ == "__main__":
    root = tk.Tk()
    app = IntroApp(root)
    root.mainloop()
