# app.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import csv
from ui_compo import LIGHT, DARK, VolunteerCard, EditDialog, format_now_date


class VolunteerApp:
    def __init__(self, root):
        self.root = root
        self.theme = DARK.copy()

        self.root.title("Volunteer Manager")
        self.root.geometry("600x720")
        self.root.configure(bg=self.theme["bg"])

        self.volunteer_data = []
        self.card_widgets = []

        self.availability_options = ["Weekdays", "Weekends", "Both Weekends and Weekdays", "Flexible"]
        self.experience_options = ["No prior experience", "Some experience", "Experienced ", ""]

        # ───── Top Bar ─────
        top = tk.Frame(root, bg=self.theme["bg"])
        top.pack(fill="x", padx=12, pady=10)

        self.search_var = tk.StringVar()
        search = tk.Entry(top, textvariable=self.search_var, width=36)
        search.pack(side="left", padx=(0, 8))
        search.bind("<KeyRelease>", lambda e: self.render_cards())

        tk.Button(top, text="Search", command=self.render_cards).pack(side="left", padx=4)
        tk.Button(top, text="+ Add Volunteer", bg=self.theme["accent"], fg="white",
                  command=self.create_volunteer).pack(side="left", padx=4)
        tk.Button(top, text="Export CSV", command=self.export_csv).pack(side="left", padx=4)

        self.dark = tk.Button(top, text="Toggle Dark Mode", command=self.toggle)
        self.dark.pack(side="right")

        # ───── Scroll Container ─────
        container = tk.Frame(root, bg=self.theme["bg"])
        container.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        self.canvas = tk.Canvas(container, bg=self.theme["bg"], highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.scroll_frame = tk.Frame(self.canvas, bg=self.theme["bg"])

        self.scroll_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.autosave_path = "volunteers.csv"
        self.load_autosave()
        self.render_cards()

    # ───── Theme ─────
    def theme_getter(self):
        return self.theme

    def toggle(self):
        self.theme = DARK.copy() if self.theme == LIGHT else LIGHT.copy()
        self.root.configure(bg=self.theme["bg"])
        self.canvas.configure(bg=self.theme["bg"])
        self.scroll_frame.configure(bg=self.theme["bg"])
        self.render_cards()

    # ───── Add Volunteer ─────
    def create_volunteer(self):
        new = {
            "name": "",
            "email": "",
            "phone": "",
            "registered": format_now_date(),
            "interests": [],
            "availability": self.availability_options[0],
            "experience": self.experience_options[0],
            "message": ""
        }

        def save_cb(updated):
            if not updated["name"].strip():
                messagebox.showerror("Validation", "Name is required.")
                return
            self.volunteer_data.append(updated)
            self.render_cards()
            self.autosave()

        EditDialog(
            self.root, new, save_cb, self.theme_getter,
            availability_options=self.availability_options,
            experience_options=self.experience_options
        )

    # ───── Delete ─────
    def delete(self, card):
        i = self.card_widgets.index(card)
        self.volunteer_data.pop(i)
        self.render_cards()
        self.autosave()

    # ───── Edit ─────
    def edit(self, card):
        i = self.card_widgets.index(card)
        data = self.volunteer_data[i]

        def save_cb(updated):
            if not updated["name"].strip():
                messagebox.showerror("Validation", "Name is required.")
                return
            self.volunteer_data[i] = updated
            self.render_cards()
            self.autosave()

        EditDialog(
            self.root, data, save_cb, self.theme_getter,
            availability_options=self.availability_options,
            experience_options=self.experience_options
        )

    # ───── Render Cards ─────
    def render_cards(self):
        q = self.search_var.get().lower().strip()

        for c in self.card_widgets:
            c.destroy()
        self.card_widgets.clear()

        if q:
            candidates = [d for d in self.volunteer_data if
                          q in " ".join([d["name"], d["email"], " ".join(d["interests"]), d["message"]]).lower()]
        else:
            candidates = self.volunteer_data[:]

        for d in candidates:
            card = VolunteerCard(self.scroll_frame, d, self.delete, self.edit, self.theme_getter)
            card.pack(fill="x", pady=6)
            self.card_widgets.append(card)

    # ───── CSV Export ─────
    def export_csv(self):
        if not self.volunteer_data:
            messagebox.showinfo("No Data", "Nothing to export.")
            return

        f = filedialog.asksaveasfilename(defaultextension=".csv")
        if not f:
            return

        self.write_csv(f)
        messagebox.showinfo("Exported", "CSV saved!")

    # ───── Autosave ─────
    def autosave(self):
        self.write_csv(self.autosave_path)

    def load_autosave(self):
        try:
            with open(self.autosave_path, newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    row["interests"] = row["interests"].split(";") if row["interests"] else []
                    self.volunteer_data.append(row)
        except FileNotFoundError:
            pass
        self.render_cards()

    def write_csv(self, path):
        keys = ["name", "email", "phone", "registered", "availability", "experience", "message", "interests"]
        with open(path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(keys)
            for d in self.volunteer_data:
                writer.writerow([
                    d[k] if k != "interests" else ";".join(d["interests"])
                    for k in keys
                ])


if __name__ == "__main__":
    root = tk.Tk()
    app = VolunteerApp(root)
    root.mainloop()
