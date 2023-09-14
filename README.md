Android xml formatter Plugin
===============================

Sublime Text plugin that format android xml file.

## Installation:

- Add xml_formatter/android_xml_formatter.py to **Sublime Text**: Packages Folder

- Edit or add **Sublime Text** Packages Main.sublime-menu

```json
[
  {
    "id": "selection",
    "caption": "Selection",
    "children": [
      {
        "id": "android",
        "caption": "Android Formatter",
        "children": [
          {
            "caption": "Format XML",
            "command": "android_xml_formatter"
          }
        ]
      }
    ]
  }
]
```

- Edit or add **Sublime Text** Packages Context.sublime-menu

```json
[
  {
    "caption": "Format Android XML",
    "command": "android_xml_formatter",
    "id": "android_xml_formatter"
  }
]
```

## Usage:
- Click **Sublime Text** Menu (Selection/Android Formatter/Format XML)
- Click right mouse and choice Format Android XML
