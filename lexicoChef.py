import csv

class Lexico:
    def __init__(self, cadenas):
        filename = 'malo(2).csv'
        self.estados_finales_reservadas = [1000,1020,1040,1060,1080,1100,1120,1140,1160,1180,1200,1220,1240,1260,1280,1300,1320,1340,1360,1380,1400]
        
        # self.estados_finales_operadores = [2010, 2020, 2030, 2040, 2050, 2060, 2070, 2080, 2090, 2100, 2110, 2120, 2130, 2140, 2150, 2160, ]

        self.estados_finales_separadoes = [3000, 3020]

        # self.estados_finales_llaves = [4000, 4100]
        self.estados_finales_parentesis = [5000, 5020]


        self.estados_finales_numeros = [7020, 8020]

        self.finales=[self.estados_finales_reservadas + self.estados_finales_separadoes + self.estados_finales_parentesis + self.estados_finales_numeros + [6020] + [9000,999]]
        # print("Estados finales reservadas: ", self.finales[0])
        self.tokens = []  # Lista para guardar los tokens reconocidos

        # Inicializar el diccionario vacío
        self.mat_transicion = {}

        # Abrir el archivo CSV
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            # Iterar a través de las filas y organizar los datos en el diccionario
            for row in reader:
                for column, value in row.items():
                    if column not in self.mat_transicion:
                        self.mat_transicion[column] = []
                    self.mat_transicion[column].append(value)  
        
        # print(self.mat_transicion['Ñ'][0])  # Imprimir la matriz de transición para verificar su contenido

    
        #Separar texto en varias cadenas
        # palabras = cadenas.split()
        # for palabra in palabras:

        self.estado_actual=0
        #Tipo de caracter 
        self.tipo_actual=' '
        # self.flg_reconoce=True
        #Analizar cada cadena
        self.leer_cadena(cadenas)
        # print("Tokens reconocidos: ", self.tokens)  # Imprimir todos los tokens reconocidos

        # return self.tokens

    def leer_cadena(self,cadena):
        cont = 1
        historial = []  # Lista para guardar los últimos caracteres
        for caracter in cadena:

            historial.append(caracter)
            if len(historial) > 11:  # Mantener solo los últimos 10 caracteres
                historial.pop(0)

            if cont == 3:
                break

            self.tipo_actual=caracter
            # print("Tipo actual: ", self.tipo_actual)
            # print("Estado actual: ", self.estado_actual)

            if self.estado_actual == None:
                    self.estado_actual = 999

            if not self.estado_actual == 999:
                
                # print('---------------------------------------------')
                # print("tipo actual: ", self.tipo_actual)
                # print("Estado anterior: ", self.estado_actual)

                
                
                
                if self.tipo_actual == ' ':
                    self.tipo_actual = 'blank'

                # print("Estado actual00: ", self.estado_actual)
                
                try:
                    self.estado_actual = self.mat_transicion[self.tipo_actual][int(self.estado_actual)]
                    # print("Estado actual: ", self.estado_actual)
                except KeyError:
                    print(f"Error: El tipo '{self.tipo_actual}' no está definido en la matriz de transición.")
                    self.estado_actual = 999
                    break
                if self.estado_actual == '6000':
                    self.estado_actual = '130'
                if self.estado_actual == '7000':
                    self.estado_actual = '131'
                if self.estado_actual == '8000':
                    self.estado_actual = '132'
                

                if int(self.estado_actual) in self.finales[0]:
                    print("Estado final alcanzado: ", self.estado_actual)
                    self.reconocer()
            else:
                # print('Error lexico en: ',caracter, " no se reconoce")
                # print('Error léxico en:', caracter, "- no se reconoce")
                print('Error lexico en el ultimo caracter de:', ''.join(historial))
                return
                # break
        

            
            # self.tokens.append(self.mat_transicion['fila'][self.estado_actual])
        # else:
            # self.tokens.append(self.mat_transicion['fila'][self.estado_actual])

    def reconocer(self):
        self.estado_actual = int(self.estado_actual)
        # objetivo = int(self.mat_transicion['fila'][self.estado_actual])
        objetivo = int(self.estado_actual)


        if objetivo in self.estados_finales_reservadas:
            self.tokens.append(self.estado_actual)
            self.estado_actual=0
            self.tipo_actual=' '
        elif objetivo in self.estados_finales_numeros:
            self.tokens.append(self.estado_actual)
            # self.tokens.append(self.mat_transicion['fila'][self.estado_actual])
            self.estado_actual=0
            self.tipo_actual=' '
        
        elif objetivo in self.estados_finales_separadoes:
            self.tokens.append(self.estado_actual)
            self.estado_actual=0
            self.tipo_actual=' '
            # self.tokens.append(self.mat_transicion['fila'][self.estado_actual])
        
        elif objetivo in self.estados_finales_parentesis:
            self.tokens.append(self.estado_actual)
            self.estado_actual=0
            self.tipo_actual=' '
            # self.tokens.append(self.mat_transicion['fila'][self.estado_actual])
        elif objetivo == 6020:
            self.tokens.append(self.estado_actual)
            self.estado_actual=0
            self.tipo_actual=' '
        elif objetivo == 9000:
            self.tokens.append(self.estado_actual)
            self.estado_actual=0
            self.tipo_actual=' '
        elif objetivo == 999:
            self.tokens.append(self.estado_actual)
            self.estado_actual=999
            self.tipo_actual=' '

    def comparar_matriz(self, objetivo):
        if int(objetivo)==999:
            self.flg_reconoce=False
        # Estado 9 es de aceptacion
        elif int(objetivo) in self.estados_finales:
            self.flg_reconoce=True
        else:
            self.flg_reconoce=False
        
    def encontrar_fila(self, encontrar):
        izq = 0
        der = len(self.mat_transicion['fila']) - 1

        while izq <= der:
            medio = (izq + der) // 2
            if self.mat_transicion['fila'][medio] == encontrar:
                # self.estado_actual = medio
                # print("Encontrado en indice: ", medio)
                # print("Encontrado en la fila: ", self.mat_transicion['fila'][medio])
                # break
                return medio
            elif self.mat_transicion['fila'][medio] < encontrar:
                izq = medio + 1
            else:
                der = medio - 1



texto = "inicio " \
"receta Hola2 " \
"ingredientes" \
"10.50 litros agua " \
"20 kilos harina " \
"procedimiento " \
"añadir(agua,harina) en tupper.mezcla " \
# "INGREDIENTES" \
# "AGUA 1 LITRO" 
aut=Lexico(texto.upper())
print("Tokens reconocidos: ", aut.tokens)  # Imprimir todos los tokens reconocidos
