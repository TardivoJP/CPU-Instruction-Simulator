# CPU Instructions Simulator
## _A simple educational tool for visualizing a CPU's Instruction Cycle_

![Burning CPU](https://i.imgur.com/gljhnE7.jpg)

This desktop application takes inputs in the form of instruction codes and operand values that have different behaviors depending on the instruction ranging from assigning a value to certain memory address all the way to jumping to a different line in the instructions sequence if certain conditions are met. 

For the purpuses of the educational simulation, this fictional instruction set will be used:

![Instructions table](https://i.imgur.com/qH8rlrT.png)

The application features two possible input methods, manual and file:

![Application welcome screen](https://i.imgur.com/hFqz7Tx.png)

The manual method allows for more granular inputs, perfect for someone who's trying to play with few instructions:

![Application manual input menu screen](https://i.imgur.com/wiGIkJC.png)
![Application manual insertion screen selector](https://i.imgur.com/Eno1Jct.png)
![Application insertion screen list](https://i.imgur.com/VeMaxMW.png)

Meanwhile the file method allows more flexibility and quicker iteration when testing:

![Application file input screen text box](https://i.imgur.com/8FUYxwZ.png)
![Application file input screen menu](https://i.imgur.com/MhzND8q.png)
![Application file input screen browser](https://i.imgur.com/yRrZz1Y.png)

Ultimately the input method is up to the user, what really matters are the results!

![Application results screen](https://i.imgur.com/G1vsNKM.png)

They show a detailed log of every single instruction, how it changed the MBR or the address' value, or even if it performed a jump or not, perfect for learning how the sequence was parsed and ran!


## Usage

- Run the application and choose the desired input method in the welcome screen

**Manual**
  * Choose the "insert instructions" option to modify the sequence.
  * In the bottom part of the screen you'll find a selector for the instruction codes according to the table.
  * The other two fields will activate or deactivate depending on wether that code allows for that operand.
  * Input the desired operands, remember to only use integer values.
    * However floats are still possible for the second operand in instruction 000010
  * Click the "insert" button to add the instruction to the sequence.
  * Click the "remove" button to remove any instruction from the sequence.
  * Click the "back" button to return to the manual input sub menu.
  * CLick "run instructions" to see the result of your instruction sequence.

**File**
  * Either write, paste in or use the file browser to find a a .txt with a valid input.
  * Input formatting goes as follows:
    * "[CODE],[VAL_A],[VAL_B]"
    * One instruction per line, each value separated by a comma
    * Note that invalid codes won't be accepted and will return an error!
    * The same rules apply for integer and float values!
    * Only use the operands on instructions that actually use them!
  * Click the "confirm" button to see the result of your instruction sequence.

## Packages used

This educational application was only made possible because of these amazing packages.

| Package | Link |
| ------ | ------ |
| PyQt6 | https://pypi.org/project/PyQt6/ |
| PyInstaller | https://pypi.org/project/pyinstaller/ |

## Building the application

If you want to build the application yourself from the source code:

**Windows**
1. Download Python from https://www.python.org/downloads/ and install it
2. Open a terminal and run this command to install the dependencies:
```sh
pip install PyQt6 PyInstaller
```
3. Navigate to the source code's directory and run this command to build the application:
```sh
pyInstaller main_window.py --onefile --noconsole --icon=logo.ico --add-data "resources;resources"
```
4. Run the newly created .exe in the "dist" folder

**Linux**
1. Download and install Python using the package manager from your distro:
* Ubuntu/Debian
```sh
sudo apt install python3
```
* Fedora
```sh
sudo dnf install python3
```
* CentOS/RHEL
```sh
sudo yum install centos-release-scl
sudo yum install rh-python36
scl enable rh-python36 bash
```
* Arch
```sh
sudo pacman -S python
```
2. Download and install the Package Installer for Python (pip):
```sh
python3 get-pip.py
```
3. Download and install the dependencies:
```sh
sudo pip3 install pyinstaller pyqt6
```
4. Navigate to the source code's directory and run this command to build the application:
```sh
python3 -m PyInstaller main_window.py --onefile --noconsole --icon=logo.ico --add-data "resources:resources"
```
5. Navigate to the newly created "dist" folder
6. Run this command on the main_window binary file to grant it permission to execute
```sh
chmod +x main_window
```
7. Run the application with this command:
```sh
./main_window
```

## Compatibility

This application currently runs on Windows 10 and Linux. I am looking into the possibility of adding a macOS release but I won't make any promises.

## Future development

This application does have a few possibilities for additional features which may include:

- More instructions
- Saving manual sequences as .txt files that can later be ran
- Parsing .txt files in the manual sequence screen 
- Threaded implementation to see the instructions running in real time
- Stricter input checks to reduce possible misuse or errors