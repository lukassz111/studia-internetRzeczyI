from sense_emu import SenseHat
import time

hat = SenseHat()

green = (0, 255, 0)
green_dark = (0, 180, 0)
yellow = (255, 255, 0)
blue = (0, 0, 255)
blue_dark = (0, 0, 180)
red = (255, 0, 0)
red_dark = (180, 0, 0)
white = (255,255,255)
black = (0,0,0)
transparent = (-1,-1,-1)

rotate0 = 0
rotate90 = 1
rotate180 = 2
rotate270 = 3


def image_clear(color):
    c = color
    img = [
        c, c, c, c, c, c, c, c,
        c, c, c, c, c, c, c, c,
        c, c, c, c, c, c, c, c,
        c, c, c, c, c, c, c, c,
        c, c, c, c, c, c, c, c,
        c, c, c, c, c, c, c, c,
        c, c, c, c, c, c, c, c,
        c, c, c, c, c, c, c, c
    ]
    return img

class Image:
    def __init__(self, color):
        self._data = image_clear(color)

    def getData(self):
        return self._data

    def setPixel(self,x,y,color):
        if(color == transparent):
            return
        if(x < 0 or x > 7 or y < 0 or y > 7):
            print("error x or y is out of range")
            raise
        self._data[(y*8)+x] = color

    def getPixel(self,x,y):
        if(x < 0 or x > 7 or y < 0 or y > 7):
            print("error x or y is out of range")
            raise
        return self._data[(y*8)+x]

    def drawPic(self, pic, pic_width, pic_height, offset_x, offset_y):
        for index, pix in enumerate(pic, 0):
            x = index % pic_width
            y = int((index-x) / pic_width)
            color = pix
            self.setPixel(x+offset_x,y+offset_y,color)

    def drawDigit(self,digit = 0,color = black, right = False):
        c = color
        t = transparent
        offset_x = 0
        offset_y = 0
        if(right):
            offset_x = 4
            offset_y = 0
        if digit == 0:
            pic = [
                t, c, c, t,
                c, t, t, c,
                c, t, t, c,
                c, t, t, c,
                c, t, t, c,
                t, c, c, t
            ]
            self.drawPic(pic,4,6,offset_x,offset_y)
        elif digit == 1:
            pic = [
                t, t, t, c,
                t, t, c, c,
                t, c, t, c,
                c, t, t, c,
                t, t, t, c,
                t, t, t, c,
            ]
            self.drawPic(pic,4,6,offset_x,offset_y)
        elif digit == 2:
            pic = [
                c, c, c, c,
                t, t, t, c,
                t, t, c, c,
                c, c, t, t,
                c, t, t, t,
                c, c, c, c,
            ]
            self.drawPic(pic,4,6,offset_x,offset_y)
        elif digit == 3:
            pic = [
                c, c, c, c,
                t, t, t, c,
                t, c, c, c,
                t, c, c, c,
                t, t, t, c,
                c, c, c, c,
            ]
            self.drawPic(pic,4,6,offset_x,offset_y)
        elif digit == 4:
            pic = [
                c, t, t, c,
                c, t, t, c,
                c, c, c, c,
                t, t, t, c,
                t, t, t, c,
                t, t, t, c,
            ]
            self.drawPic(pic,4,6,offset_x,offset_y)
        elif digit == 5:
            pic = [
                c, c, c, c,
                c, t, t, t,
                c, c, t, t,
                t, t, c, c,
                t, t, t, c,
                c, c, c, c,
            ]
            self.drawPic(pic,4,6,offset_x,offset_y)
        elif digit == 6:
            pic = [
                c, c, c, c,
                c, t, t, t,
                c, c, c, c,
                c, t, t, c,
                c, t, t, c,
                c, c, c, c,
            ]
            self.drawPic(pic,4,6,offset_x,offset_y)
        elif digit == 7:
            pic = [
                c, c, c, c,
                t, t, t, c,
                t, t, t, c,
                t, t, c, t,
                t, c, t, t,
                c, t, t, t,
            ]
            self.drawPic(pic,4,6,offset_x,offset_y)
        elif digit == 8:
            pic = [
                c, c, c, c,
                c, t, t, c,
                c, t, c, c,
                c, c, t, c,
                c, t, t, c,
                c, c, c, c,
            ]
            self.drawPic(pic,4,6,offset_x,offset_y)
        elif digit == 9:
            pic = [
                c, c, c, c,
                c, t, t, c,
                c, t, t, c,
                c, c, c, c,
                t, t, t, c,
                c, c, c, c,
            ]
            self.drawPic(pic,4,6,offset_x,offset_y)
        elif digit > 9:
            pic = [
                c, t, t, t,
                t, c, t, t,
                t, t, c, t,
                t, t, c, t,
                t, c, t, t,
                c, t, t, t,
            ]
            self.drawPic(pic,4,6,offset_x,offset_y)


switchMode = 0
temperatureMode = 1
humidityMode = 2
mode = switchMode
modeLetters = ['S','T','H']
newMode = temperatureMode
rotate = rotate0

printEnabled = False
def printMode():
    if not printEnabled:
        return
    if(mode == switchMode):
        print("mode: switch")
    elif(mode == temperatureMode):
        print("mode: temperature")
    elif(mode == humidityMode):
        print("mode: humidity")
    else:
        print("mode: wtf!")

def printEvent(event):
    if not printEnabled:
        return
    print("event: "+str(event.action)+" "+str(event.direction))

#  0  1  2  3  4  5  6  7
#  8  9 10 11 12 13 14 15
# 16 17 18 19 20 21 22 23
# 24 25 26 27 28 29 30 31
# 32 33 34 35 36 37 38 39
# 40 41 42 43 44 45 46 47
# 48 49 50 51 52 53 54 55
# 56 57 58 59 60 61 62 63
# Po obróceniu o 90 stopni
#  7 15 23 31 39 47 55 63
#  6 14 22 30 38 46 54 62

def applyRotate(rot = rotate0):
    if rot == rotate0:
        return
    elif rot == rotate90:
        pix = hat.get_pixels()
        newPix = []
        for x in range(7,-1,-1):
            for y in range(0,8,1):
                newPix.append(pix[(y * 8) + x])
        hat.set_pixels(newPix)
        return
    else:
        pix = hat.get_pixels()
        newPix = []
        for x in range(7,-1,-1):
            for y in range(0,8,1):
                newPix.append(pix[(y * 8) + x])
        hat.set_pixels(newPix)
        return applyRotate(rot-1)

while True:

    events = hat.stick.get_events()
    for event in events:
        if event.action == "released":
            printEvent(event)
            if event.direction == "right":
                newMode += 1
                if(newMode > 2):
                    newMode = 1
            elif event.direction == "middle":
                if(mode != switchMode):
                    newMode = mode
                    mode = switchMode
                else:
                    mode = newMode


    rotate = rotate0
    hat.set_imu_config(compass_enabled=False,gyro_enabled=False,accel_enabled=True)
    a = hat.get_accelerometer_raw()
    x = a['x']
    y = a['y']
    z = a['z']
    if abs(x) < 0.1:
        x = 0
    if abs(y) < 0.1:
        y = 0
    if abs(z) < 0.1:
        z = 0
    if x < -0.9:
        x = -1
    if y < -0.9:
        y = -1
    if z < -0.9:
        z = -1
    if x > 0.9:
        x = 1
    if y > 0.9:
        y = 1
    if z > 0.9:
        z = 1
    print(str(x)+" "+str(y)+" "+str(z))
    printMode()

    # Tryb do przełączania trybów
    if(mode == switchMode):
        img = Image(black)
        hat.set_pixels(img.getData())
        hat.show_letter(modeLetters[newMode],back_colour=red)
        applyRotate(rot=rotate)
    # Temperatura - wyświetla 2 cyfry na czerwono lub niebiesko
    # zależnie od tego czy temperatura jest ujemna lub dodatnia.
    # Jeśli wartość absolutna temperatury jest przynajmniej równa 100
    # to zamiast jednej liczby jest wyświetlany znak większości
    elif(mode == temperatureMode):
        digit_a_color = black
        digit_b_color = black
        t = int(hat.get_temperature())
        if t < 0:
            digit_a_color = blue
            digit_b_color = blue_dark
        else:
            digit_a_color = red
            digit_b_color = red_dark
        abst = abs(t)
        digit_b = int(abst % 10)
        digit_a = int((abst - digit_b)/10)
        img = Image(white)
        img.drawDigit(digit_a,digit_a_color)
        img.drawDigit(digit_b,digit_b_color,True)
        hat.set_pixels(img.getData())
        applyRotate(rot=rotate)
    elif(mode == humidityMode):
        t = int(hat.get_humidity())
        abst = abs(t)
        digit_b = int(abst % 10)
        digit_a = int((abst - digit_b)/10)
        img = Image(white)
        img.drawDigit(digit_a,green)
        img.drawDigit(digit_b,green_dark,True)
        hat.set_pixels(img.getData())
        applyRotate(rot=rotate)

    time.sleep(.75)
