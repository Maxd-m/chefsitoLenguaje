
from flask import Flask, request, render_template
from analisis.lexicoChef import AnalizadorLexicoChefsito  # importa tu analizador
from analisis.analizador_sintactico_chefsito import AnalizadorSintactico2  # importa el analizador sintáctico
from analisis.analizador_semantico import AnalizadorSemantico  # importa el analizador semántico

app = Flask(__name__)

# Instancia global del analizador
# analizador = AnalizadorSintacticoChefsito("vamoss(2).csv")  # Cambia el nombre del archivo según sea necesario

@app.route('/')
def index():
    return render_template('index.html', mensaje=None)

@app.route('/compilar', methods=['POST'])
def compilar():

    #--------------------------------------------------------------- Analisis léxico
    analizador = AnalizadorLexicoChefsito("vamoss.csv")
    codigo = request.form['codigo']
    tokens, errores = analizador.procesarTexto(codigo)

    if errores:
        for error in errores:
            print(error)  
        mensaje = errores[0]  
    else:
        #----------------------------------------------------------analisis sintactico
        tipos_tokens = [t['tipo'] for t in tokens]
        sintactico = AnalizadorSintactico2(tipos_tokens)
        resultado= sintactico.analizar_programa()
        if resultado:
            return render_template('index.html', mensaje=resultado, codigo=codigo)
        else:
            # ---------------------------------------------------------Analisis semántico
            semantico = AnalizadorSemantico(tokens)
            semantico.analizar()
            if semantico.errores:
                return render_template('index.html', mensaje=semantico.errores[0], codigo=codigo)
            else:
                mensaje = "✅ Análisis completado sin errores."
                return render_template('index.html', mensaje=mensaje, codigo=codigo)


    # mensaje = "✅ Análisis léxico completado sin errores."
    return render_template('index.html', mensaje=mensaje, codigo=codigo)

if __name__ == '__main__':
    app.run(debug=True)
