bl_info = {
    "name": "Gear Generator",
    "author": "Katharina Eisenhardt, Matthias Mühl, Maria Morgillo",
    "version": (1, 0),
    "blender": (2, 75, 0),
    "location": "View3D > Add > Mesh > New Object",
    "description": "Adds a new Mesh Object",
    "warning": "",
    "wiki_url": "",
    "category": "Add Mesh",
    }

import sys
import os
import bpy
from bpy.types import Operator
from bpy.props import FloatVectorProperty
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector

dir = os.path.dirname(bpy.data.filepath)
if dir not in sys.path:
   sys.path.append(dir )
   

import apply_material
import imp
imp.reload(apply_material)
apply_material.Material()
from apply_material import *
bpy.context.scene.render.engine = 'CYCLES'


############# ADD OBJECT METHOD #############

def add_object(self, context):
    
    teeth = self.teeth
    tooth_length = self.tooth_length
    
    outer_radius = self.outer_radius
    central_axis = self.central_axis
    
    tooth_distance = self.tooth_distance
    tooth_edges = 1
    
    spokes_count = self.spokes_count
    cuttingDepth = self.cuttingDepth  
      
    squareShape=True     
    hasSpokes = self.hasSpokes
    
    inner_radius = self.inner_radius
    spoke_scale = self.spoke_scale  
    spindel_faces = self.spindel_faces
    
    off_set = 0
    
############# Create Cylinder with teeth #################

    def create_cylinder_with_teeth():
        
        #Startcylinder
        bpy.ops.mesh.primitive_cylinder_add(vertices=(((teeth-1)*tooth_distance)+tooth_distance), radius=outer_radius, depth=1, enter_editmode=False)
        
        #Editmodus
        bpy.ops.object.editmode_toggle()        
        bpy.context.tool_settings.mesh_select_mode = (False,True,False)   
        bpy.ops.mesh.select_all(action='TOGGLE')

        #select sharp edges and invert 
        bpy.ops.mesh.edges_select_sharp()  
        bpy.ops.mesh.select_all(action='INVERT')    

        #select every nth element
        bpy.ops.mesh.select_nth(nth=tooth_distance, skip=tooth_edges, offset=off_set)   

        #extrude theeth
        bpy.ops.transform.resize(value=(tooth_length, tooth_length, 1), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)

        #Objecmodus
        bpy.ops.object.editmode_toggle()
        
        #rename selected Object to "CylinderWithTeeth"
        for obj in bpy.context.selected_objects:
            obj.name = "CylinderWithTeeth"

########################################################    
        
    def create_cylinder_with_square():
        #Startcylinder
        bpy.ops.mesh.primitive_cylinder_add(vertices=(((teeth-1)*tooth_distance)+tooth_distance), radius=outer_radius, depth=1, enter_editmode=False)
        
        bpy.ops.object.editmode_toggle()   
        bpy.context.tool_settings.mesh_select_mode = (False,False,True)

        #deselected alles 
        bpy.ops.mesh.select_all(action='TOGGLE')    

        #wählt Mantelflächen aus, nicht Kreisflächen (Enden) des Zylinders
        bpy.ops.mesh.select_face_by_sides()     

        bpy.ops.mesh.select_nth(nth=tooth_distance, skip=tooth_edges, offset=off_set)    

        bpy.ops.mesh.extrude_faces_move(MESH_OT_extrude_faces_indiv={"mirror":False}, TRANSFORM_OT_shrink_fatten={"value": -tooth_length/4, "use_even_offset":False, "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "release_confirm":False})

        #wechselt in den Object Mode
        bpy.ops.object.editmode_toggle()    
        bpy.context.tool_settings.mesh_select_mode = (False,True,False)


        #rename selected Object to "CylinderWithTeeth"
        for obj in bpy.context.selected_objects:
            obj.name = "CylinderWithTeeth"
            
        #faces werden verbunden
        bpy.data.objects['CylinderWithTeeth'].select = True
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='TOGGLE')
        bpy.ops.mesh.edge_face_add()
        bpy.ops.object.editmode_toggle()

########### SELECT THOOTH SHAPE ####################

    if self.shape_enum == "Pointy":
        create_cylinder_with_teeth()
        
    if self.shape_enum =="Square":
        create_cylinder_with_square()
            
    if self.shape_enum == "Rounded":
        create_cylinder_with_teeth()
        
        #creates Cylinder with bigger radius than CylinderWithTeeth 
        bpy.ops.mesh.primitive_cylinder_add(radius=outer_radius+tooth_length+0.01, depth=2, view_align=False, enter_editmode=False, layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
        bpy.ops.transform.resize(value=(tooth_length, tooth_length, 1), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
        
        #rename to "ZylinderNegShape"
        for obj in bpy.context.selected_objects:
            obj.name = "ZylinderNegShape"
        
        #creates cylinder and cut a hole in ZylinderNegShape  
        bpy.ops.mesh.primitive_cylinder_add(radius=outer_radius, depth=2, view_align=False, enter_editmode=False, layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
        bpy.ops.transform.resize(value=(tooth_length-cuttingDepth, tooth_length-cuttingDepth, 1.4), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
            
        #remane to ZylinderNegShapeHole
        for obj in bpy.context.selected_objects:
            obj.name = "ZylinderNegShapeHole"
                
        #Cutting Hole
        bpy.context.scene.objects.active = bpy.data.objects["ZylinderNegShape"]
        bpy.ops.object.modifier_add(type='BOOLEAN')
        bpy.context.object.modifiers["Boolean"].operation = 'DIFFERENCE'
        bpy.context.object.modifiers["Boolean"].object = bpy.data.objects["ZylinderNegShapeHole"]
        bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Boolean")
         
        #delete cylinder that was used to cut (ZylinderNegShapeHole)
        bpy.data.objects['ZylinderNegShape'].select = False
        bpy.data.objects['ZylinderNegShapeHole'].select = True
        bpy.ops.object.delete()
            
        #cut the theeth: Subtract --> ZylinderNegShape - CylinderWithTeeth  
        bpy.context.scene.objects.active = bpy.data.objects["CylinderWithTeeth"]
        bpy.ops.object.modifier_add(type='BOOLEAN')
        bpy.context.object.modifiers["Boolean"].operation = 'DIFFERENCE'
        bpy.context.object.modifiers["Boolean"].object = bpy.data.objects["ZylinderNegShape"]
        bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Boolean")
           
           
        #delete Cylinder that was used to cut (ZylinderNegShape)
        bpy.data.objects['CylinderWithTeeth'].select = False
        bpy.data.objects['ZylinderNegShape'].select = True
        bpy.ops.object.delete()
        
        #faces werden verbunden
        bpy.data.objects['CylinderWithTeeth'].select = True
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='TOGGLE')
        bpy.ops.mesh.edge_face_add()
        bpy.ops.object.editmode_toggle()

################ SPOKED GEAR #####################

    if hasSpokes == True:
        if inner_radius > outer_radius:
            inner_radius= outer_radius-0.1
        #erstellt Zylinder für negativ Fläche, (Loch ausschneiden)
        bpy.ops.mesh.primitive_cylinder_add(vertices=teeth*3, radius = inner_radius, depth=2, enter_editmode=False)
        
        #gibt selektiertem Objekt einen Namen, Zylinder der ausschneidet
        for obj in bpy.context.selected_objects:
            obj.name = "CylinderCuttingInnerRadius"  

        #Im folgenden wird per boolean modifier die überlappende Fläche ausgeschnitten
        bpy.data.objects['CylinderWithTeeth'].select = True     
        bpy.data.objects['CylinderCuttingInnerRadius'].select = True

        bpy.ops.object.join()
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.intersect_boolean()
        bpy.ops.object.editmode_toggle()        

        #gibt selektiertem Objekt einen Namen, Zylinder der vorher nur Zähne hat jetzt mit Loch
        for obj in bpy.context.selected_objects:
            obj.name = "AnnularGear"
   
        #erstellt Zylinder für negativ Fläche (Speichenlöcher ausschneiden) mit doppelter Anzahl an Flächen als Speichen, 3x so großem Radius/Scale
        bpy.ops.mesh.primitive_cylinder_add(vertices=spokes_count *2,radius=spoke_scale*3, enter_editmode=False)

        #wechselt in den Edit mode
        bpy.ops.object.editmode_toggle()   
        bpy.context.tool_settings.mesh_select_mode = (False,False,True)

        #wählt alles aus
        bpy.ops.mesh.select_all(action='TOGGLE')    

        #wählt Mantelflächen aus, nicht Kreisflächen (Enden) des Zylinders
        bpy.ops.mesh.select_face_by_sides()     

        bpy.ops.mesh.select_nth(nth=2, skip=1, offset=1)    

        bpy.ops.mesh.extrude_faces_move(MESH_OT_extrude_faces_indiv={"mirror":False}, TRANSFORM_OT_shrink_fatten={"value": -1.4, "use_even_offset":False, "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "release_confirm":False})

        #wechselt in den Object Mode
        bpy.ops.object.editmode_toggle()    
        bpy.context.tool_settings.mesh_select_mode = (False,True,False)

        bpy.ops.transform.resize(value=(inner_radius/1.78, inner_radius/1.78, 0.48), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)

        #gibt selektiertem Objekt einen Namen, Zylinder der Speichen ausschneidet
        for obj in bpy.context.selected_objects:
            obj.name = "CylinderCuttingSpokes"

        #Im folgenden wird per boolean modifier die überlappende Fläche ausgeschnitten
        bpy.data.objects['AnnularGear'].select = True   
        bpy.data.objects['CylinderCuttingSpokes'].select = True

        bpy.ops.object.join()  
        
    #wechselt in den Edit Mode 
    bpy.ops.object.editmode_toggle()    

    #gibt selektiertem Objekt einen Namen, Zahnrad wird zu Speichenrad
    for obj in bpy.context.selected_objects:
        obj.name = "SpokedGear"
    #wechselt in den Object Mode
    bpy.ops.object.editmode_toggle() 
      
    #erstellt Zylinder für negativ Fläche, (Loch für Mittelachse ausschneiden) 
    bpy.ops.mesh.primitive_cylinder_add(vertices=spindel_faces, radius=central_axis, depth=2, enter_editmode=False)   

    #gibt selektiertem Objekt einen Namen, Zylinder der Mittelachse ausschneidet
    for obj in bpy.context.selected_objects:
        obj.name = "CylinderCuttingCentralAxis"

    #Im folgenden wird per boolean modifier die überlappende Fläche ausgeschnitten
    bpy.data.objects['SpokedGear'].select = True   
    bpy.data.objects['CylinderCuttingCentralAxis'].select = True

    bpy.ops.object.join()
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.intersect_boolean()
    bpy.ops.object.editmode_toggle()


    ### Physik ###
    
    bpy.ops.rigidbody.objects_add(type='ACTIVE') 
    
    #bpy.ops.transform.rotate(value=1.5708, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)

    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)   
    bpy.context.object.rigid_body.collision_shape = 'MESH'
    bpy.context.object.rigid_body.collision_margin = 0.001
    bpy.context.object.rigid_body.friction = 0.1
    bpy.context.object.rigid_body.use_deactivation = True
    bpy.context.object.rigid_body.linear_damping = 0.4
    bpy.context.object.rigid_body.angular_damping = 0.3
    bpy.ops.transform.resize(value=(0.271443, 0.271443, 0.271443), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)

    #gibt selektiertem Objekt einen Namen, Speichenrad wird zu fertigem Gear (Zahnrad)
    for obj in bpy.context.selected_objects:
        obj.name = "Gear"
        
############### MATERIAL ON GEAR ####################
    
    if self.material_gear == "SILVER":
        m = apply_material.Material()
        m.set_cycles()
        m.make_material('silver')
        m.deleteBSDF1()
        
        materialOutput = m.nodes['Material Output']
        glossyBSDF = m.makeNode('ShaderNodeBsdfGlossy', 'Glossy BSDF')
        glossyBSDF.inputs[1].default_value = 0.02
        
        #link Glossy Shader to Material Output
        m.link(glossyBSDF, 'BSDF', materialOutput, 'Surface')
        
        #make RGB Node
        rgb = m.makeNode('ShaderNodeRGB','RGB')
        rgb.outputs["Color"].default_value = [0.972, 0.960, 0.915, 1]
        
        #link RGB Node to GlossyShader
        m.link(rgb, 'Color', glossyBSDF, 'Color')
    
    if self.material_gear == "GOLD":
        m = apply_material.Material()

        m.make_material('gold')
        m.deleteBSDF1()
        
        materialOutput = m.nodes['Material Output']
        glossyBSDF = m.makeNode('ShaderNodeBsdfGlossy', 'Glossy BSDF')
        glossyBSDF.inputs[1].default_value = 0.02
        
        #link Glossy Shader to Material Output
        m.link(glossyBSDF, 'BSDF', materialOutput, 'Surface')
        
        #make RGB Node
        rgb = m.makeNode('ShaderNodeRGB','RGB')
        rgb.outputs["Color"].default_value = [1, 0.766, 0.366, 1]
        
        #link RGB Node to GlossyShader
        m.link(rgb, 'Color', glossyBSDF, 'Color')
        
    if self.material_gear == "IRON":
        m = apply_material.Material()
        
        m.make_material('iron')
        m.deleteBSDF1()
        
        materialOutput = m.nodes['Material Output']
        glossyBSDF = m.makeNode('ShaderNodeBsdfGlossy', 'Glossy BSDF')
        glossyBSDF.inputs[1].default_value = 0.02
        
        #link Glossy Shader to Material Output
        m.link(glossyBSDF, 'BSDF', materialOutput, 'Surface')
        
        #make RGB Node
        rgb = m.makeNode('ShaderNodeRGB','RGB')
        rgb.outputs["Color"].default_value = [0.560, 0.570, 0.580, 1]
        
        #link RGB Node to GlossyShader
        m.link(rgb, 'Color', glossyBSDF, 'Color')
        
    if self.material_gear == "CUPPER":
        m = apply_material.Material()
        
        m.make_material('cupper')
        m.deleteBSDF1()
        
        materialOutput = m.nodes['Material Output']
        glossyBSDF = m.makeNode('ShaderNodeBsdfGlossy', 'Glossy BSDF')
        glossyBSDF.inputs[1].default_value = 0.02
        
        #link Glossy Shader to Material Output
        m.link(glossyBSDF, 'BSDF', materialOutput, 'Surface')
        
        #make RGB Node
        rgb = m.makeNode('ShaderNodeRGB','RGB')
        rgb.outputs["Color"].default_value = [0.955, 0.637, 0.538, 1]
        
        #link RGB Node to GlossyShader
        m.link(rgb, 'Color', glossyBSDF, 'Color')
        
#################################################

    #erstellt Zylinder mit ? Flächen, größe des Zylinders mit Abstand zur Mittelachse, dicke und Bearbeitungsmodus
    bpy.ops.mesh.primitive_cylinder_add(vertices=spindel_faces, radius=central_axis-0.01, depth=0.7, enter_editmode=False,)
    
    #????Spindel ist passive und steht fest im Raum (warum rotiert es in die selbe Richtung wie Zahnrad) mit Physik?
    bpy.ops.rigidbody.objects_add(type='PASSIVE')   
    #bpy.ops.transform.rotate(value=1.5708, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)

    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)   
    bpy.context.object.rigid_body.collision_margin = 0.001
    bpy.context.object.rigid_body.friction = 0.1

    #gibt selektiertem Objekt einen Namen, Zylinder wird zu Spindel (Achse)
    for obj in bpy.context.selected_objects:
        obj.name = "Spindle"

    #select gear and spindle
    bpy.data.objects['Gear'].select = True  
    bpy.data.objects['Spindle'].select = True
    bpy.ops.rigidbody.connect() 

    #alles wird deselected
    bpy.ops.object.select_all(action='DESELECT')   

    bpy.data.objects['Constraint'].select = True   
    #bpy.ops.transform.rotate(value=1.5708, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)

    bpy.data.objects['Constraint'].rigid_body_constraint.type = 'HINGE'
    
    bpy.ops.object.select_all(action='TOGGLE')
    
    bpy.data.objects['Gear'].select = True
    bpy.data.objects['Spindle'].select = True
    bpy.data.objects['Constraint'].select = True

    bpy.ops.transform.rotate(value=1.5708, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
    bpy.ops.group.create()
    bpy.ops.object.select_all(action='TOGGLE')

    bpy.data.objects['Gear'].select = True
    for obj in bpy.context.selected_objects:
        obj.name = "Gear_2"
    
    bpy.ops.object.select_all(action='TOGGLE')
        
    bpy.data.objects['Spindle'].select = True
    for obj in bpy.context.selected_objects:
        obj.name = "Gear_Axis"
    

    bpy.ops.object.select_all(action='TOGGLE')

    bpy.data.objects['Constraint'].select = True
    for obj in bpy.context.selected_objects:
        obj.name = "Physics_Axis"
    
    bpy.ops.object.select_all(action='TOGGLE')
    bpy.data.objects['Gear_2'].select = True
    bpy.data.objects['Gear_Axis'].select = True
    bpy.data.objects['Physics_Axis'].select = True

    bpy.ops.object.select_all(action='TOGGLE')


    # useful for development when the mesh may be invalid.
    # mesh.validate(verbose=True)

########################### MATERIAL ON SPINDEL ###########################################
    
    if self.material_spindel == "SILVER":
        m = apply_material.Material()
        
        m.make_material('silver')
        m.deleteBSDF1()
        
        materialOutput = m.nodes['Material Output']
        glossyBSDF = m.makeNode('ShaderNodeBsdfGlossy', 'Glossy BSDF')
        glossyBSDF.inputs[1].default_value = 0.02
        
        #link Glossy Shader to Material Output
        m.link(glossyBSDF, 'BSDF', materialOutput, 'Surface')
        
        #make RGB Node
        rgb = m.makeNode('ShaderNodeRGB','RGB')
        rgb.outputs["Color"].default_value = [0.972, 0.960, 0.915, 1]
        
        #link RGB Node to GlossyShader
        m.link(rgb, 'Color', glossyBSDF, 'Color')
    
    if self.material_spindel == "GOLD":
        m = apply_material.Material()
        
        m.make_material('gold')
        m.deleteBSDF1()
        
        materialOutput = m.nodes['Material Output']
        glossyBSDF = m.makeNode('ShaderNodeBsdfGlossy', 'Glossy BSDF')
        glossyBSDF.inputs[1].default_value = 0.02
        
        #link Glossy Shader to Material Output
        m.link(glossyBSDF, 'BSDF', materialOutput, 'Surface')
        
        #make RGB Node
        rgb = m.makeNode('ShaderNodeRGB','RGB')
        rgb.outputs["Color"].default_value = [1, 0.766, 0.366, 1]
        
        #link RGB Node to GlossyShader
        m.link(rgb, 'Color', glossyBSDF, 'Color')
        
    if self.material_spindel == "IRON":
        m = apply_material.Material()
        
        m.make_material('iron')
        m.deleteBSDF1()
        
        materialOutput = m.nodes['Material Output']
        glossyBSDF = m.makeNode('ShaderNodeBsdfGlossy', 'Glossy BSDF')
        glossyBSDF.inputs[1].default_value = 0.02
        
        #link Glossy Shader to Material Output
        m.link(glossyBSDF, 'BSDF', materialOutput, 'Surface')
        
        #make RGB Node
        rgb = m.makeNode('ShaderNodeRGB','RGB')
        rgb.outputs["Color"].default_value = [0.560, 0.570, 0.580, 1]
        
        #link RGB Node to GlossyShader
        m.link(rgb, 'Color', glossyBSDF, 'Color')
        
    if self.material_spindel == "CUPPER":
        m = apply_material.Material()
    
        m.make_material('cupper')
        m.deleteBSDF1()
        
        materialOutput = m.nodes['Material Output']
        glossyBSDF = m.makeNode('ShaderNodeBsdfGlossy', 'Glossy BSDF')
        glossyBSDF.inputs[1].default_value = 0.02

        #link Glossy Shader to Material Output
        m.link(glossyBSDF, 'BSDF', materialOutput, 'Surface')
        
        #make RGB Node
        rgb = m.makeNode('ShaderNodeRGB','RGB')
        rgb.outputs["Color"].default_value = [0.955, 0.637, 0.538, 1]
        
        #link RGB Node to GlossyShader
        m.link(rgb, 'Color', glossyBSDF, 'Color')

####################################################################################
        
### Panels ###
class OBJECT_OT_add_object(Operator, AddObjectHelper):
    """Create a new Mesh Object"""
    bl_idname = "mesh.add_object"
    bl_label = "Add Gear Generator"
    bl_options = {'REGISTER', 'UNDO'}

    teeth = bpy.props.IntProperty(
        name="Teeth",
        description="This is a default value for the number of gear teeth",
        default=12,
        min=5,
        max=30
        )
    
    tooth_length = bpy.props.FloatProperty(
        name="Tooth Length",
        description="This is a default value for the length of the teeth",
        default=1.4,
        min=1,
        max=10
        )

    tooth_distance = bpy.props.IntProperty(
        name="Tooth Distance",
        description="This is a default value for the distance between each tooth",
        default=3,
        min=3,
        max=10
        )

    outer_radius = bpy.props.FloatProperty(
        name="Outer Radius",
        description="This is a default value for the outer radius",
        default=0.5,
        min=0.3,
        max=5,
        )
        
    central_axis = bpy.props.FloatProperty(
        name="Central Axis",
        description="This is a default value for the radius of the central axis",
        default=0.1,
        min=0.01,
        max=10
        )
    
    spindel_faces = bpy.props.IntProperty(
        name="Spindel Faces",
        description="This is a default value for the number of spindel faces",
        default=40,
        min=4,
        max=40
    )

    material_gear = bpy.props.EnumProperty(
        name = "Gear Material",
        description = "Different gear materials",
        items = [
            ("STANDARD" , "None" , "Description..."),
            ("SILVER" , "Silver" , "Description..."),
            ("GOLD", "Gold", "other description"),
            ("IRON", "Iron", "other description"),
            ("CUPPER", "Cupper", "Some other description")            
        ]
        
    )
    
    material_spindel = bpy.props.EnumProperty(
        name = "Spindel Material",
        description = "Different spindel materials",
        items = [
            ("STANDARD" , "None" , "Description..."),
            ("SILVER" , "Silver" , "Description..."),
            ("GOLD", "Gold", "other description"),
            ("IRON", "Iron", "other description"),
            ("CUPPER", "Cupper", "Some other description")            
        ]
        
    )
    
    
    shape_enum = bpy.props.EnumProperty(
        name = "Tooth Shape",
        description = "Different tooth shapes",
        items = [
            ("Pointy", "Pointy", "Create a pointy tooth shape"),
            ("Rounded", "Rounded", "Create a rounded tooth shape"),
            ("Square", "Square", "Create a square tooth shape"),
        ]
        
    )
    
    cuttingDepth = bpy.props.FloatProperty(
        name="Cutting Depth",
        description="This is a default value for the cutting depth to form the teeth",
        default=0.2,
        min=0,
        max=1  #max so tief geschnitten wie teethlengt/2
        )
    
    hasSpokes = bpy.props.BoolProperty(
        name="Spoked Gear",
        description="Adds parameters to create a spoked gear",
        default = True
    )
        
    inner_radius = bpy.props.FloatProperty(
        name="Inner Radius",
        description="This is a default value for inner radius of the gear",
        default=0.4,
        min=0.1,
        max= 10,
        )
        
    spokes_count = bpy.props.IntProperty(
        name="Spokes",
        description="This is a default value for the number of gear spokes",
        default=5,
        min=2,
        max=10
        )

    spoke_scale = bpy.props.FloatProperty(
        name="Spoke Size",
        description="This is a default value for the scale of the spokes",
        default=0.2,
        min=0.2,
        max=10
        )
   
    def execute(self, context):
        add_object(self, context)
        return {'FINISHED'}
    
    
class add_gear(bpy.types.Panel):
    bl_idname = "panel.gearGenerator"
    bl_label = "Gear Generator"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    # bl_category = "Tools"
    bl_category = "Gear Generator"
 
    def draw(self, context):
        self.layout.operator("mesh.add_object")
        

def add_object_button(self, context):
    self.layout.operator(
        OBJECT_OT_add_object.bl_idname,
        text="Add Gear Generator",
        icon='SCRIPTWIN')


# This allows you to right click on a button and link to the manual
def add_object_manual_map():
    url_manual_prefix = "https://docs.blender.org/manual/en/dev/"
    url_manual_mapping = (
        ("bpy.ops.mesh.add_object", "editors/3dview/object"),
        )
    return url_manual_prefix, url_manual_mapping

### register/unregister ####
def register():
    bpy.utils.register_class(OBJECT_OT_add_object)
    bpy.utils.register_manual_map(add_object_manual_map)
    bpy.types.INFO_MT_mesh_add.append(add_object_button)
    bpy.utils.register_class(add_gear)
    
def unregister():
    bpy.utils.unregister_class(OBJECT_OT_add_object)
    bpy.utils.unregister_manual_map(add_object_manual_map)
    bpy.types.INFO_MT_mesh_add.remove(add_object_button)
    bpy.utils.register_class(add_gear)

if __name__ == "__main__":
    register()