Organizational Hierarchy Visualizer

This Python application lets you create, manage, and visualize an organizational hierarchy through a graphical user interface built with Tkinter. You can add, update, delete, and move nodes (representing individuals), import hierarchy data from a text file, and export the hierarchy as a PDF diagram using Graphviz.
Features

    Add/Update/Delete Nodes
    Create new nodes as children of selected nodes (or under the root), update names and descriptions, or delete nodes. When a node is deleted, its children are automatically reparented to its parent.

    Import TXT Hierarchy
    Import a text file with lines in the format:
    Name, Superior: SuperiorName
    This parses the file to automatically construct the hierarchy.

    Export PDF Diagram
    Export the current hierarchy to a PDF file using Graphviz, generating a neat organizational chart.

    Move Nodes
    Move nodes by selecting a node to move (via "Set as Move Node") and then choosing a destination node (via "Move Here").

    Save/Load Hierarchy
    Save the current hierarchy as a JSON file and load it back later.

    Tooltips
    Hover over buttons to see helpful tooltips that explain their function.

Requirements

    Python 3.x
    The application is built using Python 3 and Tkinter (which is included with most Python distributions).

    Graphviz Software
    Install the Graphviz software from graphviz.org and ensure it is added to your system's PATH.

    Graphviz Python Package
    Install the Python package using:

    py -m pip install graphviz

Installation

    Install Python 3:
    Download and install Python 3 if you haven't already.

    Install Graphviz:
        Download and install Graphviz from graphviz.org.
        Ensure the Graphviz bin folder is in your system PATH.

    Install Python Dependencies:
    Open a command prompt or terminal and run:

    py -m pip install graphviz

    Download the Source Code:
    Clone or download the repository containing the program.

Usage

Manage the Hierarchy:

    Add Node:
    Enter a name (and optional description) and click Add to add a new node under the currently selected node (or the root if none is selected).
    Update Node:
    Select a node, modify its name or description, and click Update.
    Delete Node:
    Select a node (other than the root) and click Delete. Its children will be automatically moved to its parent.

Save/Load:

    Save:
    Click Save to export the hierarchy to a JSON file.
    Load:
    Click Load to import a hierarchy from a JSON file.

Import TXT Hierarchy:
Click Import TXT and choose a text file with lines formatted like:

    Alice, Superior: Bob

    This will create a node for "Bob" (if it doesn’t exist) and add "Alice" as a child.

    Export PDF Diagram:
    Click Export PDF to generate a PDF visualization of the hierarchy using Graphviz.

    Move Nodes:
        Select a node and click Set as Move Node.
        Then select the destination node and click Move Here to reparent the node.

Troubleshooting

    Graphviz Errors:
    If you see errors regarding Graphviz, make sure both the Graphviz software and the Python package are properly installed and that Graphviz is in your system PATH.

    File Permissions:
    Ensure you have permission to read/write files in the directory where you are saving or loading JSON/PDF files.

License

This project is open source. Feel free to modify and distribute it as needed.
