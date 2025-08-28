from .csv_generator import csv_creator, intrinsics_json, colmap_json


import maya.cmds as cmds
import os
import mtoa.core as core
from mtoa.aovs import AOVInterface


import glob


camera_list = []
data_path = r"C:\Users\ruizo\OneDrive\Escritorio\Maya_Python_tools\snapshot"

# Render Settings
width  = 1920
height = 1080
path   = r"C:\Users\ruizo\OneDrive\Escritorio\Maya_Python_tools\snapshot"  

AA = 3
diffuse = 1
specular = 2
transmission = 1
subsurface = 4

def camera_saver():
    
    sel = cmds.ls(selection=True)

    for obj in sel:
        shapes = cmds.listRelatives(obj, shapes=True) or []
        for s in shapes:
            if cmds.nodeType(s) == "camera":
                camera_list.append(obj)  # store transform name
                print(obj)
    return camera_list
      
def arnold_render_beauty(cam):
    # Setting Arnold as main render
    if not cmds.pluginInfo("mtoa", q=True, loaded=True):
        cmds.loadPlugin("mtoa")
    core.createOptions()
    frame = int(cmds.getAttr("defaultRenderGlobals.startFrame"))  
    cmds.currentTime(frame, e=True)
    cmds.setAttr("defaultRenderGlobals.currentRenderer", "arnold", type="string")
    

    # Get selected cameras
    # sel = cmds.ls(sl=True, type="transform") or []
    # cam = None
    # for s in sel:
    #     for sh in (cmds.listRelatives(s, shapes=True) or []):
    #         if cmds.nodeType(sh) == "camera":
    #             cam = s
    #             break
    #     if cam:
    #         break
    # if not cam:
    #     cmds.error("Select a camera transform first."); return

    # Ensure output folder exists
    base_prefix = path.replace("\\", "/")             
    out_dir = os.path.dirname(base_prefix)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir)

    # Setting Arnold Atributes
    cmds.setAttr("defaultArnoldDriver.ai_translator", "png", type="string")
    cmds.setAttr("defaultArnoldDriver.mergeAOVs", 0)
    cmds.setAttr("defaultArnoldDriver.append", 0) 
    cmds.setAttr("defaultResolution.width",  width)
    cmds.setAttr("defaultResolution.height", height)

    # File naming

    cmds.setAttr("defaultRenderGlobals.imageFilePrefix", base_prefix + "/" + cam + 
                 "/ColorImage/<RenderPass>.<Frame>", type="string")

    # Arnold settings
    cmds.setAttr("defaultArnoldRenderOptions.AASamples", AA)
    cmds.setAttr("defaultArnoldRenderOptions.GIDiffuseSamples", diffuse)
    cmds.setAttr("defaultArnoldRenderOptions.GISpecularSamples", specular)
    cmds.setAttr("defaultArnoldRenderOptions.GITransmissionSamples", transmission)
    cmds.setAttr("defaultArnoldRenderOptions.GISssSamples", subsurface)
    
    # Render one frame and delete other images
    cmds.arnoldRender(cam=cam, w=width, h=height)
    beauty_dir = (base_prefix + "/" + cam + "/ColorImage").replace("\\", "/")
    for f in glob.glob(beauty_dir + "/N*.exr"):
        try:
            os.remove(f)
        except Exception:
            pass
    for f in glob.glob(beauty_dir + "/Z*.png"):
        try:
            os.remove(f)
        except Exception:
            pass

    print("[OK] Wrote EXRs to:", out_dir or base_prefix)
    print(" - Beauty: .../beauty.exr")


def arnold_render_normals(cam):
    # Setting Arnold as main render
    if not cmds.pluginInfo("mtoa", q=True, loaded=True):
        cmds.loadPlugin("mtoa")
    core.createOptions()
    frame = int(cmds.getAttr("defaultRenderGlobals.startFrame"))  
    cmds.currentTime(frame, e=True)
    cmds.setAttr("defaultRenderGlobals.currentRenderer", "arnold", type="string")

    # Get selected cameras
    # sel = cmds.ls(sl=True, type="transform") or []
    # cam = None
    # for s in sel:
    #     for sh in (cmds.listRelatives(s, shapes=True) or []):
    #         if cmds.nodeType(sh) == "camera":
    #             cam = s
    #             break
    #     if cam:
    #         break
    # if not cam:
    #     cmds.error("Select a camera transform first."); return

    # Ensure output folder exists
    base_prefix = path.replace("\\", "/")              
    out_dir = os.path.dirname(base_prefix)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir)

    # Setting Arnold Atributes
    cmds.setAttr("defaultArnoldDriver.ai_translator", "exr", type="string")
    cmds.setAttr("defaultArnoldDriver.mergeAOVs", 0)
    cmds.setAttr("defaultResolution.width",  width)
    cmds.setAttr("defaultResolution.height", height)

    # File naming
    cmds.setAttr("defaultRenderGlobals.imageFilePrefix", base_prefix + "/" + cam + 
                 "/Normals/<RenderPass>.<Frame>", type="string")

    # Arnold settings
    cmds.setAttr("defaultArnoldRenderOptions.AASamples", AA)
    cmds.setAttr("defaultArnoldRenderOptions.GIDiffuseSamples", diffuse)
    cmds.setAttr("defaultArnoldRenderOptions.GISpecularSamples", specular)
    cmds.setAttr("defaultArnoldRenderOptions.GITransmissionSamples", transmission)
    cmds.setAttr("defaultArnoldRenderOptions.GISssSamples", subsurface)
    
    

    # Adding N AOV
    AOVInterface().addAOV("N")
    cmds.setAttr("defaultArnoldRenderOptions.aovMode", 1)

    # Render one frame and delete other images
    cmds.arnoldRender(cam=cam, w=width, h=height)
    
    normals_dir = (base_prefix + "/" + cam + "/Normals").replace("\\", "/")
    for f in glob.glob(normals_dir + "/beauty*.exr"):
        try:
            os.remove(f)
        except Exception:
            pass
    for f in glob.glob(normals_dir + "/Z*.exr"):
        try:
            os.remove(f)
        except Exception:
            pass

    print("[OK] Wrote EXRs to:", out_dir or base_prefix)
    print(" - Normals: .../N.exr")
    
def arnold_render_depth(cam):
    # 0) Ensure Arnold is ready and current
    if not cmds.pluginInfo("mtoa", q=True, loaded=True):
        cmds.loadPlugin("mtoa")
    core.createOptions()
    frame = int(cmds.getAttr("defaultRenderGlobals.startFrame"))  
    cmds.currentTime(frame, e=True)
    cmds.setAttr("defaultRenderGlobals.currentRenderer", "arnold", type="string")
    
    # cmds.setAttr("defaultArnoldRenderOptions.outputs[0].enabled", 0)

    # 1) Resolve selected camera transform
    # sel = cmds.ls(sl=True, type="transform") or []
    # cam = None
    # for s in sel:
    #     for sh in (cmds.listRelatives(s, shapes=True) or []):
    #         if cmds.nodeType(sh) == "camera":
    #             cam = s
    #             break
    #     if cam:
    #         break
    # if not cam:
    #     cmds.error("Select a camera transform first."); return

    # 2) Normalize path + ensure output folder exists
    base_prefix = path.replace("\\", "/")              # avoid \U unicode escapes
    out_dir = os.path.dirname(base_prefix)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir)

    # 3) Driver + resolution (EXR for all, separate files per pass)
    cmds.setAttr("defaultArnoldDriver.ai_translator", "exr", type="string")
    cmds.setAttr("defaultArnoldDriver.mergeAOVs", 0)
    cmds.setAttr("defaultResolution.width",  width)
    cmds.setAttr("defaultResolution.height", height)

    # 4) File prefix with <RenderPass> so beauty/N split into separate files
    cmds.setAttr("defaultRenderGlobals.imageFilePrefix", base_prefix + "/" + cam + 
                 "/Depth/<RenderPass>.<Frame>", type="string")

    # 5) Arnold sampling
    cmds.setAttr("defaultArnoldRenderOptions.AASamples", AA)
    cmds.setAttr("defaultArnoldRenderOptions.GIDiffuseSamples", diffuse)
    cmds.setAttr("defaultArnoldRenderOptions.GISpecularSamples", specular)
    cmds.setAttr("defaultArnoldRenderOptions.GITransmissionSamples", transmission)
    cmds.setAttr("defaultArnoldRenderOptions.GISssSamples", subsurface)
    
    

    # 6) Add AOV Z
    AOVInterface().addAOV("Z")
    
    # cmds.setAttr("defaultArnoldDriver.mergeAOVs", 0)
    cmds.setAttr("defaultArnoldRenderOptions.aovMode", 1)

    # 7) Render one frame
    cmds.arnoldRender(cam=cam, w=width, h=height)
    
    depth_dir = (base_prefix + "/" + cam + "/Depth").replace("\\", "/")
    for f in glob.glob(depth_dir + "/beauty*.exr"):
        try:
            os.remove(f)
        except Exception:
            pass
    for f in glob.glob(depth_dir + "/N*.exr"):
        try:
            os.remove(f)
        except Exception:
            pass

    print("[OK] Wrote EXRs to:", out_dir or base_prefix)
    print(" - Depth: .../z.exr")
    
def render_all(do_color=True, do_normals=True, do_depth=True, do_params=True):
    for cam in camera_list:
        if do_color:
            arnold_render_beauty(cam)
        if do_normals:
            arnold_render_normals(cam)
        if do_depth:
            arnold_render_depth(cam)
        if do_params:
            csv_creator(cam)
            intrinsics_json(cam)
            colmap_json(cam)

def saver_test():
    
    file_path = os.path.join(data_path, f"camera.png").replace("\\", "/")
    



def main():
    
    camera_saver()
    render_all()
   



if __name__ == "__main__":
    main()