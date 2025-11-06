# Physics Analyzer - Modern CustomTkinter Edition
# Author: Jacob Fisher
# Date: 2025-11-05

import customtkinter as ctk
from tkinter import filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
import os

# Set modern appearance
ctk.set_appearance_mode("System")  # Auto light/dark
ctk.set_default_color_theme("blue")


class PhysicsAnalyzerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # ===== Window setup =====
        self.title("Physics Analyzer Pro")
        self.geometry("1100x700")
        self.data = None

        # ===== Top bar =====
        topbar = ctk.CTkFrame(self, height=50)
        topbar.pack(fill="x", pady=(0, 5))

        ctk.CTkLabel(
            topbar,
            text="⚛️ Physics Analyzer Pro",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(side="left", padx=20)

        self.theme_switch = ctk.CTkSwitch(
            topbar, text="Dark Mode", command=self.toggle_theme
        )
        self.theme_switch.pack(side="right", padx=20)

        # ===== Main Tabs =====
        self.tabs = ctk.CTkTabview(self)
        self.tabs.pack(fill="both", expand=True, padx=10, pady=10)

        # Create tabs
        self.tab_home = self.tabs.add("📂 Data")
        self.tab_analyze = self.tabs.add("📊 Analyze")
        self.tab_visualize = self.tabs.add("📈 Visualize")

        self.build_home_tab()
        self.build_analyze_tab()
        self.build_visualize_tab()

    # =======================
    # Build Tabs
    # =======================

    def build_home_tab(self):
        """Home tab for importing data."""
        ctk.CTkLabel(
            self.tab_home,
            text="Welcome to Physics Analyzer",
            font=ctk.CTkFont(size=22, weight="bold")
        ).pack(pady=20)

        ctk.CTkButton(
            self.tab_home, text="📂 Import CSV File", command=self.import_data
        ).pack(pady=10)

        self.file_info = ctk.CTkTextbox(self.tab_home, wrap="word", height=400)
        self.file_info.pack(fill="both", expand=True, padx=20, pady=20)

    def build_analyze_tab(self):
        """Tab for performing data analysis."""
        frame = ctk.CTkFrame(self.tab_analyze)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Options
        self.show_mean = ctk.BooleanVar(value=True)
        self.show_median = ctk.BooleanVar(value=False)
        self.show_std = ctk.BooleanVar(value=False)
        self.show_minmax = ctk.BooleanVar(value=True)

        ctk.CTkCheckBox(frame, text="Mean", variable=self.show_mean).grid(row=0, column=0, padx=10, pady=5)
        ctk.CTkCheckBox(frame, text="Median", variable=self.show_median).grid(row=0, column=1, padx=10, pady=5)
        ctk.CTkCheckBox(frame, text="Standard Deviation", variable=self.show_std).grid(row=0, column=2, padx=10, pady=5)
        ctk.CTkCheckBox(frame, text="Min/Max", variable=self.show_minmax).grid(row=0, column=3, padx=10, pady=5)

        ctk.CTkButton(
            frame, text="Run Analysis", command=self.analyze_data
        ).grid(row=0, column=4, padx=20)

        self.results_output = ctk.CTkTextbox(self.tab_analyze, wrap="word", height=500)
        self.results_output.pack(fill="both", expand=True, padx=20, pady=(10, 20))

    def build_visualize_tab(self):
        """Tab for data visualization."""
        ctk.CTkLabel(
            self.tab_visualize,
            text="Visualize Numeric Data",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=10)

        ctk.CTkButton(
            self.tab_visualize, text="📈 Show Plot", command=self.visualize_data
        ).pack(pady=10)

        self.plot_info = ctk.CTkTextbox(self.tab_visualize, wrap="word", height=400)
        self.plot_info.pack(fill="both", expand=True, padx=20, pady=20)

    # =======================
    # Core Functions
    # =======================

    def toggle_theme(self):
        """Switch between dark/light mode."""
        current = ctk.get_appearance_mode()
        new = "Dark" if current == "Light" else "Light"
        ctk.set_appearance_mode(new)

    def import_data(self):
        """Import CSV and display columns."""
        try:
            file_path = filedialog.askopenfilename(
                title="Select CSV File",
                filetypes=(("CSV files", "*.csv"), ("All files", "*.*"))
            )
            if file_path:
                self.data = pd.read_csv(file_path)
                cols = list(self.data.columns)
                self.file_info.delete("1.0", "end")
                self.file_info.insert("end", f"✅ Loaded: {os.path.basename(file_path)}\n\n")
                self.file_info.insert("end", f"Columns Detected:\n{', '.join(cols)}\n\n")
                self.file_info.insert("end", f"Preview:\n{self.data.head()}\n")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file:\n{e}")

    def analyze_data(self):
        """Compute descriptive statistics based on user selection."""
        if self.data is None:
            messagebox.showwarning("No Data", "Please import a CSV file first.")
            return

        numeric_cols = self.data.select_dtypes(include="number")
        if numeric_cols.empty:
            messagebox.showinfo("Info", "No numeric columns found.")
            return

        results = []
        if self.show_mean.get():
            results.append("Means:\n" + str(numeric_cols.mean()))
        if self.show_median.get():
            results.append("\nMedians:\n" + str(numeric_cols.median()))
        if self.show_std.get():
            results.append("\nStandard Deviations:\n" + str(numeric_cols.std()))
        if self.show_minmax.get():
            results.append("\nMinimums:\n" + str(numeric_cols.min()))
            results.append("\nMaximums:\n" + str(numeric_cols.max()))

        display_text = "\n".join(results)
        self.results_output.delete("1.0", "end")
        self.results_output.insert("end", display_text)

    def visualize_data(self):
        """Plot first two numeric columns."""
        if self.data is None:
            messagebox.showwarning("No Data", "Please import a CSV file first.")
            return

        numeric_cols = self.data.select_dtypes(include="number").columns
        if len(numeric_cols) < 2:
            messagebox.showinfo("Info", "Not enough numeric columns to plot.")
            return

        x, y = numeric_cols[0], numeric_cols[1]
        plt.figure(figsize=(7, 5))
        plt.scatter(self.data[x], self.data[y], color="#00BFFF")
        plt.xlabel(x)
        plt.ylabel(y)
        plt.title(f"{y} vs {x}")
        plt.grid(True, linestyle="--", alpha=0.6)
        plt.tight_layout()
        plt.show()


# =======================
# Run Safely
# =======================
if __name__ == "__main__":
    app = PhysicsAnalyzerApp()
    app.mainloop()
