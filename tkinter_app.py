import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from music_library.music_service import MusicService
from music_library.logging import LoggerFactory
from music_library.models import Track, Album, Single, Collection
from music_library.factories import MusicFactory

class MusicEntityDialog(simpledialog.Dialog):
    def __init__(self, parent, title, entity=None):
        self.entity = entity
        self.result_entity = None
        super().__init__(parent, title)
    
    def body(self, frame):
        self.frame = frame
        self.controls = {}
        self.current_row = 0
        
        # Entity Type
        tk.Label(frame, text="Type:").grid(row=self.current_row, column=0, sticky="w", padx=5, pady=5)
        self.entity_type = ttk.Combobox(frame, values=["Track", "Single", "Album", "Collection"], state="readonly")
        self.entity_type.grid(row=self.current_row, column=1, sticky="ew", padx=5, pady=5)
        self.entity_type.set("Track")
        self.entity_type.bind('<<ComboboxSelected>>', self.on_type_changed)
        self.current_row += 1
        
        # Common Fields
        self.create_field("Name:", "name", tk.StringVar)
        self.create_field("Artist:", "exec", tk.StringVar)
        self.create_field("Year:", "year", tk.IntVar, spinbox=True, min_val=1900, max_val=2100, default=2024)
        
        # Track/Specific Fields
        self.create_field("Duration (sec):", "duration", tk.IntVar, spinbox=True, min_val=1, max_val=3600, default=180)
        self.create_field("Track Number:", "track_num", tk.IntVar, spinbox=True, min_val=1, max_val=999, default=1)
        self.create_field("Genre:", "genre", tk.StringVar)
        
        # Single Specific Fields
        self.create_field("Version:", "version", tk.StringVar, default="Original")
        self.controls["remix"] = tk.BooleanVar()
        self.remix_checkbox = tk.Checkbutton(frame, text="Is Remix", variable=self.controls["remix"])
        self.remix_checkbox.grid(row=self.current_row, column=1, sticky="w", padx=5, pady=2)
        self.current_row += 1
        
        # Album/Collection Fields
        self.create_field("Style:", "style", tk.StringVar)
        self.create_field("Label:", "label", tk.StringVar)
        
        # Collection Specific Fields
        self.create_field("Theme:", "theme", tk.StringVar)
        self.create_field("Release Year:", "release_year", tk.IntVar, spinbox=True, min_val=1900, max_val=2100, default=2024)
        
        if self.entity:
            self.populate_form()
        
        self.on_type_changed()
        return frame
    
    def create_field(self, label, field_name, var_type, spinbox=False, min_val=0, max_val=100, default=None):
        tk.Label(self.frame, text=label).grid(row=self.current_row, column=0, sticky="w", padx=5, pady=2)
        
        var = var_type()
        if default is not None:
            if isinstance(default, str):
                var.set(default)
            else:
                var.set(default)
        
        if spinbox:
            control = tk.Spinbox(self.frame, from_=min_val, to=max_val, textvariable=var, width=20)
        else:
            control = tk.Entry(self.frame, textvariable=var, width=23)
        
        control.grid(row=self.current_row, column=1, sticky="ew", padx=5, pady=2)
        self.controls[field_name] = var
        self.current_row += 1
        return control
    
    def on_type_changed(self, event=None):
        entity_type = self.entity_type.get()
        
        # Show/hide fields based on type
        is_track_like = entity_type in ["Track", "Single"]
        is_single = entity_type == "Single"
        is_album_like = entity_type in ["Album", "Collection"]
        is_collection = entity_type == "Collection"
        
        # Track fields (rows 3-5)
        self.toggle_row(3, is_track_like)  # Duration
        self.toggle_row(4, is_track_like)  # Track Number
        self.toggle_row(5, is_track_like)  # Genre
        
        # Single fields (rows 6-7)
        self.toggle_row(6, is_single)  # Version
        self.toggle_row(7, is_single)  # Remix checkbox
        
        # Album fields (rows 8-9)
        self.toggle_row(8, is_album_like)  # Style
        self.toggle_row(9, is_album_like)  # Label
        
        # Collection fields (rows 10-11)
        self.toggle_row(10, is_collection)  # Theme
        self.toggle_row(11, is_collection)  # Release Year
    
    def toggle_row(self, row, visible):
        # Find all widgets in the specified row and show/hide them
        for widget in self.frame.grid_slaves(row=row):
            if visible:
                widget.grid()
            else:
                widget.grid_remove()
    
    def populate_form(self):
        if not self.entity:
            return
        
        # Set common fields
        self.controls["name"].set(self.entity.name)
        self.controls["exec"].set(self.entity.exec)
        self.controls["year"].set(self.entity.year)
        
        # Set type-specific fields
        if isinstance(self.entity, Track):
            self.entity_type.set("Track")
            self.controls["duration"].set(self.entity.duration)
            self.controls["track_num"].set(self.entity.track_num)
            self.controls["genre"].set(self.entity.genre)
            
            if isinstance(self.entity, Single):
                self.entity_type.set("Single")
                self.controls["version"].set(self.entity.version)
                self.controls["remix"].set(self.entity.remix)
        
        elif isinstance(self.entity, Album):
            self.entity_type.set("Album")
            self.controls["style"].set(self.entity.style)
            self.controls["label"].set(self.entity.label)
            
            if isinstance(self.entity, Collection):
                self.entity_type.set("Collection")
                self.controls["theme"].set(self.entity.theme)
                self.controls["release_year"].set(self.entity.release_year)
        
        self.on_type_changed()
    
    def validate(self):
        if not self.controls["name"].get().strip():
            messagebox.showerror("Error", "Name is required")
            return False
        if not self.controls["exec"].get().strip():
            messagebox.showerror("Error", "Artist is required")
            return False
        
        # Validate numeric fields
        try:
            year = int(self.controls["year"].get())
            if year < 1900 or year > 2100:
                messagebox.showerror("Error", "Year must be between 1900 and 2100")
                return False
        except (ValueError, tk.TclError):
            messagebox.showerror("Error", "Year must be a valid number")
            return False
            
        return True
    
    def dapply(self):
        entity_type = self.entity_type.get()
        name = self.controls["name"].get().strip()
        exec_artist = self.controls["exec"].get().strip()
        year = int(self.controls["year"].get())
        
        factory = MusicFactory()
        
        try:
            if entity_type == "Track":
                self.result_entity = factory.create_track(
                    name=name,
                    exec=exec_artist,
                    year=year,
                    duration=int(self.controls["duration"].get()),
                    track_num=int(self.controls["track_num"].get()),
                    genre=self.controls["genre"].get().strip()
                )
            elif entity_type == "Single":
                self.result_entity = factory.create_single(
                    name=name,
                    exec=exec_artist,
                    year=year,
                    duration=int(self.controls["duration"].get()),
                    track_num=int(self.controls["track_num"].get()),
                    genre=self.controls["genre"].get().strip(),
                    remix=bool(self.controls["remix"].get()),
                    version=self.controls["version"].get().strip()
                )
            elif entity_type == "Album":
                self.result_entity = factory.create_album(
                    name=name,
                    exec=exec_artist,
                    year=year,
                    style=self.controls["style"].get().strip(),
                    label=self.controls["label"].get().strip()
                )
            elif entity_type == "Collection":
                self.result_entity = factory.create_collection(
                    name=name,
                    exec=exec_artist,
                    year=year,
                    style=self.controls["style"].get().strip(),
                    label=self.controls["label"].get().strip(),
                    theme=self.controls["theme"].get().strip(),
                    release_year=int(self.controls["release_year"].get())
                )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create entity: {str(e)}")
            self.result_entity = None

class MusicLibraryApp:
    def __init__(self, root):
        self.root = root
        self.music_service = MusicService(LoggerFactory.create_console_logger())
        self.setup_ui()
        self.load_initial_data()
    
    def setup_ui(self):
        self.root.title("Music Library")
        self.root.geometry("800x600")
        
        # Title
        title_label = tk.Label(self.root, text="Music Library", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Listbox with scrollbar
        list_frame = ttk.Frame(main_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(list_frame, text="Music Entities:", font=("Arial", 10, "bold")).pack(anchor="w")
        
        listbox_frame = ttk.Frame(list_frame)
        listbox_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.listbox = tk.Listbox(listbox_frame, font=("Courier New", 9))
        scrollbar = ttk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=self.listbox.yview)
        self.listbox.configure(yscrollcommand=scrollbar.set)
        
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="Add", command=self.add_entity).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Edit", command=self.edit_entity).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete", command=self.delete_entity).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Refresh", command=self.refresh_list).pack(side=tk.LEFT, padx=5)
        
        # Total duration
        self.duration_label = tk.Label(main_frame, text="Total Duration: 0h 0m 0s", 
                                      font=("Arial", 10, "bold"), fg="blue")
        self.duration_label.pack(anchor="w", pady=5)
        
        # Bind double-click to edit
        self.listbox.bind('<Double-Button-1>', lambda e: self.edit_entity())
    
    def load_initial_data(self):
        # Create some initial data using the factory
        factory = MusicFactory()
        
        # Add some sample tracks
        track1 = factory.create_track("Song One", "Artist A", 2020, 180, 1, "Pop")
        track2 = factory.create_track("Song Two", "Artist B", 2021, 210, 2, "Rock")
        single1 = factory.create_single("Hit Single", "Artist C", 2022, 195, 1, "Pop", True, "Remix")
        
        # Create album
        album = factory.create_album("Great Album", "Artist A", 2020, "Pop Rock", "Music Label")
        
        # Create collection
        collection = factory.create_collection("Best Hits", "Various", 2023, "Various", "Collection Label", "Hits", 2023)
        
        # Add to service
        self.music_service.music_library.extend([track1, track2, single1, album, collection])
        
        self.refresh_list()
    
    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        for entity in self.music_service.get_all_music():
            self.listbox.insert(tk.END, str(entity))
        self.update_total_duration()
    
    def update_total_duration(self):
        total = self.music_service.get_total_duration()
        hours = total // 3600
        minutes = (total % 3600) // 60
        seconds = total % 60
        self.duration_label.config(text=f"Total Duration: {hours}h {minutes}m {seconds}s")
    
    def add_entity(self):
        dialog = MusicEntityDialog(self.root, "Add Music Entity")
        if dialog.result_entity:
            self.music_service.music_library.append(dialog.result_entity)
            self.refresh_list()
            messagebox.showinfo("Success", "Item added successfully!")
    
    def edit_entity(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an item to edit")
            return
        
        index = selection[0]
        entity = self.music_service.music_library[index]
        
        dialog = MusicEntityDialog(self.root, "Edit Music Entity", entity)
        if dialog.result_entity:
            self.music_service.music_library[index] = dialog.result_entity
            self.refresh_list()
            messagebox.showinfo("Success", "Item updated successfully!")
    
    def delete_entity(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an item to delete")
            return
        
        index = selection[0]
        entity_name = self.music_service.music_library[index].name
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{entity_name}'?"):
            del self.music_service.music_library[index]
            self.refresh_list()
            messagebox.showinfo("Success", "Item deleted successfully!")

def main():
    root = tk.Tk()
    app = MusicLibraryApp(root)
    root.mainloop()

if __name__ == "__main__":

    main()
