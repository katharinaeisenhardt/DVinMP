import bpy
#print("------")

class Material:

    def set_cycles(self):
        scn = bpy.context.scene
        if not scn.render.engine == 'CYCLES':
            scn.render.engine = 'CYCLES'
            
    def make_material(self, name):
        activeObject = bpy.context.active_object
        #activeObject = bpy.context.selected_objects
        self.mat = bpy.data.materials.new(name)
        self.mat.use_nodes = True
        self.nodes = self.mat.node_tree.nodes
        if len(bpy.context.active_object.material_slots) == 0:
            activeObject.data.materials.append(self.mat)
        activeObject.data.materials[0] = self.mat
        
    def deleteBSDF1(self):
        nodes=self.mat.node_tree.nodes
        diffuse=nodes['Diffuse BSDF']
        nodes.remove(diffuse)
        
    def link(self, from_node, from_slot_name, to_node, to_slot_name):
        input = to_node.inputs[to_slot_name]
        output = from_node.outputs[from_slot_name]
        self.mat.node_tree.links.new(input, output)
        
    def makeNode(self, type, name):
        self.node = self.nodes.new(type)
        self.node.name = name
        self.xpos -= 200
        self.ypos += 200
        self.node.location = self.xpos, self.ypos
        return self.node
    
    def new_row():
        self.xpos = 0
        self.ypos += 200        
        
    def __init__(self):
        self.xpos = 0
        self.ypos = 0





