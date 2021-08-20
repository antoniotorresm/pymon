import json
import pymem
import re
import requests
import XInput as xinput
import keyboard

PROC_NAME = 'DQXGame.exe'

def instantiate(exe):
    '''Instantiates a pymem instance that attaches to an executable.'''
    global PY_MEM  # pylint: disable=global-variable-undefined
    global HANDLE  # pylint: disable=global-variable-undefined

    try:
        PY_MEM = pymem.Pymem(exe)
        HANDLE = PY_MEM.process_handle
    except pymem.exception.ProcessNotFound:
        print('''Cannot find DQX. Ensure the game is launched and try
                again.\nIf you launched DQX as admin, this program must'
                also run as admin.\n\nPress ENTER or close this window.''')

def detect_controller():
    ''''''
    connected = list(xinput.get_connected())
    try:
        if connected.index(True) in (0, 1, 2, 3):
            return True
        return False
    except:
        return False

def listen_for_input():
    '''
    Listens for controller input. Function exits when
    a supported button is pressed.
    '''
    
    acceptable_buttons = [
        'A',
        'B',
        'X',
        'Y',
        'DPAD_LEFT',
        'DPAD_RIGHT',
        'DPAD_UP',
        'DPAD_DOWN'
    ]
    
    # to be implemented
    acceptable_keys = [
        'enter',
        'escape',
        'up',
        'down',
        'left',
        'right'
    ]

    if detect_controller():
        print('Listening for controller input..')
        while True:
            events = xinput.get_events()
            for event in events:
                if ((event.type == xinput.EVENT_BUTTON_RELEASED)
                and (event.button in acceptable_buttons)):
                    return False
            while True:
                events = xinput.get_events()
                for event in events:
                    if ((event.type == xinput.EVENT_BUTTON_PRESSED)
                    and (event.button in acceptable_buttons)):
                        print('pressed')
                        return False
    else:
        print('Listening for keyboard input..')
        while True:
            if keyboard.is_pressed('enter'):
                while True:
                    if keyboard.is_pressed('enter') == False:
                        break
                break
        
def address_scan(pattern: bytes, *, start_address = 0, end_address = 0x7FFFFFFF):
    '''
    Scans the entire virtual memory space and returns the address
    that match the given byte pattern.
    '''
    instantiate('DQXGame.exe')
    
    next_region = start_address
    while next_region < end_address:
        next_region, found = pymem.pattern.scan_pattern_page(HANDLE, next_region, pattern)
        if found:
            base_address = found + 36
            return PY_MEM.read_int(base_address)

def read_string(address):
    ''''''
    instantiate(PROC_NAME)
    
    end_addr = address
    
    if end_addr is not None:
        while True:
            result = PY_MEM.read_bytes(end_addr, 1)
            end_addr = end_addr + 1
            if result == b'\x00':
                bytes_to_read = end_addr - address
                break
        
        return sanitize_text(PY_MEM.read_string(address, bytes_to_read))

def sanitize_text(dialog_text):
    ''''''
    text = re.sub('\n', '', dialog_text)
    text = re.sub('<br>', '\n', text)
    text = re.sub('(<.+?>)', '', text)
    text = re.sub('「', '', text)
    text = re.sub('　', '', text)
    
    return text

def deepl_translate(dialog_text, is_pro, api_key, region_code):
    ''''''
    if is_pro:
        api_url = 'https://api.deepl.com/v2/translate'
    else:
        api_url = 'https://api-free.deepl.com/v2/translate'
    
    payload = {'auth_key': api_key, 'text': dialog_text, 'target_lang': region_code}
    r = requests.post(api_url, data=payload)
    translated_text = r.content
    
    return json.loads(translated_text)['translations'][0]['text']
    
def google_translate(dialog_text, api_key, region_code):
    ''''''
    uri = '&source=ja&target=' + region_code + '&q=' + dialog_text
    api_url = 'https://www.googleapis.com/language/translate/v2?key=' + api_key + uri
    headers = {'Content-Type': 'application/json'}
    
    r = requests.post(api_url, headers=headers)
    translated_text = r.content
    
    return json.loads(translated_text)['data']['translations'][0]['translatedText']
