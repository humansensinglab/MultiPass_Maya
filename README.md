MultiPass for Maya

A Maya Python tool that automates multi-pass rendering with Arnold and generates camera metadata for pipelines.
The UI lets you pick cameras, set resolution, adjust Arnold sampling, and choose which passes to render (Color, Normals, Depth, Camera Parameters).

Features

Camera Management: Add selected cameras from the scene.

Resolution Control: Set custom width and height for renders.

Arnold Setup: Configure AA, Diffuse, Specular, Transmission, and SSS samples.

Selectable Passes:

Color Image (PNG)

Normals (EXR)

Depth (EXR)

Camera Parameters → CSV, intrinsics JSON, COLMAP extrinsics JSON

Custom Output Path: Choose where rendered data and metadata are stored.

Qt UI: Clean and simple PySide6/PySide2 interface integrated in Maya.

Installation

Clone or download this repo.

Copy the folder MultiPass into your Maya scripts directory:

Documents/maya/2025/scripts/


(Optional) Use the provided installer.bat to automate installation.

Usage

In Maya, open the Script Editor (Python tab) and run:

import MultiPass
MultiPass.launch()


The UI will appear.

Workflow:

Select cameras → click Add Selected Cameras.

Set resolution and Arnold settings.

Tick which passes you want.

Choose an output path.

Hit Render Images.

Output Structure
<chosen path>/
   └── <camera name>/
       ├── ColorImage/
       │   └── frame.png
       ├── Normals/
       │   └── N.exr
       ├── Depth/
       │   └── Z.exr
       ├── camera_csv.csv
       ├── camera_json.json
       └── colmap_camera_json.json

Requirements

Autodesk Maya 2025 (tested)

Arnold for Maya (mtoa plugin)

Python 3 (bundled with Maya)

PySide6 or PySide2 (bundled with Maya)

Notes

Make sure Arnold (mtoa) is loaded in Maya.

If reloading the UI doesn’t show changes, run:

import importlib, MultiPass
importlib.reload(MultiPass)
MultiPass.launch()

License

MIT License — feel free to use and adapt.