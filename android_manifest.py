import sublime
import sublime_plugin


class AndroidManifestCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.insert(edit, 0, "Hello, World!")


if __name__ == '__main__':
    print('test')
