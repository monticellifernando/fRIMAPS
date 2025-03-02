class PrintLogLevel:
    FATAL    = 0
    ERROR    = 1
    WARNING  = 2
    INFOLCD  = 3
    INFO     = 4
    DEBUG    = 5
    DEBUGLCD = 6
    VERBOSE  = 7



class Print:
    Name=''
    LogLevel = PrintLogLevel.INFO
    lcd = None
    prefix = { # prefix printed according to LogLevel
            0:'FATAL: ',     # Print info both on serial annd LCD
            1:'ERROR: ',     # Print info both on serial annd LCD
            2:'WARNING: ',     # Print WARNING on serial
            3:'INFOLCD: ',     # Print info both on serial annd LCD
            4:'INFO: ',     # Print info  on serial
            5:'DEBUG: ',    # Print DEBUG only on serial
            6:'DEBUGLCD: ',    # Print DEBUG only on serial
            7:'VERBOSE: ',    # Print VERBOSE only on serial
            }

    color = {
             PrintLogLevel.FATAL : '\033[95m',
             PrintLogLevel.ERROR : '\033[91m',
             PrintLogLevel.WARNING : '\033[93m',
             PrintLogLevel.INFOLCD : '\033[92m',
             PrintLogLevel.INFO : '\033[92m',
             PrintLogLevel.DEBUG : '\033[96m',
             PrintLogLevel.DEBUGLCD : '\033[96m',
             PrintLogLevel.VERBOSE : '\033[94m',
            }
             #PrintLogLevel.HEADER : '\033[95m',
             #PrintLogLevel.ENDC : '\033[0m',
             #PrintLogLevel.BOLD : '\033[1m',
             #PrintLogLevel.UNDERLINE : '\033[4m',




    def __init__(self, Level = PrintLogLevel.INFO, lcd = None):
        self.SetLogLevel(Level)
        self.SetLCD(lcd)

    def SetLCD(self, lcd):
        print(f'{self.Name} Print:: setting LCD object...')
        self.lcd = lcd

    def SetLogLevel(self, LogLevel):
        print(f'{self.Name} Print:: setting LogLevel to {LogLevel}' )
        self.LogLevel = LogLevel


    def Print(self, Str1='', Str2='', LogLevel = PrintLogLevel.INFO, ShowInDisplay = True, end='\n' ):
        # ShowInDisplay is evaluated for Debug status. If not DEBUG will ALWAYS show in display
        if LogLevel > self.LogLevel:
            return

        try:

            print(f'{self.color[LogLevel]}{self.Name} {self.prefix[LogLevel]} {Str1}\033[0m', end = end)
            if self.lcd and ShowInDisplay:
                self.lcd.clear()
                self.lcd.putstr(Str1)
            if Str2 != '' :
                print(f'{self.color[LogLevel]}{self.Name} {self.prefix[LogLevel]} {Str2}\033[0m')
                if self.lcd and ShowInDisplay:
                    self.lcd.move_to(0, 1)
                    self.lcd.putstr(Str2)
        except Exception as e:
            self.ERROR('ERROR')
            print(e)

    def FATAL(self, Str1='', Str2=''):
        self.Print( Str1=Str1, Str2=Str2, LogLevel = PrintLogLevel.FATAL, ShowInDisplay = True)

    def ERROR(self, Str1='', Str2=''):
        self.Print( Str1=Str1, Str2=Str2, LogLevel = PrintLogLevel.ERROR, ShowInDisplay = True)

    def WARNING(self, Str1='', Str2=''):
        self.Print( Str1=Str1, Str2=Str2, LogLevel = PrintLogLevel.WARNING, ShowInDisplay = False)

    def INFO(self, Str1='', Str2='', end='\n'):
        self.Print( Str1=Str1, Str2=Str2, LogLevel = PrintLogLevel.INFO, ShowInDisplay = False, end=end)

    def INFOLCD(self, Str1='', Str2=''):
        self.Print( Str1=Str1, Str2=Str2, LogLevel = PrintLogLevel.INFOLCD, ShowInDisplay = True)

    def DEBUG(self, Str1='', Str2=''):
        self.Print( Str1=Str1, Str2=Str2, LogLevel = PrintLogLevel.DEBUG, ShowInDisplay = False)

    def DEBUGLCD(self, Str1='', Str2=''):
        self.Print( Str1=Str1, Str2=Str2, LogLevel = PrintLogLevel.DEBUGLCD, ShowInDisplay = True)

    def VERBOSE(self, Str1='', Str2=''):
        self.Print( Str1=Str1, Str2=Str2, LogLevel = PrintLogLevel.VERBOSE, ShowInDisplay = False)


    def TestPrint(self):

             self.FATAL   (' Testing: FATAL   ')
             self.ERROR   (' Testing: ERROR   ')
             self.WARNING (' Testing: WARNING ')
             self.INFOLCD (' Testing: INFOLCD ')
             self.INFO    (' Testing: INFO    ')
             self.DEBUG   (' Testing: DEBUG   ')
             self.DEBUGLCD(' Testing: DEBUGLCD')
             self.VERBOSE (' Testing: VERBOSE ')
   

