from RIMAPS.RIMAPS import RIMAPS

class Powerdist(RIMAPS):

    nombre = 'PSD'

    m_circulo = []


    def __init__(self, nombre='PSD'):
        self.INFO(f'New {nombre}')
        self.nombre = nombre
        super().__init__()


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
            print()




            


                


        # Now, lets fill until I get index y = 0

        print(centro)


 








