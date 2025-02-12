import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import sys
import traceback
import os

class OrgHierarchyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Organizational Hierarchy")
        # Dictionary to store the description for each tree item
        self.description_data = {}
        # Variable to store the node selected for moving
        self.move_source = None

        # Create two main frames: one for the tree view and one for the details panel
        self.tree_frame = ttk.Frame(root)
        self.tree_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.details_frame = ttk.Frame(root, padding="10")
        self.details_frame.pack(side=tk.RIGHT, fill=tk.Y)

        # Create the TreeView widget
        self.tree = ttk.Treeview(self.tree_frame)
        self.tree.heading("#0", text="Organization")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Bind the selection event to update the details fields when a node is clicked
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        # Create the Name field
        ttk.Label(self.details_frame, text="Name:").grid(row=0, column=0, sticky=tk.W)
        self.name_var = tk.StringVar()
        self.name_entry = ttk.Entry(self.details_frame, textvariable=self.name_var)
        self.name_entry.grid(row=0, column=1, sticky=tk.EW)

        # Create the Description field using a Text widget
        ttk.Label(self.details_frame, text="Description:").grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        self.desc_text = tk.Text(self.details_frame, width=30, height=10)
        self.desc_text.grid(row=1, column=1, sticky=tk.EW, pady=(5, 0))

        # Create buttons to add, update, and delete nodes
        self.add_button = ttk.Button(self.details_frame, text="Add", command=self.add_node)
        self.add_button.grid(row=2, column=0, pady=5, sticky=tk.EW)

        self.update_button = ttk.Button(self.details_frame, text="Update", command=self.update_node)
        self.update_button.grid(row=2, column=1, pady=5, sticky=tk.EW)

        self.delete_button = ttk.Button(self.details_frame, text="Delete", command=self.delete_node)
        self.delete_button.grid(row=3, column=0, columnspan=2, pady=5, sticky=tk.EW)

        # Create Save, Load, and Export buttons
        self.save_button = ttk.Button(self.details_frame, text="Save", command=self.save_data)
        self.save_button.grid(row=4, column=0, pady=5, sticky=tk.EW)

        self.load_button = ttk.Button(self.details_frame, text="Load", command=self.load_data)
        self.load_button.grid(row=4, column=1, pady=5, sticky=tk.EW)

        self.export_button = ttk.Button(self.details_frame, text="Export PDF", command=self.export_pdf)
        self.export_button.grid(row=5, column=0, columnspan=2, pady=5, sticky=tk.EW)
        CreateToolTip(self.import_button, 
            text='Export text to visualization in PDF format')

        # Create Import TXT button
        self.import_button = ttk.Button(self.details_frame, text="Import TXT", command=self.import_txt)
        self.import_button.grid(row=6, column=0, columnspan=2, pady=5, sticky=tk.EW)
        CreateToolTip(self.import_button, 
            text='Import TXT hierarchy, parses lines for [Name], Superior: [Name] to construct hierarchy')

        # Create buttons for moving nodes
        self.set_move_button = ttk.Button(self.details_frame, text="Set as Move Node", command=self.set_move_node)
        self.set_move_button.grid(row=7, column=0, columnspan=2, pady=5, sticky=tk.EW)

        self.move_here_button = ttk.Button(self.details_frame, text="Move Here", command=self.move_here)
        self.move_here_button.grid(row=8, column=0, columnspan=2, pady=5, sticky=tk.EW)

        # Allow the details frame's second column to expand
        self.details_frame.columnconfigure(1, weight=1)

        # Create an initial root node for the organization
        self.root_node = self.tree.insert("", "end", text="Company", open=True)
        self.description_data[self.root_node] = "Root of the organizational hierarchy"

    def on_tree_select(self, event):
        """When a tree item is selected, display its name and description in the fields."""
        selected_items = self.tree.selection()
        if selected_items:
            item_id = selected_items[0]
            self.name_var.set(self.tree.item(item_id, "text"))
            desc = self.description_data.get(item_id, "")
            self.desc_text.delete("1.0", tk.END)
            self.desc_text.insert(tk.END, desc)

    def add_node(self):
        """Add a new node to the tree as a child of the selected node or as a child of the root if none is selected."""
        name = self.name_var.get().strip()
        description = self.desc_text.get("1.0", tk.END).strip()
        if not name:
            messagebox.showwarning("Input Error", "Please enter a name.")
            return
        selected_items = self.tree.selection()
        parent = selected_items[0] if selected_items else ""
        new_node = self.tree.insert(parent, "end", text=name, open=True)
        self.description_data[new_node] = description
        self.name_var.set("")
        self.desc_text.delete("1.0", tk.END)

    def update_node(self):
        """Update the selected node's name and description."""
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("Selection Error", "Please select a node to update.")
            return
        item_id = selected_items[0]
        new_name = self.name_var.get().strip()
        new_description = self.desc_text.get("1.0", tk.END).strip()
        if not new_name:
            messagebox.showwarning("Input Error", "Name cannot be empty.")
            return
        self.tree.item(item_id, text=new_name)
        self.description_data[item_id] = new_description

    def delete_node(self):
        """
        Delete the selected node while transferring its children up one level.
        The children of the deleted node will be moved to its parent.
        """
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("Selection Error", "Please select a node to delete.")
            return
        for item in selected_items:
            if item == self.root_node:
                messagebox.showwarning("Delete Error", "Cannot delete the root node.")
            else:
                parent = self.tree.parent(item)
                for child in self.tree.get_children(item):
                    self.tree.move(child, parent, "end")
                self.tree.delete(item)
                if item in self.description_data:
                    del self.description_data[item]

    def build_tree(self, item_id):
        """Recursively build a dictionary representing the tree structure starting from item_id."""
        return {
            "name": self.tree.item(item_id, "text"),
            "description": self.description_data.get(item_id, ""),
            "children": [self.build_tree(child) for child in self.tree.get_children(item_id)]
        }

    def insert_tree_item(self, parent, node_data):
        """Recursively insert a node (and its children) into the tree from a dictionary."""
        new_item = self.tree.insert(parent, "end", text=node_data.get("name", ""), open=True)
        self.description_data[new_item] = node_data.get("description", "")
        for child in node_data.get("children", []):
            self.insert_tree_item(new_item, child)

    def save_data(self):
        """Save the current tree structure to a JSON file."""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
        )
        if not file_path:
            return
        tree_data = [self.build_tree(item_id) for item_id in self.tree.get_children("")]
        try:
            with open(file_path, "w") as f:
                json.dump(tree_data, f, indent=4)
            messagebox.showinfo("Save Successful", f"Data saved to {file_path}")
        except Exception as e:
            messagebox.showerror("Save Error", f"Could not save data: {e}")

    def load_data(self):
        """Load the tree structure from a JSON file."""
        file_path = filedialog.askopenfilename(
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
        )
        if not file_path:
            return
        try:
            with open(file_path, "r") as f:
                tree_data = json.load(f)
            for item in self.tree.get_children():
                self.tree.delete(item)
            self.description_data.clear()
            for node_data in tree_data:
                self.insert_tree_item("", node_data)
            messagebox.showinfo("Load Successful", f"Data loaded from {file_path}")
        except Exception as e:
            messagebox.showerror("Load Error", f"Could not load data: {e}")

    def export_pdf(self):
        """Export the current hierarchy as a PDF diagram using Graphviz."""
        try:
            from graphviz import Digraph
        except ImportError:
            messagebox.showerror("Graphviz Error",
                                 "The 'graphviz' package is required for exporting diagrams.\nInstall it via pip: py -m pip install graphviz")
            return

        dot = Digraph(comment='Organizational Hierarchy', format='pdf')
        dot.attr(rankdir='TB')

        def add_nodes_edges(parent_id, parent_dot_id=None):
            for child_id in self.tree.get_children(parent_id):
                node_label = self.tree.item(child_id, 'text')
                dot.node(child_id, node_label)
                if parent_dot_id is not None:
                    dot.edge(parent_dot_id, child_id)
                add_nodes_edges(child_id, child_id)

        for root_id in self.tree.get_children(''):
            root_label = self.tree.item(root_id, 'text')
            dot.node(root_id, root_label)
            add_nodes_edges(root_id, root_id)

        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")]
        )
        if file_path:
            file_path = os.path.splitext(file_path)[0]
            output_path = dot.render(file_path, view=True, cleanup=True)
            messagebox.showinfo("Export Successful", f"Diagram exported to:\n{output_path}")

    def find_node_by_name(self, name, parent=""):
        """Recursively search for a node with the given name starting from parent."""
        for child in self.tree.get_children(parent):
            if self.tree.item(child, "text") == name:
                return child
            result = self.find_node_by_name(name, child)
            if result:
                return result
        return None

    def import_txt(self):
        """
        Import a text file. Each line should contain a subordinate's name followed by 
        ", Superior: " and then the superior's name. For example:
        
            Alice, Superior: Bob
        
        This function will find (or create) a node for Bob and then add Alice as a child.
        """
        file_path = filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if not file_path:
            return
        try:
            with open(file_path, "r") as f:
                lines = f.readlines()
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                if ", Superior: " in line:
                    parts = line.split(", Superior: ")
                    subordinate_name = parts[0].strip()
                    superior_name = parts[1].strip()
                    superior_node = self.find_node_by_name(superior_name)
                    if not superior_node:
                        superior_node = self.tree.insert(self.root_node, "end", text=superior_name, open=True)
                        self.description_data[superior_node] = ""
                    subordinate_node = self.tree.insert(superior_node, "end", text=subordinate_name, open=True)
                    self.description_data[subordinate_node] = ""
            messagebox.showinfo("Import Successful", f"Data imported from {file_path}")
        except Exception as e:
            messagebox.showerror("Import Error", f"Could not import data: {e}")

    # --- Methods for Moving Nodes via Buttons ---
    def set_move_node(self):
        """Set the currently selected node as the node to move."""
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("Move Node", "Please select a node to move.")
            return
        self.move_source = selected_items[0]
        messagebox.showinfo("Move Node", f"Selected node '{self.tree.item(self.move_source, 'text')}' for moving.")

    def move_here(self):
        """Move the previously selected node to be a child of the currently selected node."""
        if not self.move_source:
            messagebox.showwarning("Move Node", "No node selected to move. Please click 'Set as Move Node' first.")
            return
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("Move Node", "Please select a destination node.")
            return
        destination = selected_items[0]
        if destination == self.move_source:
            messagebox.showwarning("Move Node", "Destination cannot be the same as the node to move.")
            return
        if self.is_descendant(destination, self.move_source):
            messagebox.showwarning("Move Node", "Cannot move a node to one of its descendants.")
            return
        self.tree.move(self.move_source, destination, "end")
        messagebox.showinfo("Move Node", f"Moved node '{self.tree.item(self.move_source, 'text')}' under '{self.tree.item(destination, 'text')}'.")
        self.move_source = None

    def is_descendant(self, item, potential_ancestor):
        """Return True if 'item' is a descendant of 'potential_ancestor'."""
        parent = self.tree.parent(item)
        while parent:
            if parent == potential_ancestor:
                return True
            parent = self.tree.parent(parent)
        return False

def main():
    root = tk.Tk()
    app = OrgHierarchyApp(root)
    root.mainloop()

if __name__ == "__main__":
    try:
        main()
    except Exception:
        error_message = traceback.format_exc()
        with open("error_report.txt", "w") as f:
            f.write(error_message)
        try:
            temp_root = tk.Tk()
            temp_root.withdraw()
            messagebox.showerror("Unexpected Error", error_message)
            temp_root.destroy()
        except Exception:
            print("Unexpected Error:")
            print(error_message)
