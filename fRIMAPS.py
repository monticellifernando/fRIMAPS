#!env python3
# -*- coding: utf-8 -*-
import sys, getopt, math, os
import argparse

from RIMAPS import RIMAPS
from RIMAPS.Print import PrintLogLevel


def Get1DFFtFromImage(m_img):

    m_1d_img=[]
    # primero agarro cada columna, promedio todo y asigno eso a la posición del vector
    cols,rows = m_img.shape
    for col in range(cols):
        m_value_col=0
        for row in range(rows):
            m_value_col=m_value_col+m_img[col][row]
        m_1d_img.append(float(m_value_col)/float(cols))

    #m_fft=np.fft.rfft(m_img_r)
    #m_fft_1d=1.*np.abs(np.fft.rfft(m_1d_img))
    m_fft_1d=(np.fft.rfft(m_1d_img))
    return(m_fft_1d)






def ObtenerMaximo(data, GlobalMaximum):
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
        m_maximo_local=GlobalMaximum or (m_local>m_prev and m_prev>m_prev_prev and m_local>m_post and m_post > m_post_post)

        if m_maximo_local and m_local > maximo:
            maximo=m_local
    return maximo

def SaveData(y_data,x_data=0, Name='datos.txt'):
    of = open(Name,'w')
    of.write('# [Ángulo]  [Máximo de ampliatud de la FFT]\n')
    for entry in range(len(y_data)):
        try:
            x=x_data[entry]
            y=y_data[entry]
            of.write('%f %f \n' %(x,y))
        except:
            print('Hey!!! Algo pasó aca que no pude grabar el archivo de datos. Fer aprene a programar!')
    of.close()



def PlotDataset(data, x=0, Name="test.png"):
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


def Plot3D(m_3d_fig):
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

   
def RotateImage(m_img, m_angle=0.2):
  image_center = tuple(np.array(m_img.shape)/2)
  rot_mat = cv2.getRotationMatrix2D(image_center,m_angle,1.41)
  result = cv2.warpAffine(m_img, rot_mat, m_img.shape,flags=cv2.INTER_LINEAR)
  return result

def GetRIMAPS(m_img,m_Steps,  GlobalMaximum, Debug=False):

    print(f'Processig image of size {m_img.shape}')
    
    x_output=[]
    y_output=[]
    m_angle=0
    m_end = '\r'
    for Step in (range(m_Steps+1)):
        if Step==m_Steps:
            m_end = '\n'
        m_angle= 180./m_Steps*Step
        print(f'Step {Step}/{m_Steps}, angle = {m_angle}⁰', end=m_end)
        m_img_r=RotateImage(m_img,m_angle)
        #plt.imshow(m_img_r, cmap = 'gray')
        #plt.show()
        # m_fft=Get1DFFtFromImage(m_img_r)
        # #m_fft=np.fft.rfft(m_img_r)
        # #print("Size = "+str(m_fft.shape))
        # fft_1d= 1.*np.abs(m_fft)[1:] # FFT de la imagen en 2D
        
        
        fft_1d= 1.*np.abs(np.fft.rfft2(m_img_r)[0][:])[1:] # FFT de la imagen en 2D
        if Debug:
            print(f'{fft_1d}, Shape = {fft_1d.shape}')
        maximo=ObtenerMaximo(fft_1d, GlobalMaximum)
        x_output.append(m_angle)
        y_output.append(maximo)
        #Plot3D(fft_1d)
        #print("Angulo "+str(m_angle)+" Maximo = "+str(maximo))
        #PlotDataset(fft_1d)

    return x_output,y_output






def GetLocalMaxima(m_e, X_max=-1, Y_max=-1):
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
        

def main(argv):
  parser = argparse.ArgumentParser("FreeMAPS - the Free/Libre RIMAPS analysis tool")
  parser.add_argument('-f', '--FileName',  required=True, help="Input image file. Accepted file formats are png and jpeg")
  parser.add_argument('--Size',  required=False, help="Size of the output FFT", type=int)
  parser.add_argument('-L','--LogScale', help="Mostrar en escala logaritmica", action="store_true")
  parser.add_argument('-B','--BlockRange', help="Defines the size of the window of NxN of content to be erase from the outptu FFT", type=int)
  parser.add_argument('-F','--FilterRange', help="Filtrar Rango en FFT", type=int)
  parser.add_argument('-S','--Steps', help="Steps en 180 grados", type=int, default=60)
  parser.add_argument('--LogLevel', help='Print LogLevel. Possible: FATAL, ERROR, WARNING, INFO, DEBUG, VERBOSE ', type=str, default='INFO')
  #parser.add_argument('-s','--SaveFFT', help="Save 2D FFT", action="store_true")
  parser.add_argument('-G','--GlobalMaximum', help="Usa Maximo Global en vez de Maximo Local", action="store_true")

  args = parser.parse_args()

  m_R = RIMAPS.RIMAPS()
  m_R.SetLogLevel(getattr(PrintLogLevel, args.LogLevel))

  m_R.LogScale = args.LogScale
  m_R.Steps = args.Steps

  m_R.AddImageFromFile(args.FileName)


  x_MAPS, y_MAPS = m_R.GetRIMAPS()

  out_filename = "MAPS_"+args.FileName.replace('/','_')
  if args.GlobalMaximum: out_filename="RIMAPS_G_"+args.FileName.replace('/','_')
  out_filename_data = out_filename.replace('.png','').replace('.jpg','')+'.txt'
  m_R.SaveData(y_MAPS,x_MAPS,out_filename_data)
  m_R.PlotDataset(y_MAPS,x_MAPS,out_filename)
  
  
  # # Load an color image in grayscale
  # 
  # filename=args.FileName
  # m_tamano=0
  # if (args.Size):
  #     m_tamano=args.Size

  # 
  # 
  # img = cv2.imread(filename,0)



  # #if args.LogScale:
  # #    magnitude_spectrum = 20*np.log(absf)
  # #else:
  # #    magnitude_spectrum = absf

  # #if (args.Debug):
  # #    print(f'DEBUG:: magnitude_spectrum = {absf}, shape = {absf.shape}')

  # #if m_tamano >0:
  # #    magnitude_spectrum = magnitude_spectrum[0:m_tamano:1,0:m_tamano:1]

  # #if args.BlockRange:
  # #    magnitude_spectrum[0:args.BlockRange:1,0:args.BlockRange:1]=0


  # #cols,rows = magnitude_spectrum.shape
  # #if args.FilterRange:
  # #    magnitude_spectrum[args.FilterRange:cols:1,args.FilterRange:rows:1]=0
  # #    magnitude_spectrum[0:cols:1,args.FilterRange:rows:1]=0
  # #    magnitude_spectrum[args.FilterRange:cols:1,0:rows:1]=0
  # #    f[args.FilterRange:f_cols:1,args.FilterRange:f_rows:1]=0
  # #    f[0:f_cols:1,args.FilterRange:f_rows:1]=0
  # #    f[args.FilterRange:f_cols:1,0:f_rows:1]=0


  # 
  # x_MAPS, y_MAPS = GetRIMAPS(img,args.Steps, args.GlobalMaximum, args.Debug) 
  # #print(y_MAPS)

  # out_filename = "MAPS_"+filename.replace('/','_')
  # if args.GlobalMaximum: out_filename="RIMAPS_G_"+filename.replace('/','_')
  # out_filename_data = out_filename.replace('.png','').replace('.jpg','')+'.txt'
  # SaveData(y_MAPS,x_MAPS,out_filename_data)
  # PlotDataset(y_MAPS,x_MAPS,out_filename)




if __name__ == "__main__":
    main(sys.argv[1:])
