#------------------------------------------------------------------------------
# Reynolds-Blender | The Blender add-on for Reynolds, an OpenFoam toolbox.
#------------------------------------------------------------------------------
# Copyright|
#------------------------------------------------------------------------------
#     Deepak Surti       (dmsurti@gmail.com)
#     Prabhu R           (IIT Bombay, prabhu@aero.iitb.ac.in)
#     Shivasubramanian G (IIT Bombay, sgopalak@iitb.ac.in)
#------------------------------------------------------------------------------
# License
#
#     This file is part of reynolds-blender.
#
#     reynolds-blender is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     reynolds-blender is distributed in the hope that it will be useful, but
#     WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
#     Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with reynolds-blender.  If not, see <http://www.gnu.org/licenses/>.
#------------------------------------------------------------------------------

# -----------
# bpy imports
# -----------
import bpy, bmesh
from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       EnumProperty,
                       PointerProperty,
                       IntVectorProperty,
                       FloatVectorProperty,
                       CollectionProperty
                       )
from bpy.types import (Panel,
                       Operator,
                       PropertyGroup,
                       UIList
                       )
from bpy.path import abspath
from mathutils import Matrix, Vector

# --------------
# python imports
# --------------
import operator
import os

# ------------------------
# reynolds blender imports
# ------------------------

from reynolds_blender.gui.register import register_classes, unregister_classes
from reynolds_blender.gui.attrs import set_scene_attrs, del_scene_attrs
from reynolds_blender.gui.custom_operator import create_custom_operators
from reynolds_blender.gui.renderer import ReynoldsGUIRenderer

# ----------------
# reynolds imports
# ----------------
from reynolds.dict.parser import ReynoldsFoamDict
from reynolds.foam.cmd_runner import FoamCmdRunner

# ------------------------------------------------------------------------
#    operators
# ------------------------------------------------------------------------

def generate_controldict(control_dict, scene):
    control_dict['startFrom'] = scene.cd_start_from
    control_dict['startTime'] = scene.cd_start_time
    control_dict['stopAt'] = scene.cd_stop_at
    control_dict['endTime'] = scene.cd_end_time
    control_dict['deltaT'] = scene.cd_delta_time
    control_dict['writeControl'] = scene.cd_write_control
    control_dict['writeInterval'] = scene.cd_write_interval
    control_dict['purgeWrite'] = scene.cd_purge_write
    control_dict['writeFormat'] = scene.cd_write_format
    control_dict['writePrecision'] = scene.cd_write_precision
    control_dict['writeCompression'] = scene.cd_write_compression
    control_dict['timeFormat'] = scene.cd_time_format
    control_dict['timePrecision'] = scene.cd_time_precision
    control_dict['runTimeModifiable'] = scene.cd_runtime_modifiable

# ------------------------------------------------------------------------
#    Panel
# ------------------------------------------------------------------------

class ControlDictOperator(bpy.types.Operator):
    bl_idname = "reynolds.of_controldict"
    bl_label = "ControlDict"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        scene = context.scene
        print('Generate controldict for solver: ' + scene.solver_name)
        abs_case_dir_path = bpy.path.abspath(scene.case_dir_path)
        control_dict = ReynoldsFoamDict('controlDict.foam')
        control_dict['application'] = scene.solver_name
        generate_controldict(control_dict, scene)

        system_dir = os.path.join(abs_case_dir_path, "system")
        if not os.path.exists(system_dir):
            os.makedirs(system_dir)
        controldict_file_path = os.path.join(system_dir, "controlDict")
        with open(controldict_file_path, "w+") as f:
            f.write(str(control_dict))
        return {'FINISHED'}

    # Return True to force redraw
    def check(self, context):
        return True

    def invoke(self, context, event):
        scene = context.scene
        return context.window_manager.invoke_props_dialog(self, width=1000)

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        gui_renderer = ReynoldsGUIRenderer(scene, layout, 'controlDict.yaml')
        gui_renderer.render()

# ------------------------------------------------------------------------
# register and unregister
# ------------------------------------------------------------------------

def register():
    register_classes(__name__)
    set_scene_attrs('controlDict.yaml')

def unregister():
    unregister_classes(__name__)
    del_scene_attrs('controlDict.yaml')

if __name__ == "__main__":
    register()
