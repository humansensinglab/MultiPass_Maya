import maya.cmds as cmds
import math
import csv
import os
import json
import numpy as np


def quaternion_convert(cam):
    # rotations from Maya are in degrees → convert to radians
    rot_x = math.radians(cmds.getAttr(cam + ".rotateX"))
    rot_y = math.radians(cmds.getAttr(cam + ".rotateY"))
    rot_z = math.radians(cmds.getAttr(cam + ".rotateZ"))

    pos_x = cmds.getAttr(cam + ".translateX")
    pos_y = cmds.getAttr(cam + ".translateY")
    pos_z = cmds.getAttr(cam + ".translateZ")

    # half-angles
    cx = math.cos(rot_x * 0.5); sx = math.sin(rot_x * 0.5)
    cy = math.cos(rot_y * 0.5); sy = math.sin(rot_y * 0.5)
    cz = math.cos(rot_z * 0.5); sz = math.sin(rot_z * 0.5)

    # quaternion (XYZ order)
    qw = cx*cy*cz + sx*sy*sz
    qx = sx*cy*cz - cx*sy*sz
    qy = cx*sy*cz + sx*cy*sz
    qz = cx*cy*sz - sx*sy*cz

    return (qw, qx, qy, qz, pos_x, pos_y, pos_z, cam)


def csv_creator(cam):
    from . import multiPass as MP
    qw, qx, qy, qz, pos_x, pos_y, pos_z, _ = quaternion_convert(cam)

    csv_name = "camera_csv"
    csv_path = MP.path.replace("\\", "/") + "/" + cam
    if not os.path.exists(csv_path):
        os.makedirs(csv_path)

    full_path = os.path.join(csv_path, csv_name + ".csv")
    with open(full_path, mode="w", newline="") as f:
        writer = csv.writer(f, dialect="excel")
        field = ["Pos X","Pos Y","Pos Z","qx","qy","qz","qw"]
        writer.writerow(field)
        writer.writerow([pos_x, pos_y, pos_z, qx, qy, qz, qw])

    print(f"CSV created at: {full_path}")


def intrinsics_json(cam):
    from . import multiPass as MP
    width = MP.width
    height = MP.height

    focal_length  = cmds.getAttr(cam + ".focalLength")
    sensor_width  = cmds.getAttr(cam + ".horizontalFilmAperture") * 25.4
    sensor_height = cmds.getAttr(cam + ".verticalFilmAperture") * 25.4

    fx = focal_length * (width / sensor_width)
    fy = focal_length * (height / sensor_height)
    cx = width / 2
    cy = height / 2
    s  = 0.0

    intrinsics = [
        float(fx), float(s), float(cx),
        0.0,       float(fy), float(cy),
        0.0,       0.0,       1.0
    ]

    data = {
        "intrinsics": intrinsics,
        "width":  int(width),
        "height": int(height)
    }

    json_path = MP.path.replace("\\", "/") + "/" + cam
    if not os.path.exists(json_path):
        os.makedirs(json_path)

    full_path = os.path.join(json_path, "camera_json.json")
    with open(full_path, "w") as f:
        json.dump(data, f, indent=4)

    print(f"JSON created at: {full_path}")


def colmap_json(cam):
    from . import multiPass as MP
    width = MP.width
    height = MP.height

    rx = math.radians(cmds.getAttr(cam + ".rotateX"))
    ry = math.radians(cmds.getAttr(cam + ".rotateY"))
    rz = math.radians(cmds.getAttr(cam + ".rotateZ"))

    pos_x = cmds.getAttr(cam + ".translateX")
    pos_y = cmds.getAttr(cam + ".translateY")
    pos_z = cmds.getAttr(cam + ".translateZ")

    Rx = np.array([[1, 0, 0],
                   [0, math.cos(rx), -math.sin(rx)],
                   [0, math.sin(rx),  math.cos(rx)]])
    Ry = np.array([[ math.cos(ry), 0, math.sin(ry)],
                   [0,              1, 0],
                   [-math.sin(ry), 0, math.cos(ry)]])
    Rz = np.array([[math.cos(rz), -math.sin(rz), 0],
                   [math.sin(rz),  math.cos(rz), 0],
                   [0,             0,            1]])

    Rc2w = Rz @ Ry @ Rx
    Rw2c = Rc2w.T

    C = np.array([[pos_x],[pos_y],[pos_z]])
    t = -Rw2c @ C

    extrinsic = np.hstack((Rw2c, t))
    data = {"extrinsics": extrinsic.tolist()}

    json_path = MP.path.replace("\\", "/") + "/" + cam
    if not os.path.exists(json_path):
        os.makedirs(json_path)

    full_path = os.path.join(json_path, "colmap_camera_json.json")
    with open(full_path, "w") as f:
        json.dump(data, f, indent=4)

    print(f"JSON created at: {full_path}")
