import board
# Matrix
import digitalio  # Also for speaker
import time
import adafruit_matrixkeypad
from math import log, sin
# LCD i2c
import busio
import lcd
import i2c_pcf8574_interface
# Parlante
import audiomp3
import audiopwmio
import keypad
from time import sleep

# DIP Switch
has_speaker = False
has_lcd = False

pins = []

for pin in (board.GP16, board.GP17, board.GP18, board.GP19, board.GP20, board.GP21):
    switch = digitalio.DigitalInOut(pin)
    switch.direction = digitalio.Direction.INPUT
    switch.pull = digitalio.Pull.UP
    pins.append(switch)

for pin in range(0, len(pins)):
    curr_pin = pins[pin]

    if not curr_pin.value:
        print(pin)
        if pin == 0:
            has_lcd = True
            print("Hay LCD")
        elif pin == 1:
            has_speaker = True
            print("Hay Speaker")

'''
# Speaker
audio = audiopwmio.PWMAudioOut(board.GP14)

# LCD I2C
i2c = busio.I2C(scl=board.GP1, sda=board.GP0)
address = 0x27

i2c = i2c_pcf8574_interface.I2CPCF8574Interface(i2c, address)
display = lcd.LCD(i2c, num_rows=2, num_cols=16)

display.set_backlight(True)
display.set_display_enabled(True)

display.clear()
'''
'''
col_pins = [board.GP10, board.GP11, board.GP12, board.GP13]
cols = []
for col in col_pins:
    switch = digitalio.DigitalInOut(col)
    switch.direction = digitalio.Direction.INPUT
    switch.pull = digitalio.Pull.UP
    cols.append(switch)
    
row_pins = [board.GP9, board.GP8, board.GP7, board.GP4, board.GP5, board.GP6]
rows = []
for row in row_pins:
    switch = digitalio.DigitalInOut(row)
    switch.direction = digitalio.Direction.INPUT
    switch.pull = digitalio.Pull.UP
    rows.append(switch)
'''
# Matriz
cols = [digitalio.DigitalInOut(x) for x in (board.GP10, board.GP11, board.GP12, board.GP13)]
rows = [digitalio.DigitalInOut(x) for x in (board.GP9, board.GP8, board.GP7, board.GP4, board.GP5, board.GP6)]
    #board.GP9, board.GP8, board.GP7, board.GP4, board.GP5, board.GP6)]


keys = (('Ñ', 'Ñ', 'Ñ', 'Ñ'),
        ('1', '2', 'ans', '+'),
        ('log(', 'sin(', '.', '-'),
        ('C1', 'Clear', 'Ñ', '*'),
        ('Ñ', 'Ñ', 'Ñ', 'Ñ'),
        ('(', ')', '#', '/'))
'''

keys = (('0', '1', '2', '3'),
        ('4', '5', '6', '7'),
        ('8', '9', 'A', 'B'),
        ('C', 'D', 'E', 'F'),
        ('G', 'H', 'I', 'J'),
        ('K', 'L', 'M', 'N'))
'''

print(f"lol: {len(keys)}")

keypad = adafruit_matrixkeypad.Matrix_Keypad(rows, cols, keys)

class Calculadora():
    def __init__(self, stackOper, stackPar, elements, results, last_pars, was_answer, last_result, isOper, ans, was_error):
        self.stackOper = stackOper
        self.stackPar = stackPar
        self.elements = elements
        self.results = results
        self.last_pars = last_pars
        self.was_answer = was_answer
        self.last_result = last_result
        self.isOper = isOper
        self.ans = ans
        self.was_error = was_error

    def calcular(self, key_press):
        print(f"was_error: {self.was_error}")
            
        if key_press == '(':
            self.stackPar.append('(')

        if key_press == ')' and len(self.stackPar) > 0:
            self.isOper = True
            self.stackPar.pop()
        
        if len(self.stackOper) > 0 and key_press in symbols:
            print("")
            if len(self.stackPar) < 1:
                print(f"lol: {stackOper}; god: {stackPar}")
                # isOper = True
                self.results+=')'*len(self.stackOper)
                #texto +=')'*len(self.stackOper)
                self.last_pars = len(self.stackOper)
                for j in range(len(stackOper)):
                    self.stackOper.pop()
                    
        if key_press in oper:
            self.stackOper.append('(')
            self.results+=key_press
            self.isOper = True
            self.elements.append(key_press)
                    
        elif key_press == 'ans':
            self.results+=self.ans
                        
        elif key_press == 'Clear':
            self.results = ''
            self.was_error = False
            self.stackPar.clear()
            self.stackOper.clear()
                        
        elif key_press == 'C1':
            if not self.was_answer:
                if self.results == '':
                    pass
                elif len(self.elements) > 0:
                    #print(f"Els: {elements}")
                    replaced = self.elements[len(self.elements)-1]
                    print(replaced)
                    if replaced in oper and len(self.stackOper) > 0: #podría crear un bool "isOper" para ahorrarme ésta iteración
                        self.stackOper.pop()                        
                    elif self.results[len(self.results)-1] == ')':
                        replaced+=')'*self.last_pars
                        
                    elif replaced == '(' and len(self.stackPar) > 0:
                        self.stackPar.pop()
                                    
                    new_res=self.results.rsplit(replaced, 1)
                        
                    print(f"new: {new_res}")
                    self.results = ''.join(new_res)
                    self.elements.pop()

        elif keys[0] == '#':
            print("God")
            try:
                print(f"ehh: {self.results}")
                self.result = eval(self.results)
                self.results=str(self.result)
                self.ans=self.results
                    
                self.was_answer = True
                    
                #time.sleep(.5)
                    
            except:
                print(self.results)
                print("Algo hiciste mal, locura")
                self.results = 'Ta mal, bobo'
                respuesta = ''
                
                self.was_error = True
        else:
            if not self.was_error:
                self.last_result = self.results
                self.results+=key_press
                self.elements.append(key_press)
            
        last_key = key_press
            
        if not last_key == '#' or not key_press == '#':
            self.was_answer = False
                

        print(f"Respuesta: {self.results}")
        return [self.results, self.last_result, self.was_answer, self.ans, self.was_error]

#todo el coso, ans, is_result
def lcd(operacion, resultado, key_press, is_answer, is_error):
    print(key_press)
    if is_error and key_press == 'Clear':
        display.clear()
    elif is_answer or key_press == 'Clear':
        display.clear()
    elif key_press == 'C1':
        display.clear()
        
    if resultado == 'Syntax Error':
        display.clear()
        display.print("Syntax Error")

    #Falta el 'Syntax Error', el ** y**(1/, el ')'*len(stackOper) y probar el C1

    excesoOper = len(operacion) - 15
    excesResult = len(resultado) - 13
    # print(excesResult)

    if excesoOper > 0:
        operacion = operacion[excesoOper:]

        display.set_cursor_pos(1, 0)
        display.print('<-')

        display.set_cursor_pos(1, 15-len(operacion[excesoOper:]))

    if excesResult > 0:
        display.set_cursor_pos(1, 15-len(operacion[excesResult:]))
        display.print("Coso")
    else:
        display.set_cursor_pos(1, 15-len(resultado))
        display.print(f'{resultado}')    

    display.set_cursor_pos(0, 0)
    display.print(f'{operacion}')

def parlante(is_answer, is_error, key_press, results=''):
    decoder = ''
    
    if is_answer or is_error:
        if results == 'Ta mal, bobo':
            decoder = audiomp3.MP3Decoder(open("/audios/Syntax Error.mp3", "rb"))
            audio.play(decoder)
        else: 
            i = 0
            decoder = audiomp3.MP3Decoder(open(f"/audios/igual.mp3", "rb"))
            audio.play(decoder)
                
            time.sleep(.5)
            

            #for num in results:
            while i < len(results):
                if results[i] == '/':
                    decoder = audiomp3.MP3Decoder(open("/audios/div.mp3", "rb"))
                elif results[i] == '.':
                    decoder = audiomp3.MP3Decoder(open("/audios/coma.mp3", "rb"))
                elif results[i] == '*':
                    decoder = audiomp3.MP3Decoder(open("/audios/por.mp3", "rb"))
                else:
                    decoder = audiomp3.MP3Decoder(open(f"/Audios/{results[i]}.mp3", "rb"))
                audio.play(decoder)
                        
                i+=1
                while audio.playing:
                    keys3 = keypad.pressed_keys
                            
                    if keys3:
                        #El clear te deja seguir escribiendo? O se va a quedar acá?
                        if keys3[0] == 'Clear':
                            audio.stop()
                            i=len(results)

    else:
        print(f"lol: {key_press}")
        if key_press == '/':
            decoder = audiomp3.MP3Decoder(open("/audios/div.mp3", "rb"))
        elif key_press == '.':
            decoder = audiomp3.MP3Decoder(open("/audios/coma.mp3", "rb"))
        elif key_press == '*':
            decoder = audiomp3.MP3Decoder(open("/audios/por.mp3", "rb"))
        else:
            decoder = audiomp3.MP3Decoder(open(f"/audios/{key_press}.mp3", "rb"))
            
        audio.play(decoder)

respuestas_calculos = []

texto = ''
was_answer = False
isOper = False
last_state = False
last_pars = 0
last_result = ''
ans = ''
was_error = False

results = ''

stackOper = []
stackPar = []

symbols = ['+', '-', '*', '/', ')', '#']
oper = ['sin(', 'cos(', 'tan(', 'log(', '**(1/']

elements = []

calculadora = Calculadora(stackOper,stackPar,elements,results,last_pars,was_answer,last_result, isOper, ans, was_error)

while True:
    keys = keypad.pressed_keys
    if keys and not last_state == keys:
        calculos = calculadora.calcular(keys[0])
        print(calculos[0])

        if has_lcd:
            lcd(calculos[0], calculos[3], keys[0], calculos[2], calculos[4])

        #El problema con esto es que siempre va a tener el speaker si el usuario lo compró así, entonces medio que tengo un if al pedo
        #if has_speaker:
        if has_speaker:
            parlante(calculos[2], calculos[4], keys[0], calculos[0])
    
    last_state = keys
    #parlante(calculos[2], keys[0], calculos[0])
