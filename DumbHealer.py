import sys
import json
import os

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, 
    QCheckBox, QGridLayout, QFileDialog, QMessageBox, QTabWidget, QInputDialog,
    QHBoxLayout
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon, QFont
import pyautogui
from pynput import mouse, keyboard
import qdarkstyle

# Path to save profiles
profiles_dir = "profiles"

# Character data to store pixel coordinates, keys, and enable state
character_data = {
    "Member 1": {"pixel": None, "key": None, "enabled": False},
    "Member 2": {"pixel": None, "key": None, "enabled": False},
    "Member 3": {"pixel": None, "key": None, "enabled": False},
    "Member 4": {"pixel": None, "key": None, "enabled": False},
    "Member 5": {"pixel": None, "key": None, "enabled": False},
    "Main Character": {
        "health_pixel": None, 
        "mana_pixel": None, 
        "heal_key": None, 
        "sit_key": None, 
        "stand_key": None,
        "enabled": False
    }
}

# Global list to store clicked coordinates
clicks = []

# Main application class
class DumbHealerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Dumb Healer")
        self.setGeometry(100, 100, 600, 400)
        self.setWindowIcon(QIcon("your_icon.png"))  # Set your own icon here
        
        # Main widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        self.setFont(QFont("Roboto", 10))

        # Set up tabs
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        # Group tab (Members 1-5)
        group_tab = QWidget()
        group_layout = QVBoxLayout()
        group_tab.setLayout(group_layout)
        self.tabs.addTab(group_tab, "Group")

        # Healer tab (Main Character)
        healer_tab = QWidget()
        healer_layout = QVBoxLayout()
        healer_tab.setLayout(healer_layout)
        self.tabs.addTab(healer_tab, "Healer")

        # Display mouse coordinates
        self.coord_label = QLabel("Position: X: 0, Y: 0")
        self.coord_label.setAlignment(Qt.AlignLeft)
        self.coord_label.setFont(QFont("Roboto", 8))
        layout.addWidget(self.coord_label)

        # Profile management buttons
        self.build_profile_buttons(layout)

        # Build character widgets in respective tabs
        self.build_character_widgets(group_layout, healer_layout)

        # Start updating mouse coordinates
        self.start_coordinate_update()

        # Start monitoring pixels
        self.monitor_pixels()

    def build_character_widgets(self, group_layout, healer_layout):
        # Clear previous widgets to avoid duplication
        self.clear_layout(group_layout)
        self.clear_layout(healer_layout)

        # Create widgets for group members
        group_grid = QGridLayout()
        for idx in range(1, 6):
            character = f"Member {idx}"
            self.build_character_controls(character, group_grid, idx - 1)
        group_layout.addLayout(group_grid)

        # Create widgets for main character (healer)
        healer_grid = QGridLayout()
        self.build_healer_controls("Main Character", healer_grid, 0)
        healer_layout.addLayout(healer_grid)

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
            else:
                self.clear_layout(item.layout())

    def build_character_controls(self, character, layout, row_idx):
        # Character name
        name_label = QLabel(character)
        name_label.setFont(QFont("Roboto", 10, QFont.Bold))
        layout.addWidget(name_label, row_idx, 0)

        # Pixel information
        pixel_label = QLabel("Selected Pixel: None")
        layout.addWidget(pixel_label, row_idx, 1)

        # Button to select health bar pixel
        select_btn = QPushButton("Select Health Bar")
        select_btn.setStyleSheet("padding: 5px; border-radius: 5px;")
        select_btn.clicked.connect(lambda: self.select_pixel(character, pixel_label, "pixel"))
        layout.addWidget(select_btn, row_idx, 2)

        # Assigned key information
        key_label = QLabel("Assigned Key: None")
        layout.addWidget(key_label, row_idx, 3)

        # Button to assign key
        assign_key_btn = QPushButton("Assign Key")
        assign_key_btn.setStyleSheet("padding: 5px; border-radius: 5px;")
        assign_key_btn.clicked.connect(lambda: self.assign_key(character, key_label, "key"))
        layout.addWidget(assign_key_btn, row_idx, 4)

        # Enable/Disable checkbox
        enable_checkbox = QCheckBox("Enable")
        enable_checkbox.stateChanged.connect(lambda state: self.toggle_enable(character, state))
        layout.addWidget(enable_checkbox, row_idx, 5)

        # Restore settings if loaded
        self.restore_character_data(character, pixel_label, key_label, enable_checkbox)

    def build_healer_controls(self, character, layout, row_idx):
        # Character name
        name_label = QLabel(character)
        name_label.setFont(QFont("Roboto", 10, QFont.Bold))
        layout.addWidget(name_label, row_idx, 0)

        # Health pixel information
        health_pixel_label = QLabel("Selected Health Pixel: None")
        layout.addWidget(health_pixel_label, row_idx, 1)

        # Button to select health bar pixel
        select_health_btn = QPushButton("Select Health Bar")
        select_health_btn.setStyleSheet("padding: 5px; border-radius: 5px;")
        select_health_btn.clicked.connect(lambda: self.select_pixel(character, health_pixel_label, "health_pixel"))
        layout.addWidget(select_health_btn, row_idx, 2)

        # Heal key information
        heal_key_label = QLabel("Assigned Heal Key: None")
        layout.addWidget(heal_key_label, row_idx, 3)

        # Button to assign heal key
        assign_heal_key_btn = QPushButton("Assign Heal Key")
        assign_heal_key_btn.setStyleSheet("padding: 5px; border-radius: 5px;")
        assign_heal_key_btn.clicked.connect(lambda: self.assign_key(character, heal_key_label, "heal_key"))
        layout.addWidget(assign_heal_key_btn, row_idx, 4)

        # Mana pixel information
        mana_pixel_label = QLabel("Selected Mana Pixel: None")
        layout.addWidget(mana_pixel_label, row_idx + 1, 1)

        # Button to select mana bar pixel
        select_mana_btn = QPushButton("Select Mana Bar")
        select_mana_btn.setStyleSheet("padding: 5px; border-radius: 5px;")
        select_mana_btn.clicked.connect(lambda: self.select_pixel(character, mana_pixel_label, "mana_pixel"))
        layout.addWidget(select_mana_btn, row_idx + 1, 2)

        # Sit key information
        sit_key_label = QLabel("Assigned Sit Key: None")
        layout.addWidget(sit_key_label, row_idx + 1, 3)

        # Button to assign sit key
        assign_sit_key_btn = QPushButton("Assign Sit Key")
        assign_sit_key_btn.setStyleSheet("padding: 5px; border-radius: 5px;")
        assign_sit_key_btn.clicked.connect(lambda: self.assign_key(character, sit_key_label, "sit_key"))
        layout.addWidget(assign_sit_key_btn, row_idx + 1, 4)

        # Stand key information
        stand_key_label = QLabel("Assigned Stand Key: None")
        layout.addWidget(stand_key_label, row_idx + 2, 3)

        # Button to assign stand key
        assign_stand_key_btn = QPushButton("Assign Stand Key")
        assign_stand_key_btn.setStyleSheet("padding: 5px; border-radius: 5px;")
        assign_stand_key_btn.clicked.connect(lambda: self.assign_key(character, stand_key_label, "stand_key"))
        layout.addWidget(assign_stand_key_btn, row_idx + 2, 4)

        # Enable/Disable checkbox
        enable_checkbox = QCheckBox("Enable")
        enable_checkbox.stateChanged.connect(lambda state: self.toggle_enable(character, state))
        layout.addWidget(enable_checkbox, row_idx + 3, 5)

        # Restore settings if loaded
        self.restore_character_data(character, health_pixel_label, heal_key_label, enable_checkbox)
        self.restore_character_data(character, mana_pixel_label, sit_key_label, enable_checkbox)
        self.restore_character_data(character, mana_pixel_label, stand_key_label, enable_checkbox)

    def restore_character_data(self, character, pixel_label, key_label, checkbox):
        data = character_data[character]
        if "pixel" in pixel_label.text().lower() and data["pixel"]:
            pixel_label.setText(f"Selected Pixel: {data['pixel']}")
        if "heal" in key_label.text().lower() and data["heal_key"]:
            key_label.setText(f"Assigned Heal Key: {data['heal_key']}")
        if "sit" in key_label.text().lower() and data["sit_key"]:
            key_label.setText(f"Assigned Sit Key: {data['sit_key']}")
        if "stand" in key_label.text().lower() and data["stand_key"]:
            key_label.setText(f"Assigned Stand Key: {data['stand_key']}")
        checkbox.setChecked(data["enabled"])

    def build_profile_buttons(self, layout):
        button_layout = QHBoxLayout()

        # Save profile button
        save_btn = QPushButton("Save Profile")
        save_btn.setStyleSheet("padding: 8px; border-radius: 5px;")
        save_btn.clicked.connect(self.save_profile)
        button_layout.addWidget(save_btn)

        # Load profile button
        load_btn = QPushButton("Load Profile")
        load_btn.setStyleSheet("padding: 8px; border-radius: 5px;")
        load_btn.clicked.connect(self.load_profile)
        button_layout.addWidget(load_btn)

        # Add buttons to main layout
        layout.addLayout(button_layout)

    def start_coordinate_update(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_coordinates)
        self.timer.start(100)  # Update every 100ms

    def update_coordinates(self):
        x, y = pyautogui.position()
        self.coord_label.setText(f"Position: X: {x}, Y: {y}")

    def select_pixel(self, character, pixel_label, pixel_type):
        QMessageBox.information(self, "Capture Click", f"Click on the {pixel_type.replace('_', ' ')} to select it.")
        global clicks
        clicks = []

        def on_click(x, y, button, pressed):
            if pressed:
                clicks.append((x, y))
                listener.stop()

        listener = mouse.Listener(on_click=on_click)
        listener.start()
        listener.join()

        if clicks:
            character_data[character][pixel_type] = clicks[-1]
            pixel_label.setText(f"Selected {pixel_type.replace('_', ' ').title()}: {clicks[-1]}")

    def assign_key(self, character, key_label, key_type):
        key, ok = QInputDialog.getText(self, "Assign Key", f"Enter the key to press for {character}:")
        if ok and key:
            character_data[character][key_type] = key
            key_label.setText(f"Assigned {key_type.replace('_', ' ').title()}: {key}")
            QMessageBox.information(self, "Key Assigned", f"Assigned key: {key} for {character}")

    def toggle_enable(self, character, state):
        character_data[character]['enabled'] = bool(state)
        self.monitor_pixels()

    def monitor_pixels(self):
        for character, data in character_data.items():
            if data['enabled']:
                if data.get('health_pixel') and data.get('heal_key'):
                    x, y = data['health_pixel']
                    current_color = pyautogui.pixel(x, y)
                    current_red = current_color[0]  # Extract the red component
                    if 'last_health_red' not in data:
                        data['last_health_red'] = current_red
                    elif current_red != data['last_health_red']:
                        self.press_key(data['heal_key'])
                        data['last_health_red'] = current_red
                
                if data.get('mana_pixel') and data.get('sit_key') and data.get('stand_key'):
                    x, y = data['mana_pixel']
                    current_color = pyautogui.pixel(x, y)
                    current_blue = current_color[2]  # Extract the blue component
                    if 'last_mana_blue' not in data:
                        data['last_mana_blue'] = current_blue
                    elif current_blue < data['last_mana_blue']:  # Mana decreasing
                        self.press_key(data['sit_key'])
                        data['last_mana_blue'] = current_blue
                    elif current_blue > data['last_mana_blue']:  # Mana increasing
                        self.press_key(data['stand_key'])
                        data['last_mana_blue'] = current_blue
        
        QTimer.singleShot(100, self.monitor_pixels)

    def press_key(self, key):
        keyboard_controller = keyboard.Controller()
        keyboard_controller.press(key)
        keyboard_controller.release(key)

    def save_profile(self):
        profile_name, _ = QFileDialog.getSaveFileName(self, "Save Profile", "", "JSON Files (*.json)")
        if profile_name:
            with open(profile_name, 'w') as f:
                json.dump(character_data, f)
            QMessageBox.information(self, "Profile Saved", f"Profile saved as '{profile_name}'.")

    def load_profile(self):
        profile_name, _ = QFileDialog.getOpenFileName(self, "Load Profile", "", "JSON Files (*.json)")
        if profile_name:
            with open(profile_name, 'r') as f:
                data = json.load(f)
                for character in character_data.keys():
                    character_data[character] = data[character]
                QMessageBox.information(self, "Profile Loaded", f"Profile '{profile_name}' loaded.")
                self.build_character_widgets(self.group_layout, self.healer_layout)  # Rebuild GUI to reflect loaded data


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Apply QDarkStyle
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    
    window = DumbHealerApp()
    window.show()
    
    sys.exit(app.exec_())
