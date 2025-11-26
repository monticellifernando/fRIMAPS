from RIMAPS.Print import Print, PrintLogLevel

import numpy as np
import cv2
import array
from matplotlib import cm
from matplotlib import pyplot as plt
from matplotlib.ticker import LinearLocator, FormatStrFormatter
class RIMAPS(Print):
    ''' 
    Class defined for RIMAPS analysis
    '''

    # Parameters
    LogScale = False      # whether to plot out in Log Scale

    BlockRange = 0        # Defines the size of the window of NxN of content to be erase from the outptu FFT

    Size = 0              # Size of the output FFT
    FilterRange = 0       # FFT range to Filter
    Steps       = 100     # Number of steps to rotate between 0 and 180 degrees
    LogLevel    = 4       # LogLevel of putput print out. 4 = INFO
    GlobalMaximum = False # Makes use of global maximum instead of Local maximum
    
    # Objects:

    m_img = None          # Loaded image
    m_img_r = None        # Rotated image by angle

    m_centered_2Dfft = []

    m_fft = []


    def __init__(self):
        self.INFO('New RIMAPS')

    def AddImage(self, image):
        self.INFO('Setting up Image')
        self.m_img   = image
        self.m_img_r = image

    def AddImageFromFile(self, m_file):
        self.INFO(f'Opening image from file {m_file}')
        image = cv2.imread(m_file,0)
        self.AddImage(image)

    def PlotImage(self):
        self.INFO(f'Plotting Image')
        plt.imshow(self.m_img_r)
        plt.colorbar(label='Pixel Intensity')
        plt.show()

    def PlotFFT(self):
        self.INFO(f'Plotting 2DFFT')
        plt.imshow(np.abs(self.m_fft))
        plt.colorbar(label='Pixel Intensity')
        plt.show()




    
    def Get1DFFtFromImage(self):
    
        m_1d_img=[]
        # primero agarro cada columna, promedio todo y asigno eso a la posición del vector
        cols,rows = self.m_img.shape
        for col in range(cols):
            m_value_col=0
            for row in range(rows):
                m_value_col=m_value_col+self.m_img[col][row]
            m_1d_img.append(float(m_value_col)/float(cols))
    
        #m_fft=np.fft.rfft(m_img_r)
        #m_fft_1d=1.*np.abs(np.fft.rfft(m_1d_img))
        m_fft_1d=(np.fft.rfft(m_1d_img))
        return(m_fft_1d)
    
    
    
    
    
    
    def GetMaxValue(self, data):
        cantidad=len(data)-1
        maximo=-1
        #if (GlobalMaximum): 
        #    for i in range(1,cantidad-1):
        #        m_local=data[i]
    
        #        if  m_local > maximo:
        #            maximo=m_local
    
        #else:
        for i in range(2,cantidad-2):
            m_local=data[i]
            m_prev=data[i-1]
            m_prev_prev=data[i-2]
            m_post=data[i+1]
            m_post_post=data[i+2]
            m_maximo_local=self.GlobalMaximum or (m_local>m_prev and m_prev>m_prev_prev and m_local>m_post and m_post > m_post_post)
    
            if m_maximo_local and m_local > maximo:
                maximo=m_local
        return maximo
    
    def SaveData(self, y_data,x_data=0, Name='datos.txt'):
        of = open(Name,'w')
        of.write('# [Ángulo]  [Máximo de ampliatud de la FFT]\n')
        for entry in range(len(y_data)):
            try:
                x=x_data[entry]
                y=y_data[entry]
                of.write('%f %f \n' %(x,y))
            except:
                self.ERROR('Hey!!! Algo pasó aca que no pude grabar el archivo de datos. Fer aprene a programar!')
        of.close()
    
    
    
    def PlotDataset(self, data, x=0, Name="test.png"):
        cantidad=(len(data))
        if not x:
            x = range(cantidad)
        fig = plt.figure()
        ax1 = fig.add_subplot(111)
    
        #print(data)
        ax1.scatter(x[:cantidad], np.asarray(data)[:cantidad], s=10, c='b', marker="s", label='first')
        plt.title(Name)# , plt.xticks([]), plt.yticks([])
        # plt.show()
        fig.savefig(f'{Name}')
    
    
    def Plot3D(self, m_3d_fig):
      cols,rows = m_3d_fig.shape
      fig = plt.figure()
      ax = fig.gca(projection='3d')
      X, Y = np.mgrid[:cols,:rows]
      
      #surf = ax.plot_wireframe(X, Y, magnitude_spectrum, rstride=2, cstride=2,
      surf = ax.plot_surface(Y, X, m_3d_fig, rstride=1, cstride=1, cmap=cm.jet,
                             linewidth=0, antialiased=False)
      
      ax.zaxis.set_major_locator(LinearLocator(10))
      ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
      
      #fig.savefig(out_filename)
      plt.show()

    def Get2DFFT(self, s = None):
        # Computs the 2D FFT of the image
        self.INFO('Computing 2D FFT')
        self.m_fft = np.fft.rfft2(self.m_img_r, s = s)

    def CenterFFT(self):
        # Centers the 2D FFT so the 0,0 frequiency is in the center of the graph. Namely you get positive and negative frequency domains for both k_x and k_y
        self.INFO('Centering 2D FFT')
        self.m_fft = np.fft.fftshift(self.m_fft)


    def RotateImage(self, m_angle=0.2):
        # Rotates the image to an angle m_angle
        image_center = tuple(np.array(self.m_img.shape)/2)
        rot_mat = cv2.getRotationMatrix2D(image_center,m_angle,1.41)
        self.m_img_r = cv2.warpAffine(self.m_img, rot_mat, self.m_img.shape,flags=cv2.INTER_LINEAR)
    
    def GetRIMAPS(self): #m_img,m_Steps,  GlobalMaximum, Debug=False):
        # Well, compute the RIMAPS graph for the provided image and number of steps
    
        self.INFO(f'Processig image of size {self.m_img.shape}')
        
        x_output=[]
        y_output=[]
        m_angle=0
        m_end = '\r'
        for Step in (range(self.Steps+1)):
            if Step==self.Steps:
                m_end = '\n'
            m_angle= 180./self.Steps*Step
            self.INFO(f'Step {Step}/{self.Steps}, angle = {m_angle}⁰', end=m_end)
            self.RotateImage(m_angle)

            self.Get2DFFT() # compute the FFT of the rotated image
            
            
            fft_1d= 1.*np.abs(self.m_fft[0][:])[1:] # 1D FFT de la imagen en 2D
            
            self.DEBUG(f'{fft_1d}, Shape = {fft_1d.shape}')
            maximo=self.GetMaxValue(fft_1d)
            x_output.append(m_angle)
            y_output.append(maximo)
    
        return x_output,y_output
    
    
    
    
    
    
    def GetLocalMaxima(self, m_e, X_max=-1, Y_max=-1):
        # Loopear sobre todo el espectro en 2D. Es un máximo local si *ninguno* de sus vecinos es igual o superior
        columnas,filas=m_e.shape
        if X_max>0 and X_max<columnas:
            columnas=X_max
    
        if Y_max>0 and Y_max<filas:
            filas=Y_max
    
    
        # [AI] [A] [AD]
        #  [I] [F]  [D]
        # [BI] [B] [BD]
    
        # tengo que recorrer la imagen entre la columna 1 y la anteúltima y la fila 1 y la anteúltima
    
        # guardo en "m_maximos_locales" una lista de ntuplas con F,x,y, donde F es el valor de la amplitud de la FFT en el máximo local en x,y 
        m_maximos_locales=[]
    
        for f in range(1,filas-2):
            for c in range(1,columnas-2):
                m_F  = m_e[c,f]
                m_BD = m_e[c+1,f+1]
                m_D  = m_e[c+1,f]
                m_BI = m_e[c+1,f-1]
                m_B  = m_e[c,f+1]
                m_I  = m_e[c,f-1]
                m_AD = m_e[c-1,f+1]
                m_A  = m_e[c-1,f]
                m_AI = m_e[c-1,f-1]
    
                # if (debug):
                #     print()
                #     print( m_AI,   m_A,  m_AD )
                #     print( m_I,   m_F,  m_D )
                #     print( m_B,   m_B,  m_BD )
                #     print()
                if m_F < 0:
                    # if debug: 
                    #     print ("No!!!! m_F = "+str(m_F)+" < 0 !!!!/ Necesito que pases el abs()!!!")
                    returnm_maximos_locales
    
                
                if m_F > m_BD and m_F > m_D  and m_F > m_BI and m_F > m_B  and m_F > m_A  and m_F > m_AD and m_F > m_A  and m_F > m_AI :
                     m_maximos_locales.append( (m_F, c, f) )
                     #print ("máximo local! -> ", str(m_F))
    
        return m_maximos_locales
            
    
    
