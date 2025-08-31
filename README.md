# 🎬 MultiPass for Maya

MultiPass is a Maya Python tool for automated Arnold multi-pass rendering.
With a simple Qt UI, you can quickly configure cameras, resolution, Arnold samples, and decide which passes to render.
It also exports camera metadata (CSV + JSON) for pipelines like COLMAP.

## ✨ Features

✅ Add selected cameras directly from your scene
<br>
✅ Choose custom resolution (Width × Height)
<br>
✅ Configure Arnold sampling (AA, Diffuse, Specular, Transmission, SSS)
<br>
✅ Select which passes to render:
<br>
   🎨 Color Image (PNG)
<br>
   🟦 Normals (EXR)
<br>
   ⚫ Depth (EXR)
<br>
   📐 Camera Parameters (CSV + JSON)
<br>
✅ Choose your output path — clean folder structure
<br>
✅ Modern Qt UI (PySide6 / PySide2) integrated in Maya

## 📦 Installation

- Clone or download this repository.

- Copy the folder MultiPass into your Maya scripts directory:

- Documents/maya/2025/scripts/

- (Optional) Run the included installer.bat for automatic setup.

## 🚀 Usage

In Maya, open the Script Editor (Python tab).

### Run:

```python
import MultiPass
MultiPass.launch()
```

### Workflow:

- 📷 Select your cameras → click Add Selected Cameras

- 📏 Set resolution and Arnold sampling

- ✅ Tick which passes you want

- 📂 Choose an output path

- ▶️ Click Render Images

- 📂 Output Structure

    ```bash
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
    ```

### ⚙️ Requirements

- Autodesk Maya 2025 (tested)

- Arnold for Maya (mtoa) plugin

- Python 3 (bundled with Maya)

- PySide6 or PySide2 (bundled with Maya)

## 📝 Notes

- Make sure Arnold (mtoa) is loaded in Maya.
- If the UI doesn’t update after edits, reload the module:

    ```python
    import importlib, MultiPass
    importlib.reload(MultiPass)
    MultiPass.launch()
    ```

## 📜 License

MIT License — free to use and adapt.