import csv

class AnalizadorLexicoChefsito:
    def __init__(self, archivoMatriz):
        self.archivoMatriz = archivoMatriz
        self.automata = {}
        self.alfabeto = []
        self.mapeo_caracteres = {}
        self.debug = False

        self.tiposToken = {
            '1000': 'PALABRA_RESERVADA_AÑADIR',
            '1020': 'PALABRA_RESERVADA_COCINAR', 
            '1040': 'PALABRA_RESERVADA_CORTAR',
            '1060': 'PALABRA_RESERVADA_EN',
            '1080': 'PALABRA_RESERVADA_FIN',
            '1100': 'PALABRA_RESERVADA_HORNEAR',
            '1120': 'PALABRA_RESERVADA_INGREDIENTES',
            '1140': 'PALABRA_RESERVADA_INICIO',
            '1160': 'PALABRA_RESERVADA_KILOS',
            '1180': 'PALABRA_RESERVADA_LITROS',
            '1200': 'PALABRA_RESERVADA_MIENTRAS_HAYA',
            '1220': 'PALABRA_RESERVADA_MINUTOS',
            '1240': 'PALABRA_RESERVADA_PIEZAS',
            '1260': 'PALABRA_RESERVADA_POR',
            '1280': 'PALABRA_RESERVADA_PROCEDIMIENTO',
            '1300': 'PALABRA_RESERVADA_RECETA',
            '1320': 'PALABRA_RESERVADA_SEPARAR',
            '1340': 'PALABRA_RESERVADA_SI_HAY',
            '1360': 'PALABRA_RESERVADA_TUPPER',
            '1380': 'PALABRA_RESERVADA_VACIAR',
            '1400': 'PALABRA_RESERVADA_VER',
            '3000': 'SIGNO_COMA',
            '3020': 'SIGNO_PUNTO',
            '5000': 'PARENTESIS_ABRE',
            '5020': 'PARENTESIS_CIERRA',
            '3040': 'ESPACIO',
            '999': 'ERROR'
        }

        for e in ['6000', '6020']:
            self.tiposToken[e] = 'IDENTIFICADOR'
        for e in ['7000', '7020', '8000', '8020']:
            self.tiposToken[e] = 'CONSTANTE_NUMERICA'

        self.cargarMatrizTransicion()

    def cargarMatrizTransicion(self):
        try:
            with open(self.archivoMatriz, 'r', encoding='utf-8') as f:
                lineas = f.readlines()
                encabezados = lineas[0].strip().split(',')
                for i in range(len(encabezados)):
                    if encabezados[i] == "":
                        encabezados[i] = " "
                self.alfabeto = encabezados[1:]
                self.mapeo_caracteres = {}
                for simbolo in self.alfabeto:
                    if simbolo.upper() == "COMA":
                        self.mapeo_caracteres[","] = simbolo
                    elif simbolo.isalpha():
                        self.mapeo_caracteres[simbolo.lower()] = simbolo
                        self.mapeo_caracteres[simbolo.upper()] = simbolo
                    else:
                        self.mapeo_caracteres[simbolo] = simbolo

                for i in range(1, len(lineas)):
                    linea = lineas[i].strip().split(',')
                    if len(linea) < 2:
                        continue
                    estado = linea[0]
                    if estado not in self.automata:
                        self.automata[estado] = {}
                    for j in range(1, min(len(linea), len(encabezados))):
                        simbolo = encabezados[j]
                        if j < len(linea) and linea[j]:
                            self.automata[estado][simbolo] = linea[j]
        except Exception as e:
            print(f"❌ Error al cargar la matriz de transición: {e}")

    def obtenerColumna(self, caracter):
        return self.mapeo_caracteres.get(caracter)

    def esFinal(self, estado):
        return estado in self.tiposToken and not self.esError(estado)

    def esError(self, estado):
        return estado == '999'

    def esEstadoNumericoValido(self, estado):
        return estado in ['7000', '8000', '7020', '8020', 'q87']

    def procesarTexto(self, texto):
        tokens_encontrados = []
        errores_lexicos = []
        i = 0
        while i < len(texto):
            if texto[i] in [' ', '\t', '\n', '\r']:
                i += 1
                continue
            resultado = self.procesarToken(texto, i)
            if resultado['token']:
                tokens_encontrados.append(resultado['token'])
                i = resultado['token']['posicion'] + len(resultado['token']['valor'])
            else:
                errores_lexicos.append(resultado['error'])
                i = resultado['siguiente_posicion']
        return tokens_encontrados, errores_lexicos

    def procesarToken(self, texto, posicion_inicial):
        estado = 'q0'
        token_actual = ""
        ultimo_estado_final = None
        ultimo_token_valido = ""
        ultima_posicion_valida = posicion_inicial
        i = posicion_inicial

        while i < len(texto):
            caracter = texto[i]

            if caracter in [' ', '\t', '\n', '\r']:
                if token_actual:
                    break
                i += 1
                posicion_inicial += 1
                continue

            columna = self.obtenerColumna(caracter)
            if columna is None:
                break

            if estado in self.automata and columna in self.automata[estado]:
                nuevo_estado = self.automata[estado][columna]

                if self.esError(nuevo_estado):
                    break

                estado = nuevo_estado
                token_actual += caracter

                if self.esFinal(estado) or self.esEstadoNumericoValido(estado):
                    ultimo_estado_final = estado
                    ultimo_token_valido = token_actual
                    ultima_posicion_valida = i + 1

                i += 1
            else:
                break

        if ultimo_estado_final:
            if ultima_posicion_valida == posicion_inicial:
                ultima_posicion_valida += 1  # ← fuerza el avance aunque sea 1 letra

            tipo_token = self.tiposToken.get(ultimo_estado_final, 'TOKEN_DESCONOCIDO')
            token = {
                'valor': ultimo_token_valido,
                'tipo': tipo_token,
                'estado_final': ultimo_estado_final,
                'posicion': posicion_inicial
            }
            return {
                'token': token,
                'error': None,
                'siguiente_posicion': ultima_posicion_valida
            }
        else:
            caracter_error = texto[posicion_inicial] if posicion_inicial < len(texto) else 'EOF'
            error = f"❌ Token no válido: '{caracter_error}' en posición {posicion_inicial}"
            return {
                'token': None,
                'error': error,
                'siguiente_posicion': posicion_inicial + 1
            }


if __name__ == '__main__':
    archivo_matriz = 'vamoss.csv'
    analizador = AnalizadorLexicoChefsito(archivo_matriz)
    texto = """
    INICIO
    INGREDIENTES
    AGUA 10.5 LITROS
    HUEVOS 3 PIEZAS 
    PROCEDIMIENTO
    AÑADIR(AGUA,HUEVOS) EN TUPPER.hola
    FIN
    """
    resultado = analizador.procesarTexto(texto)
    print("\n📌 TOKENS ENCONTRADOS:")
    for tok in resultado[0]:
        print(tok)
    print("\n❗ ERRORES LÉXICOS:")
    for err in resultado[1]:
        print(err)
