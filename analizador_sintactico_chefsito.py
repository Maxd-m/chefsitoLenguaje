class AnalizadorSintactico:
    def __init__(self, lista_tokens):
        self.tokens = lista_tokens
        self.pos = 0

    def token_actual(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def consumir(self, tipo_esperado):
        actual = self.token_actual()
        if actual == tipo_esperado:
            print(f"✔ Consumido: {actual}")
            self.pos += 1
        else:
            raise SyntaxError(f"❌ Se esperaba '{tipo_esperado}' pero se encontró '{actual}' en la posición {self.pos}")

    def analizar_ingredientes(self):
        print("\n Analizando INGREDIENTES...")
        self.consumir('PALABRA_RESERVADA_INGREDIENTES')
        while self.token_actual() == 'IDENTIFICADOR':
            self.analizar_ingrediente()

    def analizar_ingrediente(self):
        print("🔹 Analizando un ingrediente")
        self.consumir('IDENTIFICADOR')
        self.consumir('CONSTANTE_NUMERICA')
        unidad = self.token_actual()
        if unidad in ['PALABRA_RESERVADA_KILOS', 'PALABRA_RESERVADA_LITROS', 'PALABRA_RESERVADA_PIEZAS']:
            self.consumir(unidad)
        else:
            raise SyntaxError(f"❌ Unidad inválida: se encontró '{unidad}' en la posición {self.pos}")
        
    def analizar_procedimiento(self):
        print("\n Analizando PROCEDIMIENTO...")
        self.consumir('PALABRA_RESERVADA_PROCEDIMIENTO')
        while self.token_actual() in (
            'PALABRA_RESERVADA_AÑADIR',
            'PALABRA_RESERVADA_SEPARAR',
            'PALABRA_RESERVADA_CORTAR',
            'PALABRA_RESERVADA_HORNEAR'
        ):
            self.analizar_instruccion()

    def analizar_instruccion(self):
        print("🔸 Analizando una instrucción")
        tipo_instr = self.token_actual()
        self.consumir(tipo_instr) 

        self.consumir('PARENTESIS_ABRE')
        self.consumir('IDENTIFICADOR')
        self.consumir('SIGNO_COMA')
        self.consumir('IDENTIFICADOR')
        self.consumir('PARENTESIS_CIERRA')

        self.consumir('PALABRA_RESERVADA_EN')
        self.consumir('PALABRA_RESERVADA_TUPPER')
        self.consumir('SIGNO_PUNTO')
        self.consumir('IDENTIFICADOR')

    def analizar_programa(self):
        print("\n Analizando estructura general del programa")
        self.consumir('PALABRA_RESERVADA_INICIO')
        self.analizar_ingredientes()
        self.analizar_procedimiento()
        self.consumir('PALABRA_RESERVADA_FIN')


if __name__ == '__main__':
    from lexicoChef import AnalizadorLexicoChefsito
    from analizador_semantico import AnalizadorSemantico

    analizador_lex = AnalizadorLexicoChefsito('vamoss.csv')
    texto = '''
    INICIO
    INGREDIENTES
    VAR1 7 PIEZAS
    VAR2 2 PIEZAS
    VAR3 5 PIEZAS
    PROCEDIMIENTO
    AÑADIR(VAR1,VAR2) EN TUPPER.SUMA
    HORNEAR(SUMA,VAR3) EN TUPPER.ULTIMO
    FIN
    '''

    tokens, errores = analizador_lex.procesarTexto(texto)
    tipos_tokens = [t['tipo'] for t in tokens]

    print("\n TOKENS:")
    print(tipos_tokens)

    print("\n INICIANDO ANÁLISIS SINTÁCTICO")
    sintactico = AnalizadorSintactico(tipos_tokens)
    sintactico.analizar_programa()

    print("\n✅ Análisis sintáctico completado sin errores.")

    print("\n🔎 INICIANDO ANÁLISIS SEMÁNTICO")
    semantico = AnalizadorSemantico(tokens)
    semantico.analizar()
