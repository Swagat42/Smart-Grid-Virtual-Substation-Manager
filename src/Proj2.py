import customtkinter as ctk
from tkinter import messagebox
import os

# substation class
class Substation:
    def __init__(self, name, location, capacity, current_load=0.0, status="Offline"):
        self.name = name
        self.location = location
        self.capacity = capacity
        self.current_load = current_load
        self.status = status

    def update_status(self, status):
        self.status = status

    def update_load(self, load):
        if load <= self.capacity:
            self.current_load = load
            if self.current_load > 0.8 * self.capacity:
                messagebox.showwarning("Warning", f"Load on {self.name} exceeds 80% capacity!")
        else:
            messagebox.showerror("Error", f"Load exceeds capacity for {self.name}!")

    def to_text(self):
        return f"{self.name},{self.location},{self.capacity},{self.current_load},{self.status}\n"

    @classmethod
    def from_text(cls, line):
        parts = line.strip().split(",")
        if len(parts) != 5:
            raise ValueError(f"Invalid line: {line}")
        name, location, capacity, load, status = parts
        return cls(name, location, float(capacity), float(load), status)

    def __str__(self):
        return f"{self.name} | {self.location} | {self.capacity} MW | Load: {self.current_load} MW | {self.status}"


# smart grid manager class
class SmartGridManager:
    def __init__(self, file_path="data.txt"):
        self.substations = []
        self.file_path = file_path
        self.load_data()

    def add_substation(self, sub):
        self.substations.append(sub)
        self.save_data()

    def remove_substation(self, name):
        for sub in self.substations:
            if sub.name == name:
                self.substations.remove(sub)
                self.save_data()
                return True
        return False

    def total_energy_flow(self):
        return sum(sub.current_load for sub in self.substations)

    def save_data(self):
        with open(self.file_path, "w") as f:
            for sub in self.substations:
                f.write(sub.to_text())

    def load_data(self):
        self.substations = []
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f:
                for line in f.readlines():
                    line = line.strip()
                    if not line:
                        continue  # skip empty lines
                    try:
                        sub = Substation.from_text(line)
                        self.substations.append(sub)
                    except ValueError:
                        print(f"Skipping invalid line in data file: {line}")


# GUI application 
class SmartGridApp:
    def __init__(self, root):
        self.manager = SmartGridManager()

        self.root = root
        self.root.title("Smart Grid Virtual Manager")
        self.root.geometry("400x700")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        label = ctk.CTkLabel(root, text="Enjoy managing Substations!!", font=("Times New Roman", 16, "bold"))
        label.pack(pady=15)

        # Buttons for features
        ctk.CTkButton(root, text="Add Substation", command=self.add_substation).pack(pady=10)
        ctk.CTkButton(root, text="Remove Substation", command=self.remove_substation).pack(pady=10)
        ctk.CTkButton(root, text="List Substations", command=self.list_substations).pack(pady=10)
        ctk.CTkButton(root, text="Update Status", command=self.update_status).pack(pady=10)
        ctk.CTkButton(root, text="Update Load", command=self.update_load).pack(pady=10)
        ctk.CTkButton(root, text="Total Energy Flow", command=self.show_total_energy).pack(pady=10)
        ctk.CTkButton(root, text="Report Status", command=self.report_status).pack(pady=10)
        ctk.CTkButton(root, text="Exit", command=root.quit).pack(pady=10)

        # Display area
        self.output_box = ctk.CTkTextbox(root, width=350, height=250)
        self.output_box.pack(pady=20)

    # GUI functions
    def add_substation(self):
        popup = ctk.CTkToplevel(self.root)
        popup.title("Add Substation")
        popup.geometry("300x350")

        entry_name = ctk.CTkEntry(popup, placeholder_text="Name")
        entry_name.pack(pady=10)
        entry_location = ctk.CTkEntry(popup, placeholder_text="Location")
        entry_location.pack(pady=10)
        entry_capacity = ctk.CTkEntry(popup, placeholder_text="Capacity (MW)")
        entry_capacity.pack(pady=10)

        def save():
            try:
                name = entry_name.get()
                location = entry_location.get()
                capacity = float(entry_capacity.get())
                sub = Substation(name, location, capacity)
                self.manager.add_substation(sub)
                self.output_box.insert("end", f"Added: {sub}\n")
                popup.destroy()
            except ValueError:
                messagebox.showerror("Error", "Enter valid capacity (number).")

        ctk.CTkButton(popup, text="Save", command=save).pack(pady=15)

    def remove_substation(self):
        popup = ctk.CTkToplevel(self.root)
        popup.title("Remove Substation")
        popup.geometry("300x200")

        entry_name = ctk.CTkEntry(popup, placeholder_text="Substation Name")
        entry_name.pack(pady=20)

        def remove():
            name = entry_name.get()
            if self.manager.remove_substation(name):
                self.output_box.insert("end", f"Removed Substation: {name}\n")
            else:
                messagebox.showerror("Error", f"Substation {name} not found.")
            popup.destroy()

        ctk.CTkButton(popup, text="Remove", command=remove).pack(pady=15)

    def list_substations(self):
        self.output_box.insert("end", "--- List of Substations ---\n")
        if not self.manager.substations:
            self.output_box.insert("end", "No substations available.\n")
        for sub in self.manager.substations:
            self.output_box.insert("end", str(sub) + "\n")

    def update_status(self):
        popup = ctk.CTkToplevel(self.root)
        popup.title("Update Status")
        popup.geometry("300x250")

        entry_name = ctk.CTkEntry(popup, placeholder_text="Substation Name")
        entry_name.pack(pady=10)
        entry_status = ctk.CTkEntry(popup, placeholder_text="Online/Offline")
        entry_status.pack(pady=10)

        def update():
            name = entry_name.get()
            status = entry_status.get()
            for sub in self.manager.substations:
                if sub.name == name:
                    sub.update_status(status)
                    self.manager.save_data()
                    self.output_box.insert("end", f"{name} status updated to {status}\n")
                    popup.destroy()
                    return
            messagebox.showerror("Error", "Substation not found.")
            popup.destroy()

        ctk.CTkButton(popup, text="Update", command=update).pack(pady=15)

    def update_load(self):
        popup = ctk.CTkToplevel(self.root)
        popup.title("Update Load")
        popup.geometry("300x250")

        entry_name = ctk.CTkEntry(popup, placeholder_text="Substation Name")
        entry_name.pack(pady=10)
        entry_load = ctk.CTkEntry(popup, placeholder_text="New Load (MW)")
        entry_load.pack(pady=10)

        def update():
            try:
                name = entry_name.get()
                load = float(entry_load.get())
                for sub in self.manager.substations:
                    if sub.name == name:
                        sub.update_load(load)
                        self.manager.save_data()
                        self.output_box.insert("end", f"{name} load updated to {load} MW\n")
                        popup.destroy()
                        return
                messagebox.showerror("Error", "Substation not found.")
            except ValueError:
                messagebox.showerror("Error", "Enter valid load (number).")

        ctk.CTkButton(popup, text="Update", command=update).pack(pady=15)

    def show_total_energy(self):
        total = self.manager.total_energy_flow()
        self.output_box.insert("end", f"Total Energy Flow: {total} MW\n")

    def report_status(self):
        self.output_box.insert("end", "--- Status Report ---\n")
        for sub in self.manager.substations:
            self.output_box.insert("end", f"{sub.name}: {sub.status}\n")


# run app
if __name__ == "__main__":
    app = ctk.CTk()
    gui = SmartGridApp(app)
    app.mainloop()
