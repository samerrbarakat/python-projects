# python-projects

This repository contains a collection of Python-based utilities and mini-applications. Each project is self-contained and focuses on solving a specific problem or automating a common task. The goal is to build a portfolio of practical tools while improving development skills.

---

## Project 1: Automated File Backup

**Description:**
A desktop application that automates daily backups of a selected folder to a specified destination at a user-defined time. The tool features a clean GUI built with PyQt5 and supports running as a standalone `.exe` on Windows.

**Key Features:**

- Schedule daily backups at a specified time
- Simple and user-friendly PyQt5 interface
- Background image and custom styling
- Error handling and user notifications
- Multithreaded scheduling to avoid UI freezing
- Packaged as an executable with PyInstaller

**Usage:**

1. Enter the source and destination directory paths.
2. Enter the time of day for the backup (e.g., `17:00`). Note that you need to specify the time in 24-hour format.
3. Click **Launch Backup** to start the scheduler.

The app will copy the source folder into the destination directory with the current date as the folder name.

**Build Info:**

- Python 3.x
- Libraries used: `PyQt5`, `schedule`, `shutil`, `threading`
- Executable built using: `PyInstaller`
