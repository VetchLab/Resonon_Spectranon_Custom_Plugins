SpectrononPro3 Python Plugins

This repository contains two Python plugins designed for use with the SpectrononPro3 software by Resonon. Enhance your SpectrononPro3 capabilities with these easy-to-install tools.

Prerequisites

SpectrononPro3 Software: Before you proceed, ensure that you've installed the SpectrononPro3 software. If you haven't, download it from the following link:

SpectrononPro3 Software [add hyperlink to https://downloads.resonon.com/categories/53/]

Follow the installation instructions provided by Resonon for SpectrononPro3.

Installation

1. Download the Plugins
Clone this repository or download the Python scripts directly.
2. Copy the Plugins to Respective Directories

MeanSpectraAcrossEntireImage.py

Copy this script to the directory:

C:\Users\[Your_Username]\appdata\local\SpectrononPro3\user_plugins\cube\user

Replace [Your_Username] with your Windows profile username.

RandomSelectionCubeCreate.py

Copy this script to the directory:

C:\Users\[Your_Username]\appdata\local\SpectrononPro3\user_plugins\select\user

Replace [Your_Username] with your Windows profile username.

3. Reload Plugins

Start the SpectrononPro3 program.
Once loaded, go to the "File" tab at the top of the screen and select "Reload Plugins".

Usage

1. MeanSpectraAcrossEntireImage.py

Purpose: Computes the mean spectrum of an entire datacube. This comes in handy as there isn't a direct option in SpectrononPro3 for acquiring the mean spectrum of an entire datacube without using the select tool. It also pairs well with the batch processor for analyzing multiple datacubes without having to open each one individually.
Access: Within the software, navigate to the "User" tab in the cube plugin menu.

2. RandomSelectionCubeCreate.py

Purpose: A select tool plugin. Use this after selecting a specific region in an image. Once invoked, it lets users define a pixel count. The plugin then randomly samples the defined number of pixels within the selected area.
Access:
Use the select tool within an image to define a region.
Right-click on the highlighted region to access the select plugin menu.
Navigate to the "User" tab at the bottom of the menu to find this plugin.


Credits
These plugins were developed by Wyatt Medina. Special thanks to Justin Vetch and MSU-Western Triangle Agricultural Research Center for their support and collaboration throughout the project.

For any queries or feedback related to these plugins, please contact wyatt.medina@montana.edu.
