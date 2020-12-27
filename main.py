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
        self.data = image_clear(color)

    def setPixel(self,x,y,color):
        if(color == transparent):
            return
        if(x < 0 or x > 7 or y < 0 or y > 7):
            print("error x or y is out of range")
            raise
        self.data[(y*8)+x] = color

    def getPixel(self,x,y):
        if(x < 0 or x > 7 or y < 0 or y > 7):
            print("error x or y is out of range")
            raise
        return self.data[(y*8)+x]

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
def printMode():
    if(mode == switchMode):
        print("mode: switch")
    elif(mode == temperatureMode):
        print("mode: temperature")
    elif(mode == humidityMode):
        print("mode: humidity")
    else:
        print("mode: wtf!")

def printEvent(event):
    print("event: "+str(event.action)+" "+str(event.direction))

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


    printMode()

    # Tryb do przełączania trybów
    if(mode == switchMode):
        img = Image(black)
        hat.set_pixels(img.data)
        hat.show_letter(modeLetters[newMode],back_colour=red)
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
        hat.set_pixels(img.data)
    elif(mode == humidityMode):
        t = int(hat.get_humidity())
        abst = abs(t)
        digit_b = int(abst % 10)
        digit_a = int((abst - digit_b)/10)
        img = Image(white)
        img.drawDigit(digit_a,green)
        img.drawDigit(digit_b,green_dark,True)
        hat.set_pixels(img.data)

    time.sleep(.75)
