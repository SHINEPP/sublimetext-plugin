import re
import xml.etree.ElementTree as ET
from collections import OrderedDict


class ManifestFormatter:

    def __init__(self):
        self.namespace = []
        self.pattern = re.compile(r'\{(.+)}(.+)')

    def format(self, text):
        root = ET.fromstring(text)
        print('<?xml version="1.0" encoding="utf-8"?>')
        self.handle_element(root, 0)

    def handle_element(self, root, index):
        space = " " * index * 4
        tag = root.tag
        print(f'{space}<{tag}', end='')
        attr_lines = []
        attrib = root.attrib

        # namespace start
        namespace_count = 0
        for key in attrib:
            name, alize = self.match_namespace(key)
            if name and not self.is_in_namespace(name):
                self.namespace.append((name, alize))
                namespace_count += 1
                attr_lines.append(f'xmlns:{alize}="{name}"')

        # 属性
        for key in attrib:
            name = self.key_name_alize(key)
            attr_lines.append(f'{name}="{attrib[key]}"')
        if len(attr_lines) > 0:
            print(' ', end='')
            if is_tag_newline(tag):
                print(f'\n{space}{" " * 4}', end='')
        print(f'\n{space}{" " * 4}'.join(attr_lines), end='')

        # 处理子元素
        if len(root) <= 0:
            print('/>')
        else:
            print('>')
            for element in root:
                self.handle_element(element, index + 1)
            print(f'{space}</{tag}>')

        # namespace end
        for i in range(namespace_count):
            self.namespace.pop()

    def match_namespace(self, key):
        match = self.pattern.match(key)
        if match:
            return match[1], match[1].split('/')[-1]
        return None, None

    def is_in_namespace(self, name) -> bool:
        for value, _ in self.namespace:
            if name == value:
                return True
        return False

    def key_name_alize(self, key):
        match = self.pattern.match(key)
        if match:
            name1, name2 = match[1], match[2]
            for value, alize in self.namespace:
                if name1 == value:
                    return f'{alize}:{name2}'
        return key


def is_tag_newline(tag):
    return tag in ['uses-sdk', 'uses-feature', 'uses-library', 'permission', 'meta-data', 'application', 'activity',
                   'activity-alias', 'provider', 'service', 'receiver', ]


if __name__ == '__main__':
    path = '/Users/zhouzhenliang/Desktop/apk2/FreshWallpapers_1.0.4/resources/AndroidManifest.xml'
    with open(path, 'r') as file:
        ManifestFormatter().format(file.read())
