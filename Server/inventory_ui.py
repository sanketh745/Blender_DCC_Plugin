import sys
import requests
import sqlite3
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QListWidget

class InventoryUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Inventory Management")
        self.setGeometry(100, 100, 400, 300)

        self.layout = QVBoxLayout()

        # Title
        self.label = QLabel("Current Inventory:")
        self.layout.addWidget(self.label)

        # List of inventory items
        self.inventory_list = QListWidget()
        self.layout.addWidget(self.inventory_list)

        # Purchase and Return buttons
        self.purchase_button = QPushButton("Purchase Item")
        self.return_button = QPushButton("Return Item")

        self.layout.addWidget(self.purchase_button)
        self.layout.addWidget(self.return_button)

        # Set layout
        self.setLayout(self.layout)

        # Load inventory on startup
        self.load_inventory()

        # Connect buttons
        self.purchase_button.clicked.connect(self.purchase_item)
        self.return_button.clicked.connect(self.return_item)

    def load_inventory(self):
        """Fetch and display inventory from the database"""
        self.inventory_list.clear()
        conn = sqlite3.connect("inventory.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name, quantity FROM inventory")
        items = cursor.fetchall()
        conn.close()

        for item in items:
            self.inventory_list.addItem(f"{item[0]} - {item[1]} left")

    def purchase_item(self):
        """Send API request to buy an item (decrease quantity)"""
        selected = self.inventory_list.currentItem()
        if selected:
            item_name = selected.text().split(" - ")[0]
            response = requests.post("http://127.0.0.1:5000/update-quantity", json={"name": item_name, "quantity": -1})
            if response.status_code == 200:
                self.load_inventory()

    def return_item(self):
        """Send API request to return an item (increase quantity)"""
        selected = self.inventory_list.currentItem()
        if selected:
            item_name = selected.text().split(" - ")[0]
            response = requests.post("http://127.0.0.1:5000/update-quantity", json={"name": item_name, "quantity": 1})
            if response.status_code == 200:
                self.load_inventory()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InventoryUI()
    window.show()
    sys.exit(app.exec())
