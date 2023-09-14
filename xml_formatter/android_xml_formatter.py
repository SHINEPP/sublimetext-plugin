import os
import re
import xml.etree.ElementTree as ET

NS_ANDROID = 'http://schemas.android.com/apk/res/android'
NS_APP = 'http://schemas.android.com/apk/res-auto'
NS_TOOLS = 'http://schemas.android.com/tools'

NS_DICT = {NS_ANDROID: 'android', NS_APP: 'app', NS_TOOLS: 'tools'}


class XmlFormatter:

    def __init__(self):
        self.namespace = {}
        self.elements = []
        self.last_element = None
        self.result = ''
        self.pattern = re.compile(r'\{(.+)}(.+)')

    def format(self, text):
        self.namespace.clear()
        self.elements.clear()
        self.last_element = None
        self.result = ''

        root = ET.fromstring(text)
        self._handle_namespace(root)

        self.result += '<?xml version="1.0" encoding="utf-8"?>'
        self._handle_element(root, 0, 0)
        return self.result

    def _handle_namespace(self, root):
        attrib = root.attrib
        for attr_key in attrib:
            match = self.pattern.match(attr_key)
            if match:
                name = match[1]
                if name in NS_DICT and name not in self.namespace:
                    self.namespace[name] = NS_DICT[name]
        for element in root:
            self._handle_namespace(element)

    def _handle_element(self, root, level, index):
        # tag start
        tag = root.tag
        parent = None
        if len(self.elements) > 0:
            parent = self.elements[-1]
        if index == 0:
            # 父tag至少2个attr
            if parent is not None and len(parent.attrib) >= 2:
                self.result += os.linesep
        else:
            # 前后tag不同
            if tag != self.last_element.tag:
                self.result += os.linesep

        space = " " * level * 4
        self.result += f'{os.linesep}{space}<{tag}'
        self.elements.append(root)
        self.last_element = root
        attr_lines = []

        # namespace
        have_ns = False
        if level == 0:
            have_ns = len(self.namespace) > 0
            for name in self.namespace:
                alize = self.namespace[name]
                attr_lines.append(f'xmlns:{alize}="{name}"')

        # 属性
        attrib = root.attrib
        for key in attrib:
            name = self._get_attr_name_alize(key)
            attr_lines.append(f'{name}="{attrib[key]}"')
        separator = f'\n{space}{" " * 4}'
        attr_count = len(attr_lines)
        if attr_count > 0:
            self.result += ' '
            if not have_ns and attr_count > 1:
                self.result += separator
        self.result += separator.join(attr_lines)

        # 处理子元素
        text = root.text
        if len(root) <= 0 and text is None:
            self.result += '/>'
        else:
            self.result += '>'
            if text is not None and len(text.strip()) > 0:
                self.result += text

            i = -1
            for element in root:
                i += 1
                self._handle_element(element, level + 1, i)
            if len(root) > 0:
                self.result += f'{os.linesep}{space}</{tag}>'
            else:
                self.result += f'</{tag}>'

        # tag end
        self.last_element = root
        self.elements.pop()

    def _get_attr_name_alize(self, key):
        """
        判读是否使用namespace, 如何存在则返回别名, 其他则key
        :param key:
        :return:
        """
        match = self.pattern.match(key)
        if match:
            name1, name2 = match[1], match[2]
            if name1 in self.namespace:
                alize = self.namespace[name1]
                return f'{alize}:{name2}'
        return key


if __name__ == '__main__':
    path = '/Users/zhouzhenliang/Desktop/sublime-plugin/AndroidManifest.xml'
    # path = '/Users/zhouzhenliang/Desktop/sublime-plugin/strings.xml'
    with open(path, 'r') as file:
        print(XmlFormatter().format(file.read()))
    exit(0)

import sublime
import sublime_plugin


class AndroidXmlFormatterCommand(sublime_plugin.TextCommand):
    def __init__(self, view):
        super().__init__(view)
        self._formatter = XmlFormatter()

    def run(self, edit):
        region = sublime.Region(0, self.view.size())
        text = self.view.substr(region)
        if len(text) > 0:
            result = self._formatter.format(text)
            if result != text:
                self.view.replace(edit, region, result)
