import xml.etree.ElementTree as ET


def parser(text):
    root = ET.fromstring(text)
    handle_element(root, 0)


def handle_element(root, index):
    space = " " * index * 4
    tag = root.tag
    print(f'{space}<{tag} ', end='')
    attr_lines = []
    attrib = root.attrib
    for key in attrib:
        attr_lines.append(f'{key}="{attrib[key]}"')
    print(f'\n{space}{" " * 4}'.join(attr_lines), end='')

    if len(root) <= 0:
        print('/>')
    else:
        print('>')
        for element in root:
            handle_element(element, index + 1)
        print(f'{space}</{tag}>')


if __name__ == '__main__':
    path = '/Users/zhouzhenliang/Desktop/apk2/FreshWallpapers_1.0.4/resources/AndroidManifest.xml'
    with open(path, 'r') as file:
        parser(file.read())
