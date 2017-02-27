import neopixel
import nativeio
import board
import time
import usb_hid

import adafruit_hid.keyboard as kbd

# Setup keymapping for the CKD63
mapping = bytearray(80)

mapping[1] = kbd.SIX
mapping[2] = kbd.FIVE
mapping[3] = kbd.FOUR
mapping[4] = kbd.THREE
mapping[5] = kbd.TWO
mapping[6] = kbd.ONE
mapping[7] = kbd.ESCAPE
mapping[9] = kbd.DELETE
mapping[10] = kbd.BACKSPACE
mapping[11] = kbd.MINUS
mapping[12] = kbd.ZERO
mapping[13] = kbd.NINE
mapping[14] = kbd.EIGHT
mapping[15] = kbd.SEVEN

mapping[17] = kbd.Y
mapping[18] = kbd.T
mapping[19] = kbd.R
mapping[20] = kbd.E
mapping[21] = kbd.W
mapping[22] = kbd.Q
mapping[23] = kbd.TAB

mapping[25] = kbd.BACKSLASH
mapping[26] = kbd.EQUALS
mapping[27] = kbd.LEFT_BRACKET
mapping[28] = kbd.P
mapping[29] = kbd.O
mapping[30] = kbd.I
mapping[31] = kbd.U

mapping[33] = kbd.H
mapping[34] = kbd.G
mapping[35] = kbd.F
mapping[36] = kbd.D
mapping[37] = kbd.S
mapping[38] = kbd.A

mapping[41] = kbd.RETURN
mapping[42] = kbd.RIGHT_BRACKET
mapping[43] = kbd.QUOTE
mapping[44] = kbd.SEMICOLON
mapping[45] = kbd.L
mapping[46] = kbd.K
mapping[47] = kbd.J

mapping[49] = kbd.B
mapping[50] = kbd.V
mapping[51] = kbd.C
mapping[52] = kbd.X
mapping[53] = kbd.Z

mapping[55] = kbd.LEFT_SHIFT

mapping[57] = kbd.RIGHT_SHIFT
mapping[58] = kbd.UP_ARROW
mapping[59] = kbd.FORWARD_SLASH
mapping[60] = kbd.PERIOD
mapping[61] = kbd.COMMA
mapping[62] = kbd.M
mapping[63] = kbd.N
mapping[66] = kbd.SPACEBAR

mapping[69] = kbd.LEFT_GUI
mapping[70] = kbd.LEFT_ALT
mapping[71] = kbd.LEFT_CONTROL

mapping[73] = kbd.RIGHT_ARROW
mapping[74] = kbd.DOWN_ARROW
mapping[75] = kbd.LEFT_ARROW
mapping[76] = kbd.RIGHT_GUI


pixel = neopixel.NeoPixel(board.A2, 1)
pixel[0] = (0x0, 0x00, 0x0a)
pixel.write()

col_data = nativeio.DigitalInOut(board.D13)
col_data.switch_to_output()

col_clk = nativeio.DigitalInOut(board.D12)
col_clk.switch_to_output()

rows = [nativeio.DigitalInOut(x) for x in [board.D5, board.D6, board.D9, board.D10, board.D11]]

for row in rows:
    row.switch_to_input(pull=nativeio.DigitalInOut.Pull.DOWN)

keyboard = usb_hid.devices[1]
report = bytearray(8)

while True:
    col_data.value = True
    col_clk.value = False
    col_clk.value = True
    col_data.value = False
    total_pressed = 0
    report[0] = 0
    pixel[0] = (0x0, 0x00, 0x0a)
    for col in range(16):
        col_clk.value = False
        col_clk.value = True
        for i, row in enumerate(rows):
            key = i * 16 + col
            if row.value:
                key_code = mapping[key]
                if key_code == 0:
                    print(key)
                elif total_pressed < 6:
                    if key_code >= 0xe0:
                        report[0] |= 1 << (key_code - 0xE0)
                        if key_code == kbd.LEFT_SHIFT:
                            pixel[0] = (0x0, 0x0a, 0x00)
                        elif key_code == kbd.LEFT_CONTROL:
                            pixel[0] = (0x0a, 0x0, 0x0)
                    else:
                        report[2 + total_pressed] = mapping[key]
                        total_pressed += 1
        if total_pressed == 6:
            break
    for i in range(2 + total_pressed, 8):
        report[i] = 0
    keyboard.send_report(report)
    pixel.write()
