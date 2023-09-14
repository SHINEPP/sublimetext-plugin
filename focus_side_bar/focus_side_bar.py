import sublime
import sublime_plugin


class FocusSideBarCommand(sublime_plugin.WindowCommand):

    def run_(self, edit_token, args):
        self.window.run_command("focus_side_bar")
