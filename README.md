🎬 MultiPass for Maya

MultiPass is a Maya Python tool for automated Arnold multi-pass rendering.
With a simple Qt UI, you can quickly configure cameras, resolution, Arnold samples, and decide which passes to render.
It also exports camera metadata (CSV + JSON) for pipelines like COLMAP.

✨ Features

✅ Add selected cameras directly from your scene
✅ Choose custom resolution (Width × Height)
✅ Configure Arnold sampling (AA, Diffuse, Specular, Transmission, SSS)
✅ Select which passes to render:
   🎨 Color Image (PNG)
   🟦 Normals (EXR)
   ⚫ Depth (EXR)
   📐 Camera Parameters (CSV + JSON)
✅ Choose your output path — clean folder structure
✅ Modern Qt UI (PySide6 / PySide2) integrated in Maya

📦 Installation

Clone or download this repository.

Copy the folder MultiPass into your Maya scripts directory:

Documents/maya/2025/scripts/


(Optional) Run the included installer.bat for automatic setup.

🚀 Usage

In Maya, open the Script Editor (Python tab).

Run:

import MultiPass
MultiPass.launch()


Workflow:

📷 Select your cameras → click Add Selected Cameras

📏 Set resolution and Arnold sampling

✅ Tick which passes you want

📂 Choose an output path

▶️ Click Render Images

📂 Output Structure
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

⚙️ Requirements

Autodesk Maya 2025 (tested)

Arnold for Maya (mtoa) plugin

Python 3 (bundled with Maya)

PySide6 or PySide2 (bundled with Maya)

📝 Notes

Make sure Arnold (mtoa) is loaded in Maya.

If the UI doesn’t update after edits, reload the module:

import importlib, MultiPass
importlib.reload(MultiPass)
MultiPass.launch()

📸 Screenshots

(Add your UI screenshots here to show the tool in action!)

📜 License

MIT License — free to use and adapt.