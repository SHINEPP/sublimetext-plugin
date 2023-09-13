import os
import re
import xml.etree.ElementTree as ET

NS_ANDROID = 'http://schemas.android.com/apk/res/android'
NS_APP = 'http://schemas.android.com/apk/res-auto'
NS_TOOLS = 'http://schemas.android.com/tools'

NS_DICT = {NS_ANDROID: 'android', NS_APP: 'app', NS_TOOLS: 'tools'}


class AndroidXmlFormatter:

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

        self.result += '<?xml version="1.0" encoding="utf-8"?>' + os.linesep
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
        tag = root.tag
        if index == 0 or self.last_element is None or tag != self.last_element.tag:
            if index > 0:
                self.result += os.linesep
            elif len(self.elements) > 0 and len(self.elements[-1].attrib) > 1:
                self.result += os.linesep

        # tag start
        self.elements.append(root)
        self.last_element = root
        space = " " * level * 4
        self.result += f'{space}<{tag}'
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
        if len(root) <= 0:
            self.result += '/>' + os.linesep
        else:
            self.result += '>' + os.linesep
            i = -1
            for element in root:
                i += 1
                self._handle_element(element, level + 1, i)
            self.result += f'{space}</{tag}>{os.linesep}'

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
    path = '/Users/zhouzhenliang/Desktop/apk2/FreshWallpapers_1.0.4/resources/AndroidManifest.xml'
    with open(path, 'r') as file:
        print(AndroidXmlFormatter().format(file.read()))