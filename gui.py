# Graphical interface for the Physics Analyzer application
# Author: Jacob Fisher
# Date: 2025-11-04

import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt


class PhysicsAnalyzerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Physics Analyzer")
        self.root.geometry("700x500")

        # --- Header Label ---
        title_label = tk.Label(root, text="Physics Analyzer", font=("Helvetica", 20, "bold"))
        title_label.pack(pady=10)

        # --- Buttons ---
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        import_btn = tk.Button(button_frame, text="Import Data", width=15, command=self.import_data)
        import_btn.grid(row=0, column=0, padx=10)

        analyze_btn = tk.Button(button_frame, text="Analyze Data", width=15, command=self.analyze_data)
        analyze_btn.grid(row=0, column=1, padx=10)

        visualize_btn = tk.Button(button_frame, text="Visualize", width=15, command=self.visualize_data)
        visualize_btn.grid(row=0, column=2, padx=10)

        # --- Text Output Area ---
        self.output_text = tk.Text(root, height=15, width=80)
        self.output_text.pack(pady=15)

        # --- Data Storage ---
        self.data = None

    # --- Function: Import CSV ---
    def import_data(self):
        file_path = filedialog.askopenfilename(
            title="Select a CSV file",
            filetypes=(("CSV files", "*.csv"), ("All files", "*.*"))
        )
        if file_path:
            try:
                self.data = pd.read_csv(file_path)
                self.output_text.insert(tk.END, f"✅ Loaded data from {file_path}\n")
                self.output_text.insert(tk.END, f"Columns: {list(self.data.columns)}\n\n")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file:\n{e}")

    # --- Function: Analyze Data ---
    def analyze_data(self):
        if self.data is None:
            messagebox.showwarning("No Data", "Please import a CSV file first.")
            return

        try:
            summary = self.data.describe()
            self.output_text.insert(tk.END, "📊 Data Summary:\n")
            self.output_text.insert(tk.END, f"{summary}\n\n")
        except Exception as e:
            messagebox.showerror("Error", f"Analysis failed:\n{e}")

    # --- Function: Visualize Data ---
    def visualize_data(self):
        if self.data is None:
            messagebox.showwarning("No Data", "Please import a CSV file first.")
            return

        try:
            numeric_cols = self.data.select_dtypes(include='number').columns
            if len(numeric_cols) >= 2:
                x, y = numeric_cols[0], numeric_cols[1]
                plt.figure(figsize=(6, 4))
                plt.scatter(self.data[x], self.data[y])
                plt.xlabel(x)
                plt.ylabel(y)
                plt.title(f"{x} vs {y}")
                plt.tight_layout()
                plt.show()
            else:
                messagebox.showinfo("Info", "Not enough numeric data to plot.")
        except Exception as e:
            messagebox.showerror("Error", f"Visualization failed:\n{e}")


# --- Run GUI Standalone ---
if __name__ == "__main__":
    root = tk.Tk()
    app = PhysicsAnalyzerGUI(root)
    root.mainloop()