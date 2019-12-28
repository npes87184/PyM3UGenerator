import sys
import remi.gui as gui
from remi import start, App
from lib import m3u

class M3uGenerator(App):
    def __init__(self, *args):
        super(M3uGenerator, self).__init__(*args)

    def on_select_btn_pressed(self, widget):
        self.folder_selection_dialog = gui.FileSelectionDialog('Folder Selection Dialog',
                                                'Select folder to generate m3u', False,
                                                '.', False)
        self.folder_selection_dialog.confirm_value.do(
            self.on_fileselection_dialog_confirm)

        # here is returned the Input Dialog widget, and it will be shown
        self.folder_selection_dialog.show(self)

    def on_fileselection_dialog_confirm(self, widget, filelist):
        if len(filelist) == 0:
            self.lbl.set_text('Please choose a folder')
        else:
            self.lbl.set_text(filelist[0])

    def on_go_btn_pressed(self, widget):
        doing_dialog = gui.GenericDialog("", "Doing", width=500, height=100)
        doing_dialog.show(self)
        m3u_path = m3u.gen_m3u(self.lbl.get_text())
        doing_dialog.hide()
        done_dialog = gui.GenericDialog("", "m3u created at [{}]".format(m3u_path), width=500, height=100)
        done_dialog.show(self)

    def main(self):
        body = gui.VBox(width='100%', height='100%')
        main_container = gui.VBox(width=400, height=140,
                        style={'align': 'center', 'border': '5px #FFAC55 solid'})
        btn_container = gui.HBox(width=300, height=30)
        link_to_github =  gui.Link('https://github.com/npes87184/PyM3UGenerator', 'Fork me here')

        self.lbl = gui.Label('Please choose a folder')
        self.select_bt = gui.Button('Select folder', width=100, height=30)
        self.go_bt = gui.Button('Go', width=100, height=30)

        self.select_bt.onclick.do(self.on_select_btn_pressed)
        self.go_bt.onclick.do(self.on_go_btn_pressed)

        btn_container.append(self.select_bt)
        btn_container.append(self.go_bt)

        main_container.append(self.lbl)
        main_container.append(btn_container)
        main_container.append(link_to_github)
        body.append(main_container)

        return body

if __name__ == '__main__':
    start(M3uGenerator)
