from funcs import *

DIALOG_HEX = bytes(b'\xFF\xFF\xFF\x7F\xFF\xFF\xFF\x7F\x00\x00\x00\x00\x00\x00\x00\x00\xFD.\xA8\x99')
last_address = int

while True:
    dialog_address = address_scan(DIALOG_HEX)
    dialog_text = read_string(dialog_address)
    if dialog_text is not None and dialog_address != last_address:
            full_dialog = dialog_text #deepl_translate(dialog_text, False, 'enter-deepl-key', 'en')
            for sentence in full_dialog.splitlines():
                print(sentence)
                listen_for_input()
            
            last_address = dialog_address
