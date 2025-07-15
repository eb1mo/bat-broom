#!/usr/bin/env python3
"""
Bat Broom - Windows Temporary Files Cleanup GUI
A Python tkinter application for safely cleaning Windows temporary files
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import os
import shutil
import glob
import threading
import datetime
from pathlib import Path
import ctypes
import sys

class BatBroomApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bat Broom - Windows Temporary Files Cleanup")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # Check admin privileges
        self.is_admin = self.check_admin()
        
        # Initialize variables
        self.cleanup_sections = self.initialize_cleanup_sections()
        self.section_vars = {}
        self.path_vars = {}
        self.is_cleaning = False
        
        # Create GUI
        self.create_gui()
        
        # Show admin warning if needed
        if not self.is_admin:
            self.show_admin_warning()
    
    def check_admin(self):
        """Check if running with administrator privileges"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    
    def show_admin_warning(self):
        """Show warning if not running as administrator"""
        messagebox.showwarning(
            "Administrator Privileges Required",
            "Some cleanup operations require administrator privileges.\n\n"
            "For best results, please run this application as administrator."
        )
    
    def initialize_cleanup_sections(self):
        """Initialize the cleanup sections with their paths"""
        return {
            "User Temporary Files": [
                ("%TEMP%\\*.*", "User Temp Directory"),
                ("%USERPROFILE%\\AppData\\Local\\Temp\\*.*", "User AppData Local Temp"),
                ("%USERPROFILE%\\AppData\\Local\\Microsoft\\Windows\\Temporary Internet Files\\*.*", "Internet Temporary Files"),
                ("%USERPROFILE%\\AppData\\Local\\Microsoft\\Windows\\INetCache\\*.*", "Internet Cache"),
                ("%USERPROFILE%\\AppData\\Local\\Microsoft\\Windows\\INetCookies\\*.*", "Internet Cookies"),
                ("%USERPROFILE%\\AppData\\Local\\Microsoft\\Windows\\WebCache\\*.*", "Web Cache"),
            ],
            "System Temporary Files": [
                ("%SystemRoot%\\Temp\\*.*", "System Temp Directory"),
                ("%SystemRoot%\\Prefetch\\*.*", "Prefetch Files"),
                ("%SystemRoot%\\SoftwareDistribution\\Download\\*.*", "Windows Update Downloads"),
            ],
            "Recent Files and History": [
                ("%USERPROFILE%\\AppData\\Roaming\\Microsoft\\Windows\\Recent\\*.*", "Recent Documents"),
                ("%USERPROFILE%\\Recent\\*.*", "Recent Files (Legacy)"),
            ],
            "Crash Dumps and Logs": [
                ("%USERPROFILE%\\AppData\\Local\\CrashDumps\\*.*", "User Crash Dumps"),
                ("%SystemRoot%\\Logs\\*.*", "System Logs"),
                ("%SystemRoot%\\Debug\\*.*", "Debug Files"),
            ],
            "Application Specific": [
                ("%USERPROFILE%\\AppData\\Local\\Packages\\*\\TempState\\*.*", "UWP App Temp State"),
                ("%USERPROFILE%\\AppData\\Local\\Microsoft\\Windows\\Explorer\\*.*", "Explorer Thumbnails"),
                ("%USERPROFILE%\\AppData\\Local\\IconCache.db", "Icon Cache"),
                ("%USERPROFILE%\\AppData\\Local\\Microsoft\\Windows\\Caches\\*.*", "Windows Caches"),
            ],
            "Browser Temporary Files": [
                ("%USERPROFILE%\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Cache\\*.*", "Chrome Cache"),
                ("%USERPROFILE%\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Code Cache\\*.*", "Chrome Code Cache"),
                ("%USERPROFILE%\\AppData\\Local\\Mozilla\\Firefox\\Profiles\\*\\cache2\\*.*", "Firefox Cache"),
                ("%USERPROFILE%\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Cache\\*.*", "Edge Cache"),
            ]
        }
    
    def create_gui(self):
        """Create the main GUI interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="🧹 Bat Broom", font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        # Subtitle
        subtitle_label = ttk.Label(main_frame, text="Windows Temporary Files Cleanup Tool", font=('Arial', 10))
        subtitle_label.grid(row=0, column=0, columnspan=2, pady=(25, 10))
        
        # Left panel - Cleanup sections
        left_frame = ttk.LabelFrame(main_frame, text="Cleanup Sections", padding="10")
        left_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        left_frame.columnconfigure(0, weight=1)
        left_frame.rowconfigure(0, weight=1)
        
        # Scrollable frame for sections
        canvas = tk.Canvas(left_frame, width=350)
        scrollbar = ttk.Scrollbar(left_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Create sections
        self.create_sections(scrollable_frame)
        
        # Right panel - Log and controls
        right_frame = ttk.Frame(main_frame)
        right_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(1, weight=1)
        
        # Control buttons
        button_frame = ttk.Frame(right_frame)
        button_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        button_frame.columnconfigure(1, weight=1)
        
        # Select All / Deselect All buttons
        select_all_btn = ttk.Button(button_frame, text="Select All", command=self.select_all)
        select_all_btn.grid(row=0, column=0, padx=(0, 5))
        
        deselect_all_btn = ttk.Button(button_frame, text="Deselect All", command=self.deselect_all)
        deselect_all_btn.grid(row=0, column=1, padx=(0, 5))
        
        # Clean button
        self.clean_btn = ttk.Button(button_frame, text="🧹 Start Cleanup", command=self.start_cleanup, style="Accent.TButton")
        self.clean_btn.grid(row=0, column=2, padx=(5, 0))
        
        # Progress bar
        self.progress = ttk.Progressbar(right_frame, mode='indeterminate')
        self.progress.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(35, 10))
        
        # Log area
        log_frame = ttk.LabelFrame(right_frame, text="Cleanup Log", padding="5")
        log_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=20, width=50)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Initial log message
        self.log_message("Bat Broom initialized successfully!")
        if not self.is_admin:
            self.log_message("⚠️ Warning: Not running as administrator. Some operations may fail.")
    
    def create_sections(self, parent):
        """Create collapsible sections with checkboxes"""
        row = 0
        for section_name, paths in self.cleanup_sections.items():
            # Section frame
            section_frame = ttk.LabelFrame(parent, text="", padding="5")
            section_frame.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=2)
            section_frame.columnconfigure(0, weight=1)
            
            # Section checkbox and label
            section_var = tk.BooleanVar()
            self.section_vars[section_name] = section_var
            
            section_cb = ttk.Checkbutton(
                section_frame, 
                text=section_name, 
                variable=section_var,
                command=lambda sn=section_name: self.toggle_section(sn)
            )
            section_cb.grid(row=0, column=0, sticky=tk.W, pady=2)
            
            # Paths frame (initially hidden)
            paths_frame = ttk.Frame(section_frame)
            paths_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=20)
            paths_frame.columnconfigure(0, weight=1)
            
            # Create path checkboxes
            self.path_vars[section_name] = {}
            for i, (path, description) in enumerate(paths):
                path_var = tk.BooleanVar()
                self.path_vars[section_name][path] = path_var
                
                path_cb = ttk.Checkbutton(
                    paths_frame,
                    text=description,
                    variable=path_var,
                    command=lambda sn=section_name: self.update_section_state(sn)
                )
                path_cb.grid(row=i, column=0, sticky=tk.W, pady=1)
            
            # Initially hide paths
            paths_frame.grid_remove()
            
            # Store reference to paths frame for toggling
            section_frame.paths_frame = paths_frame
            section_frame.is_expanded = False
            
            # Bind click event to expand/collapse
            section_cb.bind('<Button-1>', lambda e, sf=section_frame, sn=section_name: self.toggle_section_display(sf, sn))
            
            row += 1
    
    def toggle_section_display(self, section_frame, section_name):
        """Toggle the display of section paths"""
        # This will be called after the checkbox state changes
        self.root.after(10, lambda: self._toggle_section_display(section_frame, section_name))
    
    def _toggle_section_display(self, section_frame, section_name):
        """Internal method to toggle section display"""
        if self.section_vars[section_name].get():
            section_frame.paths_frame.grid()
            section_frame.is_expanded = True
        else:
            section_frame.paths_frame.grid_remove()
            section_frame.is_expanded = False
    
    def toggle_section(self, section_name):
        """Toggle all paths in a section"""
        section_state = self.section_vars[section_name].get()
        for path_var in self.path_vars[section_name].values():
            path_var.set(section_state)
    
    def update_section_state(self, section_name):
        """Update section checkbox based on path selections"""
        path_vars = self.path_vars[section_name]
        selected_count = sum(1 for var in path_vars.values() if var.get())
        
        if selected_count == 0:
            self.section_vars[section_name].set(False)
        elif selected_count == len(path_vars):
            self.section_vars[section_name].set(True)
    
    def select_all(self):
        """Select all sections and paths"""
        for section_name in self.section_vars:
            self.section_vars[section_name].set(True)
            for path_var in self.path_vars[section_name].values():
                path_var.set(True)
    
    def deselect_all(self):
        """Deselect all sections and paths"""
        for section_name in self.section_vars:
            self.section_vars[section_name].set(False)
            for path_var in self.path_vars[section_name].values():
                path_var.set(False)
    
    def log_message(self, message):
        """Add a message to the log"""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        self.log_text.insert(tk.END, formatted_message)
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def expand_path(self, path):
        """Expand environment variables in path"""
        expanded = os.path.expandvars(path)
        # Handle SystemRoot specifically
        if '%SystemRoot%' in path:
            expanded = path.replace('%SystemRoot%', os.environ.get('SystemRoot', 'C:\\Windows'))
        return expanded
    
    def safe_delete_files(self, path_pattern, description):
        """Safely delete files matching the pattern"""
        try:
            expanded_path = self.expand_path(path_pattern)
            
            # Check if path exists
            if not os.path.exists(os.path.dirname(expanded_path)) and '*' not in expanded_path:
                self.log_message(f"ℹ️ {description} - Path not found, skipping")
                return True
            
            deleted_count = 0
            
            # Handle wildcard patterns
            if '*' in expanded_path:
                # For directory patterns like C:\path\*.*
                if expanded_path.endswith('\\*.*'):
                    dir_path = expanded_path[:-4]  # Remove \*.*
                    if os.path.exists(dir_path):
                        for item in os.listdir(dir_path):
                            item_path = os.path.join(dir_path, item)
                            try:
                                if os.path.isfile(item_path):
                                    os.remove(item_path)
                                    deleted_count += 1
                                elif os.path.isdir(item_path):
                                    shutil.rmtree(item_path, ignore_errors=True)
                                    deleted_count += 1
                            except (OSError, PermissionError):
                                continue  # Skip files that can't be deleted
                else:
                    # Use glob for other patterns
                    for file_path in glob.glob(expanded_path, recursive=True):
                        try:
                            if os.path.isfile(file_path):
                                os.remove(file_path)
                                deleted_count += 1
                            elif os.path.isdir(file_path):
                                shutil.rmtree(file_path, ignore_errors=True)
                                deleted_count += 1
                        except (OSError, PermissionError):
                            continue
            else:
                # Single file
                if os.path.exists(expanded_path):
                    try:
                        if os.path.isfile(expanded_path):
                            os.remove(expanded_path)
                            deleted_count = 1
                        elif os.path.isdir(expanded_path):
                            shutil.rmtree(expanded_path, ignore_errors=True)
                            deleted_count = 1
                    except (OSError, PermissionError):
                        self.log_message(f"⚠️ {description} - Access denied or file in use")
                        return False
            
            if deleted_count > 0:
                self.log_message(f"✅ {description} - Cleaned successfully ({deleted_count} items)")
            else:
                self.log_message(f"ℹ️ {description} - No files to clean")
            
            return True
            
        except Exception as e:
            self.log_message(f"❌ {description} - Error: {str(e)}")
            return False
    
    def cleanup_worker(self):
        """Worker thread for cleanup operations"""
        try:
            self.log_message("🧹 Starting cleanup process...")
            
            total_operations = 0
            successful_operations = 0
            
            # Count total operations
            for section_name, paths in self.cleanup_sections.items():
                for path, description in paths:
                    if self.path_vars[section_name][path].get():
                        total_operations += 1
            
            if total_operations == 0:
                self.log_message("⚠️ No paths selected for cleanup!")
                return
            
            self.log_message(f"📊 Total operations to perform: {total_operations}")
            
            # Perform cleanup
            for section_name, paths in self.cleanup_sections.items():
                if any(self.path_vars[section_name][path].get() for path, _ in paths):
                    self.log_message(f"\n📁 Processing section: {section_name}")
                    
                    for path, description in paths:
                        if self.path_vars[section_name][path].get():
                            if self.safe_delete_files(path, description):
                                successful_operations += 1
            
            # Summary
            self.log_message(f"\n🎉 Cleanup completed!")
            self.log_message(f"📊 Successful operations: {successful_operations}/{total_operations}")
            
            if successful_operations < total_operations:
                self.log_message("ℹ️ Some files could not be deleted (normal for files in use)")
            
        except Exception as e:
            self.log_message(f"❌ Cleanup error: {str(e)}")
        finally:
            # Re-enable UI
            self.root.after(0, self.cleanup_finished)
    
    def start_cleanup(self):
        """Start the cleanup process"""
        if self.is_cleaning:
            return
        
        # Confirm cleanup
        if not messagebox.askyesno("Confirm Cleanup", 
                                  "Are you sure you want to start the cleanup process?\n\n"
                                  "This will permanently delete selected temporary files."):
            return
        
        # Disable UI and start progress
        self.is_cleaning = True
        self.clean_btn.config(state='disabled', text='Cleaning...')
        self.progress.start()
        self.status_var.set("Cleaning in progress...")
        
        # Clear log
        self.log_text.delete(1.0, tk.END)
        
        # Start cleanup in separate thread
        cleanup_thread = threading.Thread(target=self.cleanup_worker)
        cleanup_thread.daemon = True
        cleanup_thread.start()
    
    def cleanup_finished(self):
        """Called when cleanup is finished"""
        self.is_cleaning = False
        self.clean_btn.config(state='normal', text='🧹 Start Cleanup')
        self.progress.stop()
        self.status_var.set("Cleanup completed")
        
        messagebox.showinfo("Cleanup Complete", 
                          "Temporary files cleanup has been completed!\n\n"
                          "Check the log for detailed results.")

def main():
    """Main application entry point"""
    root = tk.Tk()
    
    # Set application icon (if available)
    try:
        root.iconbitmap('bat_broom.ico')
    except:
        pass  # Icon file not found, use default
    
    # Create and run application
    app = BatBroomApp(root)
    
    # Center window on screen
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f'+{x}+{y}')
    
    root.mainloop()

if __name__ == "__main__":
    main() 