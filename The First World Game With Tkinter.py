import tkinter as tk
from tkinter import ttk

# --- Data Restructuring for Easier Management ---
# The original code had redefined class attributes and multiple classes with the same name.
# This structure groups similar entities together and stores their data in a clean dictionary format.

GAME_DATA = {
    "Characters": [
        {'name': 'Elevord', 'description': 'The default player', 'type': 'Character', 'traits': 'None'}
    ],
    "Territories": [
        {'name': 'Tailand', 'description': 'The territory that you live in.', 'type': 'Territory', 'population': '1'}
    ],
    "Currencies": [
        {'name': 'Emblem', 'description': 'The currency of Tailand.', 'type': 'Currency', 'traits': 'None'}
    ],
    "Resources": [
        {'name': 'Everwood', 'description': 'Wood with extra duribility.', 'type': 'Wood', 'traits': 'Duribility'},
        {'name': 'Linanium Ore', 'description': 'Raw Linanium ore. To use it you might have to do something with it first, perhaps, smelting?', 'type': 'Metal Ore', 'traits': 'Gravitational pull.'}
    ],
    "Landforms": [
        {'name': 'Cave', 'description': 'Common unpredictable cave.', 'type': 'landform', 'possible_loot': 'Emblems, weapons.'},
        {'name': 'Mountain', 'description': 'Your normal mountain.', 'type': 'Landform', 'possible_loot': '?'}
    ],
    "Stores & Hotels": [
        {'name': 'Brandon Hights', 'description': 'The main store/supermarket in the area.', 'type': 'Store/Supermarket'},
        {'name': 'Hotel Guava', 'description': 'The local hotel the player stays at.', 'type': 'Hotel'}
    ],
    "Melee Weapons": [
        {'name': 'Training Sword', 'description': 'The sword that young warriors use to train. Crafted from Everwood for duribility.', 'type': 'Sword', 'traits': 'Duribility'},
        {'name': 'Bane of Enemy Territory', 'description': "The sword that only a hero may hold, has extrordinary power.", 'type': "Hero's sword", 'traits': "Gravitational pull, hero's luck, hero's power, hero's gain, duribility."}
    ],
    "Teams": [
    {'name': 'The Order of Death', 'description': 'An order that follows Death. Wears plague docter masks called Masks of the Order of Death. Seems to mostly be dead.' 'type': 'order', 'traits': 'Only the best of the best make up this team.'}
    {'name': 'The Ancients', 'description': 'A team that is working against Death and return peace to the world.', 'type': 'team', 'traits': 'Only the best of the best are members in this team.'}
    ],
}

class GameMenuApp:
    def __init__(self, master):
        # 1. Setup the main window
        self.master = master
        master.title("Connect The First World Menu")
        master.geometry("800x600")

        # 2. Configure the main grid layout
        master.columnconfigure(0, weight=1)
        master.columnconfigure(1, weight=3)
        master.rowconfigure(0, weight=1)

        # 3. Create a Frame for the Menu (Left Side)
        menu_frame = ttk.Frame(master, padding="10")
        menu_frame.grid(row=0, column=0, sticky="nsew")
        menu_frame.rowconfigure(1, weight=1)
        
        ttk.Label(menu_frame, text="Game Entities", font=('Arial', 12, 'bold')).grid(row=0, column=0, pady=5)
        
        # 4. Create a Listbox to show the entity names
        self.listbox = tk.Listbox(menu_frame, height=20, width=30)
        self.listbox.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.listbox.bind('<<ListboxSelect>>', self.show_details) # Bind the selection event

        # 5. Populate the Listbox
        self.all_entities = []
        for category, items in GAME_DATA.items():
            self.listbox.insert(tk.END, f"--- {category} ---")
            for item in items:
                display_name = f"  {item['name']}"
                self.listbox.insert(tk.END, display_name)
                # Store the actual data linked to the display name
                self.all_entities.append({'category': category, 'data': item, 'display_name': display_name})
            self.listbox.insert(tk.END, "") # Separator space

        # 6. Create a Frame for Details (Right Side)
        details_frame = ttk.Frame(master, padding="10")
        details_frame.grid(row=0, column=1, sticky="nsew")
        details_frame.columnconfigure(0, weight=1)
        details_frame.rowconfigure(1, weight=1)

        ttk.Label(details_frame, text="Entity Details", font=('Arial', 12, 'bold')).grid(row=0, column=0, pady=5, sticky='w')

        # 7. Create a Text widget to display details (Read-only)
        self.details_text = tk.Text(details_frame, wrap=tk.WORD, height=30, width=50, state=tk.DISABLED)
        self.details_text.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        # Add a scrollbar to the text widget
        scrollbar = ttk.Scrollbar(details_frame, command=self.details_text.yview)
        scrollbar.grid(row=1, column=1, sticky='ns')
        self.details_text['yscrollcommand'] = scrollbar.set

        # Initial prompt
        self.update_details("Select an entity from the list on the left to see its details.")


    def update_details(self, text):
        """Helper function to update the content of the details text box."""
        self.details_text.config(state=tk.NORMAL) # Enable writing
        self.details_text.delete(1.0, tk.END) # Clear existing content
        self.details_text.insert(tk.END, text)
        self.details_text.config(state=tk.DISABLED) # Disable writing


    def show_details(self, event):
        """Handler for when an item is selected in the Listbox."""
        selected_indices = self.listbox.curselection()
        if not selected_indices:
            return

        index = selected_indices[0]
        selected_item_name = self.listbox.get(index)

        # Check if the selected item is a category header or empty line
        if selected_item_name.startswith("---") or selected_item_name == "":
            self.update_details("This is a category header. Please select a specific entity.")
            return

        # Find the corresponding data
        selected_data = None
        for entity in self.all_entities:
            if entity['display_name'] == selected_item_name:
                selected_data = entity['data']
                break

        if selected_data:
            # Format the data for display
            display_text = ""
            for key, value in selected_data.items():
                # Capitalize keys for cleaner presentation
                display_text += f"**{key.replace('_', ' ').capitalize()}**: {value}\n"
            
            self.update_details(display_text)
        else:
            self.update_details(f"Error: Could not find data for {selected_item_name}")


if __name__ == "__main__":
    root = tk.Tk()
    app = GameMenuApp(root)
    root.mainloop()
