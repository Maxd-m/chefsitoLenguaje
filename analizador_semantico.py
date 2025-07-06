class AnalizadorSemantico:
    def __init__(self, tokens):
        self.tokens = tokens
        self.ingredientes = {}  # identificadores declarados en INGREDIENTES
        self.tuppers = set()    # identificadores definidos en TUPPER
        self.instrucciones = [] # esquema de traducción 
        self.errores = []

    def analizar(self): 
        self.extraer_ingredientes()
        self.verificar_procedimiento()
        self.mostrar_errores()
        self.mostrar_traduccion()

    def extraer_ingredientes(self):
        print("Buscando ingredientes declarados...")

        i = 0
        while i < len(self.tokens):
            token = self.tokens[i]
            if token['tipo'] == 'PALABRA_RESERVADA_INGREDIENTES':
                i += 1
                while i + 2 < len(self.tokens) and \
                    self.tokens[i]['tipo'] == 'IDENTIFICADOR' and \
                    self.tokens[i+1]['tipo'] in ['CONSTANTE_NUMERICA_ENTERA', 'CONSTANTE_NUMERICA_FLOTANTE'] and \
                    self.tokens[i+2]['tipo'] in ['PALABRA_RESERVADA_KILOS', 'PALABRA_RESERVADA_LITROS', 'PALABRA_RESERVADA_PIEZAS']:

                    nombre = self.tokens[i]['valor']
                    tipo_constante = self.tokens[i+1]['tipo']
                    unidad = self.tokens[i+2]['valor']

                    tipo_correcto = (
                        (unidad in ['KILOS', 'LITROS'] and tipo_constante == 'CONSTANTE_NUMERICA_FLOTANTE') or
                        (unidad == 'PIEZAS' and tipo_constante == 'CONSTANTE_NUMERICA_ENTERA')
                    )

                    if not tipo_correcto:
                        self.errores.append(f"Unidad '{unidad}' requiere un número {'flotante' if unidad in ['KILOS', 'LITROS'] else 'entero'} en el ingrediente '{nombre}'.")
                    elif nombre in self.ingredientes:
                        self.errores.append(f"Ingrediente duplicado: '{nombre}' ya fue declarado.")
                    else:
                        self.ingredientes[nombre] = {
                            'valor': self.tokens[i+1]['valor'],
                            'unidad': unidad
                        }
                        print(f"✅ Ingrediente agregado: {nombre}")

                    i += 3
                continue
            i += 1


    def verificar_procedimiento(self):
        print(" Verificando instrucciones en el PROCEDIMIENTO...")

        i = 0
        while i < len(self.tokens):
            token = self.tokens[i]
            if token['tipo'] in ['PALABRA_RESERVADA_AÑADIR', 'PALABRA_RESERVADA_SEPARAR',
                                    'PALABRA_RESERVADA_HORNEAR', 'PALABRA_RESERVADA_CORTAR']:
                instruccion = token['tipo'].replace('PALABRA_RESERVADA_', '')
                print(f"🔸 Analizando instrucción {instruccion}...")

                if i + 9 < len(self.tokens):  # aseguramos que hay suficientes tokens
                    if self.tokens[i+1]['tipo'] == 'PARENTESIS_ABRE' and \
                        self.tokens[i+2]['tipo'] == 'IDENTIFICADOR' and \
                        self.tokens[i+3]['tipo'] == 'SIGNO_COMA' and \
                        self.tokens[i+4]['tipo'] == 'IDENTIFICADOR' and \
                        self.tokens[i+5]['tipo'] == 'PARENTESIS_CIERRA' and \
                        self.tokens[i+6]['tipo'] == 'PALABRA_RESERVADA_EN' and \
                        self.tokens[i+7]['tipo'] == 'PALABRA_RESERVADA_TUPPER' and \
                        self.tokens[i+8]['tipo'] == 'SIGNO_PUNTO' and \
                        self.tokens[i+9]['tipo'] == 'IDENTIFICADOR':

                        ident1 = self.tokens[i+2]['valor']
                        ident2 = self.tokens[i+4]['valor']
                        resultado = self.tokens[i+9]['valor']
                        self.tuppers.add(resultado)

                        # Verificar operandos
                        for ident in [ident1, ident2]:
                            if ident not in self.ingredientes and ident not in self.tuppers:
                                self.errores.append(f"Identificador '{ident}' en {instruccion} no ha sido declarado.")

                        # Traducción (esquema)
                        self.instrucciones.append({
                            'operacion': instruccion.lower(),
                            'operando1': ident1,
                            'operando2': ident2,
                            'resultado': resultado
                        })

                        i += 10
                        continue
                    else:
                        self.errores.append(f"Formato inválido para instrucción {instruccion} en posición {i}")
                else:
                    self.errores.append(f"Formato incompleto en instrucción {instruccion} en posición {i}")
            i += 1

    def mostrar_errores(self):
        if self.errores:
            print("\n❌ Errores semánticos encontrados:")
            for err in self.errores:
                print("  -", err)
        else:
            print("\n✅ Análisis semántico completado sin errores.")

    def mostrar_traduccion(self):
        print("\nInstrucciones traducidas:")
        for inst in self.instrucciones:
            print(f"  - {inst['resultado']} = {inst['operacion'].upper()}({inst['operando1']}, {inst['operando2']})")
        
        print("\nTUPPERS GENERADOS:")
        for t in sorted(self.tuppers):
            print("  -", t)