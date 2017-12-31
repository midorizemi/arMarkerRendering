#!BPY
import bpy
from mathutils import Vector
import numpy as np
import os
import time

def delete_all():
    print("Delete_all")
    for item in bpy.context.scene.objects:
        bpy.context.scene.objects.unlink(item)

    for item in bpy.data.objects:
        bpy.data.objects.remove(item)
    
    for item in bpy.data.curves:
        bpy.data.curves.remove(item)
        
    for item in bpy.data.meshes:
        bpy.data.meshes.remove(item)

    for item in bpy.data.materials:
        item.user_clear()
        bpy.data.materials.remove(item)
    
    for item in bpy.data.textures:
        item.user_clear()
        bpy.data.textures.remove(item)
        
    for item in bpy.data.images:
        item.user_clear()
        bpy.data.images.remove(item)
    
    for item in bpy.data.cameras:
        item.user_clear()
        bpy.data.cameras.remove(item)
        
    for item in bpy.data.lamps:
        item.user_clear()
        bpy.data.lamps.remove(item)

def add_plane(_name="test_name", num_cuts=3):
    print("create primitive obj")
    bpy.ops.mesh.primitive_plane_add(
    location=(0,0,0),
    )
    item = bpy.data.objects['Plane']
    item.name = _name
    mesh = bpy.data.meshes['Plane']
    mesh.name = _name
    item.dimensions=(8,6,0)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.subdivide(number_cuts=num_cuts)
    bpy.ops.object.mode_set(mode='OBJECT')

def add_base(_name="test_name", num_cuts=3):
    print("making base")
    bpy.ops.mesh.primitive_plane_add(
    location=(0,0,0),
    )
    item = bpy.data.objects['Plane']
    item.name = _name
    mesh = bpy.data.meshes['Plane']
    mesh.name = _name
    
def add_pl(_name="pl"):
    print("making pl")
    add_plane(_name)
    all = [False] * 20
    all[3]=True
    bpy.data.objects[_name].layers=all

def add_mltfctd(_name="mltfctd"):
    print("making mltf")
    add_plane(_name)
    mesh = bpy.data.objects[_name].data
    vertices = list(mesh.vertices)
    counter=0
    side=bpy.data.objects[_name].dimensions[0] / 4
    offset_z = side*np.sin(np.radians(60))
    offset_x = side*np.cos(np.radians(60))/4
    for vertix in vertices:
        if vertix.co[0] == 0.0:
            vertix.co = vertix.co + Vector((0, 0, offset_z))
        elif vertix.co[0] == 0.5:
            vertix.co = vertix.co + Vector((-offset_x, 0, 0))
        elif vertix.co[0] == -0.5:
            vertix.co = vertix.co + Vector((offset_x, 0, 0))
        elif vertix.co[0] == 1.0:
            vertix.co = vertix.co + Vector((-offset_x, 0, 0))
        elif vertix.co[0] == -1.0:
            vertix.co = vertix.co + Vector((offset_x, 0, 0))
    all = [False] * 20
    all[1]=True
    bpy.data.objects[_name].layers=all
            
def add_dfrm(_name="dfrm"):
    print("making dfrm")
    bpy.ops.curve.primitive_nurbs_path_add(location=(0,0,0))
    name_path = "NurbsPath"
    bpy.data.objects[name_path].dimensions=(8,0,0)
    
    add_plane(_name, 7)
    plane = bpy.data.objects[_name]
    plane.select=True
    bpy.ops.object.modifier_add(type='CURVE')
    plane.modifiers["Curve"].object=bpy.data.objects[name_path]
    plane.location[0]=4
    plane.select=False
    
    path=bpy.data.curves[name_path]
    bpy.ops.object.mode_set(mode='EDIT')
    ctrlPoints=path.splines[0].points
    ctrlPoints[0].co = Vector((-1.5, 0, 0, 1))
    ctrlPoints[1].co = Vector((-0.25, 0, 0, 1))
    ctrlPoints[2].co = Vector((0, 0, 3.5, 1))
    ctrlPoints[3].co = Vector((0.25, 0, 0, 1))
    ctrlPoints[4].co = Vector((1.5, 0, 0, 1))
    bpy.ops.object.mode_set(mode='OBJECT')
    
    all = [False] * 20
    all[2]=True
    plane.layers=all
    bpy.data.objects[name_path].layers=all
    
def add_material(_name, _file_path):
    print("adding material of %s"%_name)
    obj=bpy.data.objects[_name]
    obj.select=True
    #Material setting
    bpy.ops.material.new()
    mtrl=bpy.data.materials['Material']
    mtrl.name='Mtrl_'+_name
    mtrl.user_clear()
    mtrl.diffuse_intensity=1
    mtrl.specular_intensity=0
    mtrl.specular_hardness=1
    obj.active_material=mtrl
    #Texture setting
    bpy.ops.texture.new()
    texture=bpy.data.textures['Texture']
    texture.name='Txtr_'+_name
    texture.user_clear()
    mtrl.active_texture=texture
    bpy.ops.image.open(filepath="//"+_file_path)
    #Image setting
    img=bpy.data.images[_file_path]
    img.user_clear()
    texture.image=img
    mtrl.texture_slots[0].texture_coords='ORCO'
    
def layer(num_l):
    all = [False] * 20
    all[num_l] = True
    return all

def select_layer(num_l1, num_l2):
    all=[False] * 20
    all[num_l1]=True
    all[num_l2]=True
    return all

def make_objects(_file_path):
    name_obj="mltfctd"
    add_mltfctd(name_obj)
    add_material(name_obj, _file_path)
    name_obj="dfrm"
    add_dfrm(name_obj)
    add_material(name_obj, _file_path)
    name_obj="pl"
    add_pl(name_obj)
    add_material(name_obj, _file_path)
    
def new_scene_objects(_file_path="natural-marker3.png"):
    delete_all()
    bpy.ops.object.camera_add(location=(0,0,10), rotation=(0,0,0))
    bpy.ops.object.lamp_add(type='SUN', location=(0,0,15), rotation=(0,0,0))
    bpy.data.scenes["Scene"].camera=bpy.data.objects["Camera"]
    add_base("base")
    bpy.data.objects["base"].location=(0,0,0)
    bpy.data.objects["base"].dimensions=(0.1,0.1,0)
    bpy.data.objects["Camera"].select=True
    bpy.data.objects["base"].select=True
    bpy.ops.object.track_set(type='TRACKTO')
    ttc=bpy.data.objects["Camera"].constraints.new(type='TRACK_TO')
    ttc.target = bpy.data.objects["base"]
    ttc.track_axis='TRACK_Z'
    bpy.ops.object.select_all(action='DESELECT')
    make_objects(_file_path)

def compute_tilt_phi(params, dir_path, layer=1):
    bpy.data.scenes["Scene"].render.filepath = dir_path
    camera=bpy.data.objects["Camera"]
    all=[False] * 20
    all[0]=True
    all[layer]=True
    #return all
    bpy.data.scenes["Scene"].layers=all
    for i, param in enumerate(params):
        _location, deg_param = calculate_cam_location(param)
        camera.location = _location
        bpy.ops.render.render()
        filepath = os.path.join(dir_path,"{0:03d}_{1:03.0f}-{2:03.0f}.png".format(i, 90-deg_param[0], deg_param[1]))
        print(filepath)
        bpy.data.images['Render Result'].save_render(filepath=filepath)
        time.sleep(1)

def calculate_cam_location(param):
    theta=np.arccos(1 / param[0])
    point=(0, 0, param[2])
    Ry=np.matrix(((np.cos(theta), 0, -np.sin(theta)), (0, 1, 0),
    (np.sin(theta), 0, np.cos(theta))))
    Rz = np.matrix(((np.cos(param[1]), np.sin(param[1]), 0),
    (-np.sin(param[1]), np.cos(param[1]), 0),
    (0, 0, 1)))
    tmpY=np.dot(Ry,point)
    point=(tmpY[0,0], tmpY[0,1], tmpY[0,2])
    hoge=np.dot(Rz, point)
    _location=(hoge[0,0], hoge[0, 1], hoge[0, 2])
    return _location, np.rad2deg([theta, param[1]])

def calc_affine_params(simu: str ='default', radius=15) -> list:
    params = [(1.0, 0.0, radius)]
    if simu == 'default' or simu == 'asift' or simu is None:
        simu = 'default'
        for t in 2**(0.5*np.arange(1, 6)):
            for phi in np.arange(0, 180, 72.0 / t):
                params.append((t, phi, radius))
    if simu == 'degrees':
        for t in np.reciprocal(np.cos(np.radians(np.arange(10, 90, 10)))):
            for phi in np.radians(p.arange(0, 180, 10)):
                params.append((t, phi, radius))
    if simu == 'degrees-full':
        for t in np.reciprocal(np.cos(np.radians(np.arange(10, 90, 10)))):
            for phi in np.radians(np.arange(0, 360, 10)):
                params.append((t, phi, radius))
    if simu == 'degrees_test':
        for t in np.reciprocal(np.cos(np.radians(np.arange(10, 90, 10)))):
            for phi in np.radians(np.arange(0, 180, 10)):
                params.append((t, phi, radius))
    if simu == 'test2':
        print("This simulation is Test2 type")
        for t in np.reciprocal(np.cos(np.radians(np.arange(10, 11, 10)))):
            for phi in np.arange(0, 21, 20):
                params.append((t, phi, radius))
    if simu == 'test' or simu == 'sift':
        print("This simulation is Test type")
        pass
    print("%s -type params: %d" % (simu, len(params)))
    return tuple(params)

def  get_layer_number(obj_name):
    name, other = obj_name.split('_')
    if name == 'mltf':
        return 1
    elif name == 'crv':
        return 2
    elif name == 'pl':
        return 3
    else:
        return 3

if __name__ == "__main__":
    print(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
    #markers=["nabe", "menko", "glass", "ornament"]
    #pref_dirs=["pl_", "mltf_", "crv_"]
    markers=["menko"]
    pref_dirs=["pl_"]
    pardir=os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'data1'))
    if not os.path.exists(pardir):
        os.mkdir(pardir)
    bpy.data.scenes["Scene"].render.filepath=os.path.join(pardir, 'hoge')
    bpy.data.scenes["Scene"].layers=layer(0)
    bpy.data.scenes["Scene"].render.resolution_x=1920
    bpy.data.scenes["Scene"].render.resolution_y=1280
    bpy.data.scenes["Scene"].render.resolution_percentage=100
    #new_scene_objects("%s.png"%markers[0])
    #new_scene_objects("%s.png"%markers[1])
    params = calc_affine_params(simu='degrees-full', radius=12)
    for marker in markers:
        new_scene_objects("{}.png".format(marker))
        for pref_dir in pref_dirs:
            tmp =pref_dir + marker
            path = os.path.join(pardir, tmp)
            #print(path)
            if not os.path.exists(path):
                os.mkdir(path)
            compute_tilt_phi(params, path, get_layer_number(pref_dir))
            
