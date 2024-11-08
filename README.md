# GemCraft Frostborn Wrath Save Editor

This script allows you to modify save files for the game **GemCraft - Frostborn Wrath** (Steam Edition).  
It extracts, alters, and recompresses save data with custom modifications.


## Features

- Extracts and decodes save files from GemCraft - Frostborn Wrath
- Alters save data such as:
  - Experience gained per level
  - Shadow Core amount
  - Skill points bought
  - Skills levels
  - Talismans level
- Recompresses and restores save files with a valid checksum


## Requirements

- **Python**: This script requires Python 3.7 or later.  
  Ensure Python is installed on your system and accessible via the command line (CLI).  
  You can verify your Python installation by running:
  ```bash
  python --version
  ```

  or, depending on your system:

  ```bash
  python3 --version
  ```

- **Dependencies**: The required Python libraries are listed in the `requirements.txt` file.  
  Install them with:

  ```bash
  pip install -r requirements.txt
  ```


## Usage

1. Go to `%APPDATA%\Roaming\com.giab.games.gcfw.steam\Local Store`
2. Pick one of the save files, for example `saveslot1.dat`
3. Copy/paste the save file next to `main.py`
4. Run the script with the save file name. Example:
    ```bash
    python main.py saveslot1.dat
    ```
5. Extracted data will be saved to a JSON file, and the altered save file will be created:
    ```plaintext
    Data extracted to saveslot1.extracted.json
    Altered savefile saved to saveslot1.altered.dat
    ```
6. Go back to `%APPDATA%\Roaming\com.giab.games.gcfw.steam\Local Store`
7. Back up original savefile by renaming `saveslot1.dat` to `saveslot1.dat.bak`
8. Copy/paste the altered save file next to in `%APPDATA%\Roaming\com.giab.games.gcfw.steam\Local Store`
9. Rename it to `saveslot1.dat`
10. Launch the game, load save, enjoy


## Notes

- Ensure you have a backup of your save file before using this script
- The script works by modifying specific predefined parameters


## Disclaimer

This script is provided as-is. Use at your own risk.
