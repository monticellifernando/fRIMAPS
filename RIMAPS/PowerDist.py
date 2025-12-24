from RIMAPS.RIMAPS import RIMAPS
import numpy as np
from matplotlib import pyplot as plt

class Powerdist(RIMAPS):

    nombre = 'PSD'

    m_circulo = []

    m_fft_abs2 = []
    
    m_fft_abs2_log = []

    m_PSD_x = []
    m_PSD_y = []




    def __init__(self, nombre='PSD'):
        self.INFO(f'New {nombre}')
        self.nombre = nombre
        super().__init__()

    def SavePSD(self):
        print()

    def PlotLogFFT(self):
        self.INFO(f'Plotting log 2DFFT² ')
        plt.imshow(self.m_fft_abs2_log)
        plt.colorbar(label='Pixel Intensity')
        plt.show()


    def IntegralPSD(self, radio=1, useLog=False):
        # Integrates the power FFT on the pixels in the defined circle
        self.Circulo(radio = radio)
        m_integral = 0

        m_fft = self.m_fft_abs2

        if useLog:
            m_fft = self.m_fft_abs2_log

        for pixel in self.m_circulo:
            m_fft_in_pixel = m_fft[pixel[0]][pixel[1]]
            self.VERBOSE(f'     m_integral += {m_fft_in_pixel}')
            m_integral = m_integral + m_fft_in_pixel

        return m_integral
        

    def ComputePSD(self, useLog=False):
        # Compute the PSD for the ffT image
        # First lets compute the 2D FFT (if not there)
        self.INFO(f'Compute PSD {"Using Log scale" if useLog else ""}')
        if len(self.m_fft) == 0 :
            self.DEBUG('    No FFT 2D available. Computing')
            self.Get2DFFT()

        if len(self.m_fft_abs2) == 0:
            self.DEBUG('    No Power FFT available. Computing')
            self.m_fft_abs2 = np.abs(self.m_fft)**2
            self.DEBUG('    Computing also logaritm of Power FFT')
            self.m_fft_abs2_log = np.log10(self.m_fft_abs2)


        # Do it from radious 1 to the radious corresponding to the minimum of the shape
        fftshape = self.m_fft_abs2.shape
        MaxRad = min(fftshape[0],fftshape[1])
        self.VERBOSE(f' ffthsape = {fftshape}, MaxRad = {MaxRad}')
        self.m_PSD_x = []
        self.m_PSD_y = []
        for r in range(1,MaxRad):
            self.DEBUG(f'   ComputePSD for r = {r}')
            self.m_PSD_x.append(r)
            self.m_PSD_y.append(self.IntegralPSD(r, useLog))
            self.DEBUG(' ')


    def PlotPSD(self, filename = '', show = False):
        self.INFO('PlotPSD')
        if len(self.m_PSD_x) > 0 and len(self.m_PSD_y) > 0 :
            plt.plot(self.m_PSD_x,self.m_PSD_y)
            plt.yscale('log')
            if show:
                plt.show()
            if filename != '':
                self.DEBUG(f'Safing figure {filename}')
                plt.savefig(filename)
        else:
            self.ERROR('No PSD available :-(')


    def DumpPSD(self, filename ):
        with open(filename, 'w') as f:
            for data in range(len(self.m_PSD_x)):
                f.write(f'{self.m_PSD_x[data]}  {self.m_PSD_y[data]}')
            f.close()

        self.INFO(f'PSD text file written in {filename}')

    



    def Circulo(self,radio=1):
        self.DEBUG(f'Curculo(radio={radio})')
        # Te devuelve la lista de indices de la imagen que corresponden a los pixeles más cercanos a un circulo de radio radio alrededor del centro


        if radio < 1:
            self.ERROR(f'No. I can\'t do a circle with radious {radio}')
            return

        # Pixel central: Lo sacamos con el tamaño de la imagen
        [x,y] = self.m_fft.shape

        self.m_circulo.clear()

        centro = [int(x/2), int(y/2)]

        # First append [x=0, y=r-1]

        r = abs(int(radio)) # Need to be sure its a positive  integer

        self.m_circulo.append( [0,r-1] )
        while self.m_circulo[-1][1] > 0:
            # keep y and increase x
            self.DEBUG(f'   Adding to circle {self.m_circulo} ')

            best_distance = 999
            pix_candidate = []

            m_newpixs = [[1,0], [1,-1], [0,-1]]
            for m_p in m_newpixs:
                # Check if radious is not more than r+1
                n_pix = [ self.m_circulo[-1][0] + m_p[0], self.m_circulo[-1][1] + m_p[1]]
                self.DEBUG(f'   Checking pixel {n_pix} on top of last circulo = {self.m_circulo[-1]} ->  ({m_p})')
                if n_pix[0] < 0 or n_pix[1] < 0:
                    self.DEBUG(f'   Negative position, skipping: {n_pix}')
                    continue

                r_2 = n_pix[0]**2 + n_pix[1]**2
                m_distance = abs(r_2 - (r-1)**2)
                self.DEBUG(f'        pixel candidate {n_pix}, r² = {r_2}, actual radious² = {r**2} , radious distances = {m_distance}')
                if m_distance < best_distance:
                    best_distance = m_distance
                    pix_candidate = n_pix
            self.DEBUG(f'   Best distance! {n_pix}, r² = {r_2} ')

            # here we get the best matching pix to he radious
            self.m_circulo.append(pix_candidate)
            self.DEBUG(' ')



