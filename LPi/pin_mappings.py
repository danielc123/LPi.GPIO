# -*- coding: utf-8 -*-
# Copyright (c) 2017 Richard Hull
# See LICENSE.md for details.

import functools
from OPi.constants import BOARD, BCM, SUNXI


class _sunXi(object):

    def __getitem__(self, value):

        offset = ord(value[1]) - 65
        pin = int(value[2:])

        assert value[0] == "P"
        assert 0 <= offset <= 25
        assert 0 <= pin <= 31

        return (offset * 32) + pin


_pin_map = {
    # Physical pin to actual GPIO pin
    BOARD: {
        1: 129,                     #PE1/CSI_MCLK/LCD_DE
        2: 149,     #PE21/CSI_SCK/TWI1_SCK/UART1_TX
        3: 128,                     #PE0/CSI_PCLK/LCD_CLK
        4: 150,     #PE22/CSI_SDA/TWI1_SDA/UART1_RX
#MCSI   5: -,                       #MCSI_MCLK
        6: 32,      #PB0/UART2_TX/PB_EINT0
        7: 34,                      #PB2/UART2 RST/PB_EINT2
        8: 33,      #PB1/UART2_RX/PB_EINT1
        9: 35,                      #PB3/UART2_CTS/PB_EINT3
        10: 36,     #PB4/PWM0/PB_EINT4 --> LCD BACKLIGHT PWM CONTROL
#PW     11: -,                      #1V2
        12: 37,     #PB5/PWM1/PB_EINT5
#PW     13: -,                      #1V8
        14: 38,     #PB6/TWI0_SCK/PB_EINT6 -->I2C TOUCH CONTROL
#PW     15: -,                      #3V3
        16: 39,     #PB7/TWI0_SDA/PB_EINT7 --> I2C TOUCH CONTROL
#MCSI   17: -,                      #MCSI_D0P
        18: 40,     #PB8/TWI1_SCK /UART0_TX /PB_EINT8
#MCSI   19: -,                      #MCSI_D0N
        20: 41,     #PB9/TWI1_SDA/UART0_RX/PB_EINT9
#MCSI   21: -,                      #MCSI_D1P
        22: 65,     #PC1/SDC2_CMD/SPI_CLK
#MCSI   23: -,                      #MCSI_D1N
        24: 67,     #PC3/SDC2_D0/SPI_MOSI
#MCSI   25: -,                      #MCSI_CKP
        26: 64,     #PC0/SDC2_CLK/SPI_MISO
#MCSI   27: -,                      #MCSI_CKN
        28: 66      #PC2/SDC2_RST/SPI_CS
#PW     29: -,                      #GND
#PW     30: -,      #5V
#SD     31: 165,    #PF5/SDC0_D2/JTAG_CK1
#PW     32: -,                      #3V0
#SD     33: 164,    #PF4/SDC0_D3/UART0_RX
#ETH    34: -,                      #ETH_RXN
#SD     35: 163,    #PF3/SDC0_CMD/JTAG_DO1
#ETH    36: -,                      #ETH_RXP
#SD     37: 162,    #PF2/SDC0_CLK/UART0_TX
#ETH    38: -,                      #ETH_TXN
#SD     39: 161,    #PF1/SDC0_D0/JTAG_DI1
#ETH    40: -,                      #ETH_TXP
#SD     41: 160,    #PF0/SDC0_D1/JTAG_MS1
#USB    42: -,                      #USB_ID
#AU     43: -,      #KEYADC0
#USB    44: -,                      #USB_N
#P      45: -,      #3V3
#USB    46: -,                      #USB_P
#P      47: -,      #GND
#AU     48: -,                      #MIC_P
#WIFI   49: 197,    #PG5/SDC1_D3/PG_EINT5
#AU     50: -,                      #MIC_N
#WIFI   51: 196,    #PG4/SDC1_D2/PG_EINT4
#AU     52: -,                      #HBIAS
#WIFI   53: 195,    #PG3/SDC1_D1/PG_EINT3
#AU     54: -,                      #HP_R
#WIFI   55: 194,    #PG2/SDC1_D0/PG_EINT2 --> LED RED
#AU     56: -,                      #HP_L
#WIFI   57: 193,    #PG1/SDC1_CMD/PG_EINT1 --> LED GREEN
#AU     58: -,                      #HP_COMFB
#WIFI   59: 192,    #PG0/SDC1_CLK/PG_EINT0 --> LED BLUE
#AU     60: -,                      #HP_COM
    },

    # BCM pin to actual GPIO pin
    BCM: {
#        2: 12,
#        3: 11,
#        4: 6,
#        7: 10,
#        8: 13,
#        9: 16,
#        10: 15,
#        11: 14,
#        14: 198,
#        15: 199,
#        17: 1,
#        18: 7,
#        22: 3,
#        23: 19,
#        24: 18,
#        25: 2,
#        27: 0,
        1: 129,
        2: 149,
        3: 128,
		4: 150,
        6: 32,
        7: 34,
        8: 33,
        9: 35,
		10: 36,
        12: 37,
		14: 38,
		16: 39,
        18: 40,
        20: 41,
        22: 65,
        24: 67,
        26: 64,
        28: 66,        
#SD		31: 165,
#SD		33: 164,
#SD		35: 163,
#SD		37: 162,
#SD		39: 161,
#SD		41: 160,
#WIFI_DOCK   49: 197,
#WIFI_DOCK   51: 196,
#WIFI_DOCK   53: 195,
#WIFI_DOCK   55: 194,
#WIFI_DOCK   57: 193,
#WIFI_DOCK   59: 192,	
    },

    # LICHEE 30 CON LEFT
#    LICHEE: {
#LCD    1: 129,                     #LCD_DE / PE1 / CSI_MCLK
#       2: 149,     #UART1_TX / PE21 / CSI_SCK / TWI1_SCK
#LCD    3: 128,                     #LCD CLK / PE0 / CSI_PCLK
#       4: 150,     #UART1_RX  / PE22 / CSI_SDA / TWI1_SDA
#MCSI   5: -,                       #MCSI_MCLK
#       6: 32,      #UART2_TX / PB0 / PB_EINT0
#       7: 34,                      #UART2 RST / PB2 / PB_EINT2
#       8: 33,      #UART2_RX / PB1 /PB_EINT1
#       9: 35,                      #UART2 CTS / PB3 / PB_EINT3
#LCD    10: 36,     #PWM0 / PB4 / PB_EINT4
#PW     11: -,                      #1V2
#       12: 37,     #PWM1 / PB5 / PB_EINT5
#PW     13: -,                      #1V8
#       14: 38,     #TWI0_SCK / PB6 / PB_EINT6
#PW     15: -,                      #3V3
#       16: 39,     #TWI0_SDA / PB7 / PB_EINT7
#MCSI   17: -,                      #MCSI_D0P
#       18: 40,      #TWI1_SCK / PB8 / UART0_TX / PB_EINT8
#MCSI   19: -,                      #MCSI_D0N
#       20: 41,     #TWI1_SDA / PB9 / UART0_RX / PB_EINT9
#MCSI   21: -,                      #MCSI_D1P
#       22: 65,     #SPI_CLK / PC1 / SDC2_CMD
#MCSI   23: -,                      #MCSI_D1N
#       24: 67,     #SPI_MOSI / PC3 / SDC2_D0
#MCSI   25: -,                      #MCSI_CKP
#       26: 64,     #SPI_MISO / PC0 / SDC2_CLK
#MCSI   27: -,                      #MCSI_CKN
#       28: 66       #SPI_CS / PC2 / SDC2_RST
#PW     29: -,                      #GND
#PW     30: -,      #5V
#AU     31: -,                      #HP_COM
#WIFI   32: 192,    #SDC1_CLK / PG0 / PG_EINT0 / LED BLUE
#AU     33: -,                      #HP COMFB
#WIFI   34: 193,    #SDC1_CMD / PG1 / PG_EINT1 / LED GREEN
#AU     35: -,                      #HP_L
#WIFI   36: 194,    #SDC1_D0 / PG2 / PG_EINT2 / LED RED
#AU     37: -,                      #HP_R
#WIFI   38: 195,    #SDC1_D1 / PG3 / PG_EINT3
#AU     39: -,                      #HBIAS
#WIFI   40: 196,    #SDC1_D2 / PG4 / PG_EINT4
#AU     41: -,                      #MIC_N
#WIFI   42: 197,    #SDC1_D3 / PG5 / PG_EINT5
#AU     43: -,                      #MIC_P
#P      44: -,      #GND
#USB    45: -,                      #USB_P
#P      46: -,      #3V3
#USB    47: -,                      #USB_N
#AU     48: -,      #KEYADC0
#USB    49: -,                      #USB_ID
#SD     50: 160,    #SDC0_D1 / PF0 / JTAG_MS1
#ETH    51: -,                      #ETH_TXP
#SD     52: 161,    #SDC0_D0 / PF1 / JTAG_DI1
#ETH    53: -,                      #ETH_TXN
#SD     54: 162,    #SDC0_CLK / PF2 / UART0_TX
#ETH    55: -,                      #ETH_RXP
#SD     56: 163,    #SDC0_CMD / PF3 / JTAG_DO1
#ETH    57: -,                      #ETH_RXN
#SD     58: 164,    #SDC0_D3 / PF4 / UART0_RX
#P      59: -,                      #3V0
#SD     60: 165     #SDC0_D2 / PF5 / JTAG_CK1
#    },

    
    SUNXI: _sunXi()
}


def get_gpio_pin(mode, channel):
    assert mode in [BOARD, BCM, SUNXI]
    return _pin_map[mode][channel]


bcm = functools.partial(get_gpio_pin, BCM)
board = functools.partial(get_gpio_pin, BOARD)
sunxi = functools.partial(get_gpio_pin, SUNXI)
