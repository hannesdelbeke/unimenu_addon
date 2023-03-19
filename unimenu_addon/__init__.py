bl_info = {
    "name": "UniMenu",
    "description": "Customize your Blender menu to launch your add-ons & scripts",
    "author": "Hannes Delbeke",
    "wiki_url": "https://github.com/hannesdelbeke/unimenu/wiki/features-overview",
    "doc_url": "https://github.com/hannesdelbeke/unimenu/wiki/features-overview",
    "tracker_url": "https://github.com/hannesdelbeke/unimenu/issues",
    "version": (0, 3, 0),
    "blender": (2, 91, 0),
    "location": "",
    "support": "COMMUNITY",
    "category": "Interface",
}


import bpy
import os
import platform
import subprocess
import webbrowser
from pathlib import Path


menu_nodes = []


def open_file(path):
    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])


def open_modules_folder():
    user_modules_path = Path(bpy.utils.script_path_user()) / "addons/modules"
    if not user_modules_path.exists():
        user_modules_path.mkdir(parents=True)
    return open_file(user_modules_path)


class UserModulesPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    def draw(self, context):
        layout = self.layout
        try:
            import unimenu
            layout.label(text="UniMenu is installed.")
        except ImportError:
            layout.label(text="UniMenu is not installed. Download it from here:")
            layout.operator("wm.open_unimenu_url", text="1. Download UniMenu (open browser)")
            layout.label(text="Copy the unimenu folder to the modules folder & re-enable this add-on.")
            layout.operator("wm.open_user_addons_modules_folder", text="2. Open modules folder (install here)")
            layout.label(text="If successful, this text should be gone now.")


class UserModulesOperator(bpy.types.Operator):
    bl_idname = "wm.open_user_addons_modules_folder"
    bl_label = "Open the modules folder (install unimenu in here)"

    def execute(self, context):
        open_modules_folder()
        return {'FINISHED'}

class BrowseUnimenuOperator(bpy.types.Operator):
    bl_idname = "wm.open_unimenu_url"
    bl_label = "Open the unimenu URL"

    def execute(self, context):
        url = "https://github.com/hannesdelbeke/unimenu"
        webbrowser.open(url)
        return {'FINISHED'}


def setup_menu():
    """Setup the menu if unimenu is installed. Returns True if successful."""
    try:
        import unimenu
        os.environ["UNIMENU_CONFIG_PATH"] = str(Path(__file__).parent / "configs")
        global menu_nodes
        menu_nodes = unimenu.setup_all_configs()
        return True
    except ImportError:
        print("unimenu is not installed. Install it in the modules folder.\n"
              "You can open the modules folder from the add-on preferences.\n"
              "by clicking on the 'Open modules folder' button in the unimenu add-on")
        return False


def teardown_menu():
    """Teardown the menu if unimenu is installed. Returns True if successful."""
    try:
        import unimenu
        global menu_nodes
        for node in menu_nodes:
            node.teardown()
        return True
    except Exception as e:
        print("unimenu teardown failed:")
        import traceback
        traceback.print_exc()


def register():
    success = setup_menu()
    bpy.utils.register_class(UserModulesOperator)
    bpy.utils.register_class(BrowseUnimenuOperator)
    bpy.utils.register_class(UserModulesPreferences)

def unregister():
    teardown_menu()
    bpy.utils.unregister_class(UserModulesOperator)
    bpy.utils.unregister_class(BrowseUnimenuOperator)
    bpy.utils.unregister_class(UserModulesPreferences)

