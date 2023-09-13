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
        self.pattern = re.compile(r'\{(.+)}(.+)')

    def format(self, text):
        root = ET.fromstring(text)
        self.handle_namespace(root)
        print('<?xml version="1.0" encoding="utf-8"?>')
        self.handle_element(root, 0, 0)

    def handle_namespace(self, root):
        attrib = root.attrib
        for attr_key in attrib:
            match = self.pattern.match(attr_key)
            if match:
                name = match[1]
                if name in NS_DICT and name not in self.namespace:
                    self.namespace[name] = NS_DICT[name]
        for element in root:
            self.handle_namespace(element)

    def handle_element(self, root, level, index):
        tag = root.tag
        if self.last_element is None or tag != self.last_element.tag:
            if index > 0:
                print()
            elif len(self.elements) > 0 and len(self.elements[-1].attrib) > 0:
                print()

        # tag start
        self.elements.append(root)
        self.last_element = root
        space = " " * level * 4
        print(f'{space}<{tag}', end='')
        attr_lines = []

        # namespace
        if level == 0:
            for name in self.namespace:
                alize = self.namespace[name]
                attr_lines.append(f'xmlns:{alize}="{name}"')

        # 属性
        attrib = root.attrib
        for key in attrib:
            name = self.get_attr_name_alize(key)
            attr_lines.append(f'{name}="{attrib[key]}"')
        separator = f'\n{space}{" " * 4}'
        attr_count = len(attr_lines)
        if attr_count > 0:
            print(' ', end='')
            if attr_count > 1 and (is_tag_attr_newline(tag) or attr_count == 2):
                print(separator, end='')
        print(separator.join(attr_lines), end='')

        # 处理子元素
        if len(root) <= 0:
            print('/>')
        else:
            print('>')
            i = -1
            for element in root:
                i += 1
                self.handle_element(element, level + 1, i)
            print(f'{space}</{tag}>')

        # tag end
        self.last_element = root
        self.elements.pop()

    def get_attr_name_alize(self, key):
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


def is_tag_attr_newline(tag):
    return tag in ['application', 'activity', 'activity-alias', 'provider', 'service', 'receiver', 'uses-feature',
                   'uses-permission', 'meta-data']


if __name__ == '__main__':
    path = '/Users/zhouzhenliang/Desktop/apk2/FreshWallpapers_1.0.4/resources/AndroidManifest.xml'
    with open(path, 'r') as file:
        AndroidXmlFormatter().format(file.read())
