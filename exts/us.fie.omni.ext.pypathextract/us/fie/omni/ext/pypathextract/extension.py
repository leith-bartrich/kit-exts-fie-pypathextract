import omni.ext
import omni.ui as ui
import omni.kit
import omni.kit.app
import omni.kit.extensions
import omni.kit.mainwindow
import omni.kit.window.filepicker
import os
import os.path
import carb
import carb.tokens
import carb.settings


# Any class derived from `omni.ext.IExt` in top level module (defined in `python.modules` of `extension.toml`) will be
# instantiated when extension gets enabled and `on_startup(ext_id)` will be called. Later when extension gets disabled
# on_shutdown() is called.
class MyExtension(omni.ext.IExt):


    _save_win:omni.kit.window.filepicker.FilePickerDialog = None
    _window:ui.Window = None

    # ext_id is current extension id. It can be used with extension manager to query additional information, like where
    # this extension is located on filesystem.
    def on_startup(self, ext_id):
        print("[us.fie.omni.ext.pypathextract] FIE Python_Path Extractor startup")

        menu_path = f"Window/FIE Ext Path Extractor"
        self._menu = omni.kit.ui.get_editor_menu().add_item(menu_path,self.on_menu_click, True)




    def make_window(self):
        win_flags = ui.WINDOW_FLAGS_NO_CLOSE 
        self._window = ui.Window("FIE Python_Path Extractor", width=300, height=300,flags=win_flags)
        with self._window.frame:
            with ui.VStack(height=0):
                with ui.CollapsableFrame("Save Enabled"):
                    ui.Button("to .pth", clicked_fn=self.extract_enabled_exts_to_bat)
                with ui.CollapsableFrame("Save All"):
                    ui.Button("to .pth", clicked_fn=self.extract_all_exts_to_bat)


    def on_menu_click(self, menu, toggled):
        if self._window is None:
            self.make_window()
        self._window.visible = toggled
 


    def on_shutdown(self):
        print("[us.fie.omni.ext.pypathextract] FIE Python_Path Extractor shutdown")
        omni.kit.ui.get_editor_menu().remove_item(self._menu)
        if self._window is not None:
            self._window.destroy()


    def save_all_clicked(self, f_name:str, dir_name:str):
        self._save_win.hide() 
        if (f_name == ""):
            return
        if (dir_name == ""):
            return

        write_path = os.path.join(dir_name,f_name)


        app = omni.kit.app.get_app_interface()
        exman = app.get_extension_manager()
        extensions = exman.get_extensions()
        exman.get_extensions

        lines = []

        for ext in extensions:
            line = ext['path'] + "\n"
            lines.append(line)
        
        print("Writing all to: " + write_path)
        with open(write_path,'wt') as f:
            f.writelines(lines)

    def save_enabled_clicked(self, f_name:str,dir_name:str):
        self._save_win.hide() 
        if (f_name == ""):
            return
        if (dir_name == ""):
            return

        write_path = os.path.join(dir_name,f_name)


        app = omni.kit.app.get_app_interface()
        exman = app.get_extension_manager()
        extensions = exman.get_extensions()

        lines = []

        for ext in extensions:
            if ext['enabled'] == True:
                line = ext['path'] + "\n"
                lines.append(line)
        
        print("Writing enabled to: " + write_path)
        with open(write_path,'wt') as f:
            f.writelines(lines)

    def make_save_win(self):
        app_path = carb.tokens.get_tokens_interface().resolve("${app}")
        self._save_win = omni.kit.window.filepicker.FilePickerDialog(title="Save Ext Paths to File", current_directory=app_path,item_filter_options=['*.pth'])
        self._save_win.navigate_to(app_path)

    def extract_all_exts_to_bat(self):
        if self._save_win is None:
            self.make_save_win()

        self._save_win.set_click_apply_handler(self.save_all_clicked)
        self._save_win.show()


    def extract_enabled_exts_to_bat(self):
        if self._save_win is None:
            self.make_save_win()

        self._save_win.set_click_apply_handler(self.save_enabled_clicked)
        self._save_win.show()
        

