#!/usr/bin/env python
import ctypes
import os
import PySimpleGUI as sg

def make_main_menu():
    general_layout = [
        [sg.Checkbox('Enable logging to file?', sg.user_settings_get_entry('enable_logging', False), key='enable_logging')],
        [sg.Checkbox('Do you play with a controller?', sg.user_settings_get_entry('enable_controller', True), key='enable_controller')],
        [sg.Text('Target Language:'), sg.Combo(['bg', 'cs', 'da', 'el', 'en', 'es', 'et', 'fi', 'fr', 'hu', 'it', 'lt', 'lv', 'nl', 'pl', 'pt', 'ro', 'ru', 'sk', 'sl', 'sv', 'zh'], sg.user_settings_get_entry('target_language', 'en'), key='target_language')]
    ]

    api_layout = [
        [sg.Text('Only configure one or the other.')],
        [sg.Checkbox('Use DeepL APIs', sg.user_settings_get_entry('enable_deepl', False), change_submits=True, enable_events=True, key='enable_deepl')]
    ]

    dialog_layout = [
        [sg.Checkbox('Automatically hide dialog overlay?', default=False, key='enable_dialog_hide')],
        [sg.Text('Transparency:', pad=(None, (18,0))), sg.Slider(range=(1,100), orientation='h', size=(25,20), default_value=sg.user_settings_get_entry('dialog_transparency_value', 100), enable_events=True, key='dialog_transparency_value')],
        [sg.Text('Font Size:', pad=(None, (0,0))), sg.Combo([12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32], default_value=sg.user_settings_get_entry('dialog_font_size_value', 16), size=(29,1), enable_events=True, key='dialog_font_size_value')],
        [sg.Text('Font Color:', pad=(None, (0,0))), sg.Combo(['White', 'Yellow', 'Red', 'Green', 'Blue', 'Black', 'Gray', 'Maroon', 'Purple', 'Fuschia', 'Lime', 'Olive', 'Navy', 'Teal', 'Aqua'], default_value=sg.user_settings_get_entry('dialog_font_color_value', 'White'), size=(29,1), enable_events=True, key='dialog_font_color_value')],
        [sg.Text('Font Name:', pad=(None, (0,0))), sg.Combo(os.listdir(r'C:\Windows\fonts'), default_value=sg.user_settings_get_entry('dialog_font_name_value', 'Arial'), enable_events=True, key='dialog_font_name_value')]
    ]

    quest_layout = [
        
    ]

    about_layout = [
        
    ]

    layout = [
        [sg.TabGroup([[sg.Tab('General', general_layout, key='generalTabKey'),
                        sg.Tab('API Config', api_layout, key='apiTabKey'),
                        sg.Tab('Dialog Overlay', dialog_layout, key='dialogTabKey'),
                        sg.Tab('Quest Overlay', quest_layout, key='questTabKey'),
                        sg.Tab('About', about_layout, key='aboutTabKey')
                    ]], tab_location='left'),
        [sg.Button('Run pymon')]
        ]
    ]

    return sg.Window('pymon', layout, default_element_size=(60, 1), keep_on_top=True, finalize=True)

def make_dialog_overlay():
    layout = [
        [sg.Text('this is a test')]
    ]

    return sg.Window('a', layout, no_titlebar=True, grab_anywhere=True, alpha_channel=.9, keep_on_top=True, size=(600,200), resizable=True)

def save_user_settings(values):
    sg.user_settings_set_entry('enable_logging', values['enable_logging'])
    sg.user_settings_set_entry('enable_controller', values['enable_controller'])
    sg.user_settings_set_entry('target_language', values['target_language'])
    sg.user_settings_set_entry('enable_deepl', values['enable_deepl'])
    sg.user_settings_set_entry('dialog_transparency_value', values['dialog_transparency_value'])
    sg.user_settings_set_entry('dialog_font_size_value', values['dialog_font_size_value'])
    sg.user_settings_set_entry('dialog_font_color_value', values['dialog_font_color_value'])
    sg.user_settings_set_entry('dialog_font_name_value', values['dialog_font_name_value'])

def show_main_menu():
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
    sg.user_settings_filename(filename='settings.json', path='.')
    make_main_menu()
    while True:
        window, event, values = sg.read_all_windows()

        if event == sg.WIN_CLOSED or event == 'Exit':
            save_user_settings(values)
            break
        elif event == 'Run pymon':
            break
        else:
            print(f'Event: {event}')
            print(f'Values: {values}')

def show_dialog_overlay():
    make_dialog_overlay()
    while True:
        window, event, values = sg.read_all_windows()

        if event == sg.WIN_CLOSED or event == 'Exit':
            print('[LOG] User exited.')
            break
        else:
            print(f'Event: {event}')
            print(f'Values: {values}')

if __name__ == '__main__':
    show_main_menu()
    show_dialog_overlay()