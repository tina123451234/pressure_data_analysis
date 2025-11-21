import tkinter as tk
from tkinter import filedialog, messagebox
import os

class PressureDataGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Pressure Data Analysis Tool")
        self.root.geometry("500x550")
        self.root.resizable(False, False)
        
        # File paths
        self.csv_path = None
        self.xsl_path = None
        
        # Create GUI elements
        self.create_widgets()
    
    def create_widgets(self):
        # Title
        title_label = tk.Label(
            self.root, 
            text="Pressure Data Analysis Tool",
            font=("Arial", 16, "bold"),
            pady=20
        )
        title_label.pack()
        
        # File selection frame
        file_frame = tk.Frame(self.root, pady=10)
        file_frame.pack(fill="x", padx=20)
        
        # CSV file selection
        csv_frame = tk.Frame(file_frame)
        csv_frame.pack(fill="x", pady=5)
        
        self.csv_button = tk.Button(
            csv_frame,
            text="Select CSV File",
            command=self.select_csv,
            width=15
        )
        self.csv_button.pack(side="left")
        
        self.csv_label = tk.Label(
            csv_frame,
            text="No file selected",
            fg="gray",
            anchor="w"
        )
        self.csv_label.pack(side="left", padx=10, fill="x", expand=True)
        
        # XSL file selection
        xsl_frame = tk.Frame(file_frame)
        xsl_frame.pack(fill="x", pady=5)
        
        self.xsl_button = tk.Button(
            xsl_frame,
            text="Select XSL File",
            command=self.select_xsl,
            width=15
        )
        self.xsl_button.pack(side="left")
        
        self.xsl_label = tk.Label(
            xsl_frame,
            text="No file selected",
            fg="gray",
            anchor="w"
        )
        self.xsl_label.pack(side="left", padx=10, fill="x", expand=True)
        
        # Separator
        separator = tk.Frame(self.root, height=2, bg="lightgray")
        separator.pack(fill="x", padx=20, pady=20)
        
        # Action buttons frame
        action_label = tk.Label(
            self.root,
            text="Actions",
            font=("Arial", 12, "bold")
        )
        action_label.pack(pady=(0, 10))
        
        action_frame = tk.Frame(self.root)
        action_frame.pack(pady=10)
        
        # Merge button
        self.merge_button = tk.Button(
            action_frame,
            text="Merge Files",
            command=self.merge_files,
            width=20,
            height=2,
        )
        self.merge_button.pack(pady=5)
        
        # Plot buttons
        self.plot1_button = tk.Button(
            action_frame,
            text="Create Plot Type 1",
            command=self.create_plot1,
            width=20,
            height=2
        )
        self.plot1_button.pack(pady=5)
        
        self.plot2_button = tk.Button(
            action_frame,
            text="Create Plot Type 2",
            command=self.create_plot2,
            width=20,
            height=2
        )
        self.plot2_button.pack(pady=5)
        
        self.plot3_button = tk.Button(
            action_frame,
            text="Create Plot Type 3",
            command=self.create_plot3,
            width=20,
            height=2
        )
        self.plot3_button.pack(pady=5)
        
        self.plot4_button = tk.Button(
            action_frame,
            text="Create Plot Type 4",
            command=self.create_plot4,
            width=20,
            height=2
        )
        self.plot4_button.pack(pady=5)
        
        # Status bar
        self.status_label = tk.Label(
            self.root,
            text="Status: Ready",
            relief="sunken",
            anchor="w",
            bg="lightgray"
        )
        self.status_label.pack(side="bottom", fill="x")
    
    def select_csv(self):
        """Open file dialog to select CSV file"""
        file_path = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if file_path:
            self.csv_path = file_path
            self.csv_label.config(
                text=os.path.basename(file_path),
                fg="black"
            )
            self.update_status("CSV file selected")
    
    def select_xsl(self):
        """Open file dialog to select XSL file"""
        file_path = filedialog.askopenfilename(
            title="Select XSL File",
            filetypes=[("XSL files", "*.xsl"), ("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        if file_path:
            self.xsl_path = file_path
            self.xsl_label.config(
                text=os.path.basename(file_path),
                fg="black"
            )
            self.update_status("XSL file selected")
    
    def check_files_selected(self):
        """Check if both files are selected"""
        if not self.csv_path or not self.xsl_path:
            messagebox.showwarning(
                "Missing Files",
                "Please select both CSV and XSL files before proceeding."
            )
            return False
        return True
    
    def update_status(self, message):
        """Update status bar message"""
        self.status_label.config(text=f"Status: {message}")
        self.root.update()
    
    def merge_files(self):
        """Call merge files method"""
        if not self.check_files_selected():
            return
        
        try:
            self.update_status("Merging files...")
            
            result = merge_files(self.csv_path, self.xsl_path)
        
            
            self.update_status("Merge complete!")
            messagebox.showinfo("Success", "Files merged successfully!")
            
        except Exception as e:
            self.update_status("Error occurred")
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
    
    def create_plot1(self):
        """Create plot type 1"""
        if not self.check_files_selected():
            return
        
        try:
            self.update_status("Creating Plot Type 1...")
            
            # TODO: Replace with your actual plot function
            # from plotting import create_plot_type1
            # create_plot_type1(self.csv_path, self.xsl_path)
            
            # Placeholder
            print(f"Creating Plot 1 with: {self.csv_path} and {self.xsl_path}")
            
            self.update_status("Plot Type 1 complete!")
            
        except Exception as e:
            self.update_status("Error occurred")
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
    
    def create_plot2(self):
        """Create plot type 2"""
        if not self.check_files_selected():
            return
        
        try:
            self.update_status("Creating Plot Type 2...")
            
            # TODO: Replace with your actual plot function
            # from plotting import create_plot_type2
            # create_plot_type2(self.csv_path, self.xsl_path)
            
            print(f"Creating Plot 2 with: {self.csv_path} and {self.xsl_path}")
            
            self.update_status("Plot Type 2 complete!")
            
        except Exception as e:
            self.update_status("Error occurred")
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
    
    def create_plot3(self):
        """Create plot type 3"""
        if not self.check_files_selected():
            return
        
        try:
            self.update_status("Creating Plot Type 3...")
            
            # TODO: Replace with your actual plot function
            # from plotting import create_plot_type3
            # create_plot_type3(self.csv_path, self.xsl_path)
            
            print(f"Creating Plot 3 with: {self.csv_path} and {self.xsl_path}")
            
            self.update_status("Plot Type 3 complete!")
            
        except Exception as e:
            self.update_status("Error occurred")
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
    
    def create_plot4(self):
        """Create plot type 4"""
        if not self.check_files_selected():
            return
        
        try:
            self.update_status("Creating Plot Type 4...")
            
            # TODO: Replace with your actual plot function
            # from plotting import create_plot_type4
            # create_plot_type4(self.csv_path, self.xsl_path)
            
            print(f"Creating Plot 4 with: {self.csv_path} and {self.xsl_path}")
            
            self.update_status("Plot Type 4 complete!")
            
        except Exception as e:
            self.update_status("Error occurred")
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")


def main():
    root = tk.Tk()
    app = PressureDataGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()