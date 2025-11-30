# ui_components.py
import tkinter as tk
from tkinter import ttk, messagebox
import datetime

LIGHT = {
    "bg": "#F3F4F6",
    "card_bg": "#FFFFFF",
    "fg": "#111827",
    "muted": "#6B7280",
    "accent": "#2563EB",
    "tag_bg": "#E5E7EB",
}

DARK = {
    "bg": "#0F172A",
    "card_bg": "#0B1220",
    "fg": "#E6EEF8",
    "muted": "#9AA6B2",
    "accent": "#60A5FA",
    "tag_bg": "#1F2937",
}

def format_now_date():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def create_tag_label(parent, text, theme):
    lbl = tk.Label(
        parent,
        text=text,
        bg=theme["tag_bg"],
        fg=theme["fg"],
        padx=8,
        pady=3,
        font=("Segoe UI", 9)
    )
    return lbl


# ============================
# Volunteer Card
# ============================
class VolunteerCard(tk.Frame):
    def __init__(self, parent, data, delete_callback, edit_callback, theme_getter):
        super().__init__(parent)
        self.data = data
        self.delete_callback = delete_callback
        self.edit_callback = edit_callback
        self.theme_getter = theme_getter
        self.build_card()

    def build_card(self):
        for w in self.winfo_children():
            w.destroy()
        t = self.theme_getter()
        self.configure(bg=t["card_bg"], bd=1, relief="flat")
        outer = tk.Frame(self, bg=t["card_bg"])
        outer.pack(fill="x", padx=10, pady=8)

        top = tk.Frame(outer, bg=t["card_bg"])
        top.pack(fill="x")

        tk.Label(top, text=self.data["name"], font=("Segoe UI Semibold", 13),
                 bg=t["card_bg"], fg=t["fg"]).pack(side="left")

        btns = tk.Frame(top, bg=t["card_bg"])
        btns.pack(side="right")
        tk.Button(btns, text="✏", bg=t["card_bg"], fg=t["accent"], bd=0,
                  command=self.on_edit).pack(side="left", padx=4)
        tk.Button(btns, text="🗑", bg=t["card_bg"], fg="#F43F5E", bd=0,
                  command=self.on_delete).pack(side="left")

        # Info
        info = tk.Frame(outer, bg=t["card_bg"])
        info.pack(fill="x", pady=(6, 0))
        tk.Label(info, text=f"✉  {self.data['email']}", bg=t["card_bg"], fg=t["fg"]).pack(anchor="w")
        tk.Label(info, text=f"📞  {self.data['phone']}", bg=t["card_bg"], fg=t["fg"]).pack(anchor="w")
        tk.Label(info, text=f"🗓  Registered: {self.data['registered']}",
                 bg=t["card_bg"], fg=t["muted"]).pack(anchor="w")

        # Interests
        interest_frame = tk.Frame(outer, bg=t["card_bg"])
        interest_frame.pack(fill="x", pady=(8, 0))
        tk.Label(interest_frame, text="Areas of Interest:", bg=t["card_bg"], fg=t["fg"]).pack(anchor="w")
        wrap = tk.Frame(interest_frame, bg=t["card_bg"])
        wrap.pack(anchor="w", pady=6)
        for tag in self.data["interests"]:
            lbl = create_tag_label(wrap, tag, t)
            lbl.pack(side="left", padx=4, pady=2)

        bottom = tk.Frame(outer, bg=t["card_bg"])
        bottom.pack(fill="x", pady=(6, 0))
        tk.Label(bottom, text=f"📅  {self.data['availability']}", bg=t["card_bg"], fg=t["fg"]).pack(side="left")
        tk.Label(bottom, text=f"🔱  {self.data['experience']}", bg=t["card_bg"], fg=t["fg"]).pack(side="left", padx=28)

        msg_frame = tk.Frame(outer, bg=t["card_bg"])
        msg_frame.pack(fill="x", pady=(8, 6))
        tk.Label(msg_frame, text="Message:", bg=t["card_bg"], fg=t["fg"]).pack(anchor="w")
        tk.Label(msg_frame, text=self.data["message"], bg=t["card_bg"],
                 fg=t["muted"], wraplength=420).pack(anchor="w", pady=4)

    def on_delete(self):
        if messagebox.askyesno("Confirm", f"Delete {self.data['name']}?"):
            self.delete_callback(self)

    def on_edit(self):
        self.edit_callback(self)


# ============================
# Edit Dialog with Dropdowns
# ============================
class EditDialog(tk.Toplevel):
    def __init__(self, parent, data, on_save, theme_getter, availability_options=None, experience_options=None):
        super().__init__(parent)
        self.data = dict(data)
        self.on_save = on_save
        self.theme_getter = theme_getter
        self.availability_options = availability_options or []
        self.experience_options = experience_options or []
        self.title("Edit Volunteer")
        self.resizable(False, False)
        self.grab_set()
        self.build()

    def build(self):
        t = self.theme_getter()
        self.configure(bg=t["bg"], padx=10, pady=10)
        frm = tk.Frame(self, bg=t["bg"])
        frm.pack(fill="both")

        # Fields
        self.name_var = tk.StringVar(value=self.data.get("name", ""))
        self.email_var = tk.StringVar(value=self.data.get("email", ""))
        self.phone_var = tk.StringVar(value=self.data.get("phone", ""))
        self.reg_var = tk.StringVar(value=self.data.get("registered", format_now_date()))
        self.avail_var = tk.StringVar(value=self.data.get("availability", self.availability_options[0] if self.availability_options else ""))
        self.exp_var = tk.StringVar(value=self.data.get("experience", self.experience_options[0] if self.experience_options else ""))

        tk.Label(frm, text="Name:", bg=t["bg"], fg=t["fg"]).grid(row=0, column=0, sticky="w", pady=4)
        tk.Entry(frm, textvariable=self.name_var, width=40).grid(row=0, column=1, sticky="w", pady=4)

        tk.Label(frm, text="Email:", bg=t["bg"], fg=t["fg"]).grid(row=1, column=0, sticky="w", pady=4)
        tk.Entry(frm, textvariable=self.email_var, width=40).grid(row=1, column=1, sticky="w", pady=4)

        tk.Label(frm, text="Phone:", bg=t["bg"], fg=t["fg"]).grid(row=2, column=0, sticky="w", pady=4)
        tk.Entry(frm, textvariable=self.phone_var, width=40).grid(row=2, column=1, sticky="w", pady=4)

        tk.Label(frm, text="Registered:", bg=t["bg"], fg=t["fg"]).grid(row=3, column=0, sticky="w", pady=4)
        tk.Entry(frm, textvariable=self.reg_var, width=40).grid(row=3, column=1, sticky="w", pady=4)

        # ───── Dropdowns ─────
        tk.Label(frm, text="Availability:", bg=t["bg"], fg=t["fg"]).grid(row=4, column=0, sticky="w", pady=4)
        self.avail_cb = ttk.Combobox(frm, textvariable=self.avail_var, values=self.availability_options, state="readonly", width=38)
        self.avail_cb.grid(row=4, column=1, sticky="w", pady=4)

        tk.Label(frm, text="Experience:", bg=t["bg"], fg=t["fg"]).grid(row=5, column=0, sticky="w", pady=4)
        self.exp_cb = ttk.Combobox(frm, textvariable=self.exp_var, values=self.experience_options, state="readonly", width=38)
        self.exp_cb.grid(row=5, column=1, sticky="w", pady=4)

        # Message
        tk.Label(frm, text="Message:", bg=t["bg"], fg=t["fg"]).grid(row=6, column=0, sticky="nw")
        self.msg_text = tk.Text(frm, width=30, height=4)
        self.msg_text.grid(row=6, column=1, pady=4)
        self.msg_text.insert("1.0", self.data.get("message", ""))

        # Interests
        self.interests = list(self.data.get("interests", []))
        tag_frame = tk.Frame(frm, bg=t["bg"])
        tag_frame.grid(row=7, column=1, sticky="w", pady=4)
        self.tags_display = tk.Frame(tag_frame, bg=t["bg"])
        self.tags_display.pack()
        add_tag_frame = tk.Frame(tag_frame, bg=t["bg"])
        add_tag_frame.pack(pady=4)
        self.new_tag = tk.StringVar()
        tk.Entry(add_tag_frame, textvariable=self.new_tag, width=28).pack(side="left")
        tk.Button(add_tag_frame, text="Add Tag", command=self.add_tag).pack(side="left", padx=6)
        self.render_tags()

        # Buttons
        btns = tk.Frame(frm, bg=t["bg"])
        btns.grid(row=8, column=0, columnspan=2, pady=10)
        tk.Button(btns, text="Save", bg=t["accent"], fg="white", command=self.save).pack(side="left", padx=4)
        tk.Button(btns, text="Cancel", command=self.destroy).pack(side="left", padx=4)

    def render_tags(self):
        for w in self.tags_display.winfo_children():
            w.destroy()
        t = self.theme_getter()
        for tag in self.interests:
            row = tk.Frame(self.tags_display, bg=t["bg"])
            row.pack(side="left", padx=4)
            create_tag_label(row, tag, t).pack(side="left")
            tk.Button(row, text="x", bg=t["bg"], fg="#F87171", bd=0,
                      command=lambda x=tag: self.remove_tag(x)).pack(side="left")

    def add_tag(self):
        tag = self.new_tag.get().strip()
        if tag and tag not in self.interests:
            self.interests.append(tag)
            self.new_tag.set("")
            self.render_tags()

    def remove_tag(self, tag):
        if tag in self.interests:
            self.interests.remove(tag)
            self.render_tags()

    def save(self):
        self.data.update({
            "name": self.name_var.get().strip(),
            "email": self.email_var.get().strip(),
            "phone": self.phone_var.get().strip(),
            "registered": self.reg_var.get().strip(),
            "availability": self.avail_var.get(),
            "experience": self.exp_var.get(),
            "message": self.msg_text.get("1.0", "end").strip(),
            "interests": self.interests[:],
        })
        self.on_save(self.data)
        self.destroy()
