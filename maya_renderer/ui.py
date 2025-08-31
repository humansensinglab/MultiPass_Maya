import importlib
import maya.cmds as cmds
import maya.OpenMayaUI as omui

try:
    from PySide6 import QtWidgets, QtCore, QtGui
    from shiboken6 import wrapInstance
except ImportError:
    from PySide2 import QtWidgets, QtCore
    from shiboken2 import wrapInstance

from . import multiPass as MP  
_ui_instance = None


class CameraUI:
    
    def __init__(self):
        
        self.window_object_name = "MultiPass_UI_v1"
        self._qt_window = None

    def is_alive(self):
        
        return self._qt_window is not None and self._qt_window.isVisible()

    def raise_window(self):
        
        if self._qt_window:
            self._qt_window.raise_()
            self._qt_window.activateWindow()

    def create_ui(self):
        
        if cmds.window(self.window_object_name, exists=True):
            cmds.deleteUI(self.window_object_name)

        ptr = omui.MQtUtil.mainWindow()
        parent = wrapInstance(int(ptr), QtWidgets.QWidget)

        win = QtWidgets.QMainWindow(parent)
        win.setObjectName(self.window_object_name)
        win.setWindowTitle("MultiPass V1.0")

        flags = win.windowFlags()
        flags |= QtCore.Qt.Window | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowSystemMenuHint
        flags |= QtCore.Qt.WindowMinMaxButtonsHint | QtCore.Qt.WindowCloseButtonHint
        win.setWindowFlags(flags)
        win.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)

        # Central widget
        
        central = QtWidgets.QWidget(win)
        main_layout = QtWidgets.QVBoxLayout(central)
        win.setCentralWidget(central)

        # Camera save button
        
        self.add_cams_btn = QtWidgets.QPushButton("Save selected cameras")
        self.add_cams_btn.setFixedHeight(28)
        main_layout.addWidget(self.add_cams_btn)
        self.add_cams_btn.clicked.connect(self.add_selected_cameras)    
       
        # Image resolution
        
        res_txt = QtWidgets.QHBoxLayout()
        label_res = QtWidgets.QLabel("Choose an image resolution:")
        res_txt.addWidget(label_res)
        main_layout.addLayout(res_txt)

        heigh_sz = QtWidgets.QHBoxLayout()
        heigh_sz.addWidget(QtWidgets.QLabel("Height: "))
        self.height_input = QtWidgets.QLineEdit()
        self.height_input.setPlaceholderText("Enter image height here...")
        heigh_sz.addWidget(self.height_input)

        width_sz = QtWidgets.QHBoxLayout()
        width_sz.addWidget(QtWidgets.QLabel("Width: "))
        self.width_input = QtWidgets.QLineEdit()
        self.width_input.setPlaceholderText("Enter image width here...")
        width_sz.addWidget(self.width_input)

        main_layout.addLayout(heigh_sz)
        main_layout.addLayout(width_sz)
        
        self.width_input.editingFinished.connect(self.image_size)
        self.height_input.editingFinished.connect(self.image_size)
        self.image_size()

        # Arnold Setup
        
        title_arnold = QtWidgets.QLabel("Select Arnold Setup")
        main_layout.addWidget(title_arnold)

        AA = QtWidgets.QHBoxLayout()
        AA.addWidget(QtWidgets.QLabel("AA:"))
        self.num_AA = QtWidgets.QSpinBox()
        self.num_AA.setRange(1, 10)
        self.num_AA.setValue(1)
        AA.addWidget(self.num_AA)
        main_layout.addLayout(AA) 
        self.num_AA.valueChanged.connect(self.arnold_setup)

        diffuse = QtWidgets.QHBoxLayout()
        diffuse.addWidget(QtWidgets.QLabel("Diffuse:"))
        self.num_dif = QtWidgets.QSpinBox()
        self.num_dif.setRange(1, 10)
        self.num_dif.setValue(1)
        diffuse.addWidget(self.num_dif)
        main_layout.addLayout(diffuse)
        self.num_dif.valueChanged.connect(self.arnold_setup)

        spec = QtWidgets.QHBoxLayout()
        spec.addWidget(QtWidgets.QLabel("Specular:"))
        self.num_spec = QtWidgets.QSpinBox()
        self.num_spec.setRange(1, 10)
        self.num_spec.setValue(1)
        spec.addWidget(self.num_spec)
        main_layout.addLayout(spec)
        self.num_spec.valueChanged.connect(self.arnold_setup)

        trans = QtWidgets.QHBoxLayout()
        trans.addWidget(QtWidgets.QLabel("Transmission:"))
        self.num_trans = QtWidgets.QSpinBox()
        self.num_trans.setRange(1, 10)
        self.num_trans.setValue(1)
        trans.addWidget(self.num_trans)
        main_layout.addLayout(trans)
        self.num_trans.valueChanged.connect(self.arnold_setup)

        sss = QtWidgets.QHBoxLayout()
        sss.addWidget(QtWidgets.QLabel("SSS:"))
        self.num_sss = QtWidgets.QSpinBox()
        self.num_sss.setRange(1, 10)
        self.num_sss.setValue(1)
        sss.addWidget(self.num_sss)
        main_layout.addLayout(sss)
        self.num_sss.valueChanged.connect(self.arnold_setup)

        #Image type to render
        
        img_type = QtWidgets.QLabel("Select Images to render")
        main_layout.addWidget(img_type)

        img_txt = QtWidgets.QHBoxLayout()
        img_chr = QtWidgets.QLabel("Color Image: ")
        img_txt.addWidget(img_chr)
        self.chk_color = QtWidgets.QCheckBox()
        self.chk_color.setChecked(False)
        img_txt.addWidget(self.chk_color)
        main_layout.addLayout(img_txt)

        dp_txt = QtWidgets.QHBoxLayout()
        dp_chr = QtWidgets.QLabel("Depth: ")
        dp_txt.addWidget(dp_chr)
        self.chk_depth = QtWidgets.QCheckBox()
        self.chk_depth.setChecked(False)
        dp_txt.addWidget(self.chk_depth)
        main_layout.addLayout(dp_txt)

        nrm_txt = QtWidgets.QHBoxLayout()
        nrm_chr = QtWidgets.QLabel("Normals: ")
        nrm_txt.addWidget(nrm_chr)
        self.chk_normals = QtWidgets.QCheckBox()
        self.chk_normals.setChecked(False)
        nrm_txt.addWidget(self.chk_normals)
        main_layout.addLayout(nrm_txt)

        # Camera poses checker
        
        chr_txt = QtWidgets.QHBoxLayout()
        label_chr = QtWidgets.QLabel("Camera parameters")
        chr_txt.addWidget(label_chr)
        self.chk_params = QtWidgets.QCheckBox()
        self.chk_params.setChecked(False)
        chr_txt.addWidget(self.chk_params)
        main_layout.addLayout(chr_txt)

        # Image path saving
        
        path_images_save = QtWidgets.QHBoxLayout()
        path_images_save.addWidget(QtWidgets.QLabel("Select a path to store data"))

        self.data_saver_path = QtWidgets.QLineEdit()
        self.data_saver_path.setPlaceholderText("Choose a path…")
        self.data_saver_path.setMinimumWidth(260)
        path_images_save.addWidget(self.data_saver_path)

        btn_browse = QtWidgets.QPushButton("Browse...")
        btn_browse.clicked.connect(self.data_generation_path)
        path_images_save.addWidget(btn_browse)
        main_layout.addLayout(path_images_save)

        # Render image button
        
        render_btn = QtWidgets.QPushButton("Render Images")
        render_btn.setFixedHeight(28)
        main_layout.addWidget(render_btn)
        render_btn.clicked.connect(self.files_to_render)

        win.setMinimumWidth(200)
        win.adjustSize()
        win.show()
        self._qt_window = win
        return win
   
    def add_selected_cameras(self):
        from . import multiPass as MP
        MP.camera_list[:] = []        
        MP.camera_saver()            
        print("Cameras saved:", MP.camera_list)
    
    def image_size(self):
                    
        from . import multiPass
        try:
            multiPass.width = int(self.width_input.text())
            multiPass.height = int(self.height_input.text())
            
        except ValueError:
            multiPass.width = 1920
            multiPass.height = 1080
            
    def arnold_setup(self):
                    
        from . import multiPass
        
        multiPass.AA = self.num_AA.value()
        multiPass.diffuse = self.num_dif.value()
        multiPass.specular = self.num_spec.value()
        multiPass.transmission = self.num_trans.value()
        multiPass.subsurface = self.num_sss.value()
        
    def files_to_render(self):
        
        from . import multiPass
        MP.render_all(
        do_color=self.chk_color.isChecked(),
        do_normals=self.chk_normals.isChecked(),
        do_depth=self.chk_depth.isChecked(),
        do_params=self.chk_params.isChecked(),
        )
                
    def data_generation_path(self):

        start_pat = MP.path
        
        folder = QtWidgets.QFileDialog.getExistingDirectory(
            self._qt_window,
            "select screenshot saving path",
            start_pat
        )
        
        if folder:
            folder = folder.replace("\\", "/")
            self.data_saver_path.setText(folder)
            MP.path = folder

    def render(self):
        from . import multiPass as MP
        
        if not MP.camera_list:
            QtWidgets.QMessageBox.warning(self._qt_window, "No cameras", "Please add cameras before rendering.")
            return
        MP.render_all()

def main():
    
    global _ui_instance
    try:
        if _ui_instance and _ui_instance._qt_window:
            _ui_instance._qt_window.close()
    except Exception:
        pass
    _ui_instance = CameraUI()
    _ui_instance.create_ui()


if __name__ == "__main__":
    main()
