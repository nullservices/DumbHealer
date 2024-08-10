# Dumb Healer

**Dumb Healer** is a lightweight Python-based tool designed for gamers who need automated healing and mana management during gameplay. The tool allows you to monitor specific pixels on your screen, triggering key presses when health or mana levels change. It's fully customizable, with options to assign different keys for various actions and save/load profiles for different characters or situations.

## Features

- **Automated Healing**: Monitor health pixels and trigger a heal key when health drops.
- **Mana Management**: Monitor mana pixels and automate sitting/standing based on mana levels.
- **Customizable Profiles**: Save and load profiles for different characters or scenarios.
- **User-Friendly Interface**: Simple tabbed interface for managing group members and the main character.
- **Dark Mode**: Sleek, modern dark theme using QDarkStyle.

## Screenshots

### Group Tab
![Group Tab](https://github.com/nullservices/DumbHealer/blob/main/Members.png)  <!-- Replace with your group tab image -->

### Healer Tab
![Healer Tab](https://github.com/nullservices/DumbHealer/blob/main/Healer.png)  <!-- Replace with your healer tab image -->


## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/dumb-healer.git
   cd dumb-healer
Install Dependencies

bash
Copy code
pip install -r requirements.txt
Run the Application

bash
Copy code
python dumb_healer.pyw
Usage
Group Tab:

Add up to five group members. For each member, select the health bar pixel to monitor, assign a key to trigger when the pixel changes, and enable or disable the monitoring.
Healer Tab:

Select pixels for both health and mana bars for the main character. Assign keys for healing, sitting, and standing. Monitoring can be enabled or disabled as needed.
Saving and Loading Profiles:

Save your current setup using the "Save Profile" button. Load a saved profile to quickly switch between different configurations.
Customization
Profiles: Profiles are saved as JSON files, making it easy to edit or share configurations.
Dark Mode: The application uses QDarkStyle for a modern, sleek look. You can modify the theme in the source code if needed.
Requirements
Python 3.x
PyQt5
pyautogui
pynput
qdarkstyle
Contributing
Contributions are welcome! Please fork this repository and submit a pull request with your changes.

License
This project is licensed under the MIT License. See the LICENSE file for more details.

Acknowledgements
Special thanks to the open-source community for providing the tools and libraries that make this project possible.

Happy Healing! 🎮
