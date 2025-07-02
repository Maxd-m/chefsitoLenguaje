class AnalizadorSemantico:
    def __init__(self, tokens):
        self.tokens = tokens
        self.ingredientes = {}  # Para guardar los declarados
        self.errores = []

    def analizar(self):
        self.extraer_ingredientes()
        self.verificar_procedimiento()
        self.mostrar_errores()

    def extraer_ingredientes(self):
        print("🔍 Buscando ingredientes declarados...")

        i = 0
        while i < len(self.tokens):
            token = self.tokens[i]

            if token['tipo'] == 'PALABRA_RESERVADA_INGREDIENTES':
                i += 1
                while i + 2 < len(self.tokens) and \
                        self.tokens[i]['tipo'] == 'IDENTIFICADOR' and \
                        self.tokens[i+1]['tipo'] == 'CONSTANTE_NUMERICA' and \
                        self.tokens[i+2]['tipo'] in ['PALABRA_RESERVADA_KILOS', 'PALABRA_RESERVADA_LITROS', 'PALABRA_RESERVADA_PIEZAS']:

                    nombre = self.tokens[i]['valor']
                    if nombre in self.ingredientes:
                        self.errores.append(f"Ingrediente duplicado: '{nombre}' ya fue declarado.")
                    else:
                        self.ingredientes[nombre] = {
                            'valor': self.tokens[i+1]['valor'],
                            'unidad': self.tokens[i+2]['valor']
                        }
                        print(f"✅ Ingrediente agregado: {nombre}")

                    i += 3
                continue
            i += 1

    def mostrar_errores(self):
        if self.errores:
            print("\n❌ Errores semánticos encontrados:")
            for err in self.errores:
                print("  -", err)
        else:
            print("\n✅ Análisis semántico completado sin errores.")

    def verificar_procedimiento(self):
        print("🔍 Verificando identificadores usados en el PROCEDIMIENTO...")

        i = 0
        while i < len(self.tokens):
            token = self.tokens[i]
            if token['tipo'] in [
                'PALABRA_RESERVADA_AÑADIR',
                'PALABRA_RESERVADA_SEPARAR',
                'PALABRA_RESERVADA_HORNEAR',
                'PALABRA_RESERVADA_CORTAR'
            ]:
                instruccion = token['tipo'].replace('PALABRA_RESERVADA_', '')
                print(f"🔸 Analizando instrucción {instruccion}...")

                if i + 5 < len(self.tokens):
                    if self.tokens[i+1]['tipo'] == 'PARENTESIS_ABRE' and \
                    self.tokens[i+2]['tipo'] == 'IDENTIFICADOR' and \
                    self.tokens[i+3]['tipo'] == 'SIGNO_COMA' and \
                    self.tokens[i+4]['tipo'] == 'IDENTIFICADOR' and \
                    self.tokens[i+5]['tipo'] == 'PARENTESIS_CIERRA':

                        ident1 = self.tokens[i+2]['valor']
                        ident2 = self.tokens[i+4]['valor']

                        if ident1 not in self.ingredientes:
                            self.errores.append(f"Ingrediente '{ident1}' usado en {instruccion} pero no fue declarado.")
                        if ident2 not in self.ingredientes:
                            self.errores.append(f"Ingrediente '{ident2}' usado en {instruccion} pero no fue declarado.")

                        i += 6
                        continue
                else:
                    self.errores.append(f"Formato incompleto en instrucción {instruccion} en posición {i}")
            i += 1



