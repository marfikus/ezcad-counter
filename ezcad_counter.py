
# классный скрипт, можно много чего делать с его помощью, значительно облегчает работу
from winGuiAuto import *
import time
import os
import configparser


PROGRAM_VERSION = "1.0.0"

CONFIG_FILE = "ezcad_counter.ini"
MESSAGE_FILE = "message.bat"

DEFAULT_CONFIG = {
    "max_count": 200,
    "delay": 2,
    "window_title": "L-Master",
    "element_title": "Кол.прох.",
    "shift_from_element": -1,
    "debug_print": False,
}
config = {}

def load_config():
    global config

    def load_key(parser, key, type="str"):
        try:
            if type == "str":
                value = parser["DEFAULT"][key]
            elif type == "int":
                value = int(parser["DEFAULT"][key])
            elif type == "float":
                value = float(parser["DEFAULT"][key])
            elif type == "bool":
                value = bool(int(parser["DEFAULT"][key]))
        except KeyError:
            print(f"No key '{key}' in config file! Loaded from DEFAULT_CONFIG")
            value = DEFAULT_CONFIG[key]    

        return value


    if not os.path.exists(CONFIG_FILE):
        print("Config file not found! Loaded DEFAULT_CONFIG")
        config = DEFAULT_CONFIG
        return

    parser = configparser.ConfigParser()
    parser.read(CONFIG_FILE, encoding="utf-8")

    config["max_count"] = load_key(parser, "max_count", "int")
    config["delay"] = load_key(parser, "delay", "int")
    config["window_title"] = load_key(parser, "window_title")
    config["element_title"] = load_key(parser, "element_title")
    config["shift_from_element"] = load_key(parser, "shift_from_element", "int")
    config["debug_print"] = load_key(parser, "debug_print", "bool")


# пока экспериментальный вариант (исправленный относительно winGuiAuto)
# Из однострочного editText вроде извлекает значение нормально, с другими не проверял
def getEditText_fixed(hwnd):
    bufLen = win32gui.SendMessage(hwnd, win32con.WM_GETTEXTLENGTH, 0, 0) + 1
    # print(bufLen)
    buffer = win32gui.PyMakeBuffer(bufLen)
    win32gui.SendMessage(hwnd, win32con.WM_GETTEXT, bufLen, buffer)
    # text = buffer[:bufLen]
    # text = win32gui.PyGetString(buffer.buffer_info()[0], bufLen - 1)
    text = win32gui.PyGetString(win32gui.PyGetBufferAddressAndLen(buffer)[0], bufLen - 1)
    return text


def get_field_value(window_title, element_title, shift_from_element):
    field_value = ""
    result = {
        "value": field_value,
        "error": True
    }
    element_found = False

    # найти окно
    try:
        window = findTopWindow(wantedText=window_title)
        dump = dumpWindow(window)
    except WinGuiAutoError:
        print(f"Window '{window_title}' not found!")
        # result["error"] = True
        return result

    # найти элемент
    for obj in dump:
        debug_print(obj)
        if obj[1] == element_title:
            i = dump.index(obj) + shift_from_element
            # print("element: ", dump[i])
            edit = dump[i]
            try:
                field_value = getEditText_fixed(edit[0])
                # print("field_value: ", field_value)
                element_found = True
                # field_value = int(field_value)
            except ValueError:
                print("Incorrect EditText value!")
                # result["error"] = True
                return result

    if element_found:
        result["error"] = False
        result["value"] = field_value

    return result


def debug_print(msg):
    if config["debug_print"]:
        print(msg)


def main():
    print(f"Program version: {PROGRAM_VERSION}")
    load_config()
    print(f"Current configuration: \n{config}")

    if not os.path.exists(MESSAGE_FILE):
        print("Message file not found!")
        return

    while True:
        time.sleep(config["delay"])

        current_field_value = get_field_value(
            config["window_title"], 
            config["element_title"], 
            config["shift_from_element"]
        )
        if current_field_value["error"]:
           continue
        else:
            try:
                current_value = int(current_field_value["value"])
            except ValueError:
                print("Incorrect EditText value!")
                continue

            if current_value >= config["max_count"]:
                debug_print("stop!")
                os.system(MESSAGE_FILE)


if __name__ == "__main__":
    main()