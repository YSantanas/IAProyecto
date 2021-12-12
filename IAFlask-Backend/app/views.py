from io import BytesIO
import io
from json import dumps
from os import name
from flask import render_template, Blueprint, jsonify, request, make_response, Response
import pandas as pd                 # Para la manipulación y análisis de los datos
import numpy as np                  # Para crear vectores y matrices n dimensionales
from matplotlib.figure import Figure
from apyori import apriori, dump_as_json          # Algoritmo apriori
from uuid import uuid4
import base64


from .forms import LoginForm

# practica 3
# _____________________________________
from scipy.spatial.distance import cdist    # Para el cálculo de distancias
from scipy.spatial import distance
# _____________________________________
# practica 4 y 6
# HAY QUE CARGARLO AL PROYECTO
# Para la generación de gráficas a partir de los datos
import matplotlib.pyplot as plt
import seaborn as sns             # Para la visualización de datos basado en matplotlib
# %matplotlib inline
import scipy.cluster.hierarchy as shc
from sklearn.cluster import AgglomerativeClustering
# --- practica 5 y 6
from kneed import KneeLocator
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.cluster import KMeans
from mpl_toolkits.mplot3d import Axes3D
from sklearn.metrics import pairwise_distances_argmin_min
from sklearn.preprocessing import StandardScaler, MinMaxScaler
#

# ------------------------------------------------
# _____     Practica 7 y 8     _________
# ------------------------------------------------
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, max_error, r2_score

# practica 8
from sklearn import model_selection

# ------------------------------------------------
# _____      Practica  9 y 10      _________
# ------------------------------------------------

# Se importan las bibliotecas necesarias para generar el modelo de regresión logística
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score

from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn import model_selection
from sklearn.tree import export_graphviz


from sklearn.tree import plot_tree
import graphviz
from graphviz import Source

# ------------------------------------------------
# _____            _______________       _________
# ------------------------------------------------


# blueprint permimte usar url
pagina = Blueprint('pagina', __name__)


# Error 404

@pagina.app_errorhandler(404)
# parametro obligatorio, todo error regresa dos parametros.
def pagina_no_encontrada(error):
    return render_template('errores/404.html'), 404


@pagina.route('/')
def index():
    return render_template('index.html', title='Inicio')


"""
@pagina.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm(request.form)
    if request.method =='POST':
        # se imprime los datos
        print(form.username.data)
        print(form.password.data)
        # se imprime en consola
        print("¡Una Nueva secion creada!")

    return render_template('auth/login.html', title='Login',form=form)
"""


@pagina.route('/algoritmoApriori', methods=['POST'])
def read_csv():
    if request.method == 'POST':

        flask_file = request.files['file']

        confianza = float(request.form['confianza'])
        soporte = float(request.form['soporte'])
        elevacion = float(request.form['elevacion'])
        print(confianza)
        print(soporte)
        print(elevacion)

        if not flask_file.filename.endswith('.csv'):
            return make_response(jsonify({'message': 'Seleccione un archivo CSV'}), 400)

        movies_data = pd.read_csv(flask_file, header=None)

        # Se incluyen todas las transacciones en una sola lista
        # -1 significa 'dimensión desconocida'
        transactions = movies_data.values.reshape(-1).tolist()

        # Se crea una matriz (dataframe) usando la lista y se incluye una columna 'Frecuencia'
        transaction_list = pd.DataFrame(transactions)
        transaction_list['Frecuencia'] = 1

        # Se agrupa los elementos
        transaction_list = transaction_list.groupby(by=[0], as_index=False).count(
        ).sort_values(by=['Frecuencia'], ascending=True)  # Conteo
        transaction_list['Porcentaje'] = (
            transaction_list['Frecuencia'] / transaction_list['Frecuencia'].sum())  # Porcentaje
        transaction_list = transaction_list.rename(columns={0: 'Item'})

        # Se genera un gráfico de barras
        fig = Figure()
        fig.set_size_inches(16, 20)
        ax = fig.subplots()
        ax.plot([2, 2])
        ax.barh(transaction_list['Item'],
                transaction_list['Frecuencia'], color='blue')
        ax.set_xlabel('Frecuencia')
        ax.set_ylabel('Item')
        ax.set_title('Frecuencia de los Items')
        ax.set_yticks(transaction_list['Item'])
        ax.set_yticklabels(transaction_list['Item'])
        ax.grid(True)

        nombre_temporal_uuid = str(uuid4().hex)
        nombre_temporal_png = 'app/static/img/' + nombre_temporal_uuid + '.png'

        # Se guarda el gráfico en un archivo PNG
        fig.savefig(
            fname=nombre_temporal_png, format='png')

        json_data = movies_data.head(5).to_json(orient='records')
        json_transactions = transaction_list.to_json(orient='records')

#LO QUE FALTA POR IMPRIMIR
        #Se crea una lista de listas a partir del dataframe y se remueven los 'NaN'
#level=0 especifica desde el primer índice
        MoviesLista = movies_data.stack().groupby(level=0).apply(list).tolist()

        ReglasC1 = apriori(MoviesLista, 
                   min_support=soporte, 
                   min_confidence=confianza, 
                   min_lift=elevacion)
        
        ResultadosC1 = list(ReglasC1)
#ResultadosC1
        print(len(ResultadosC1)) #Total de reglas



#________________________TEXTO_________________
        from fpdf import FPDF


        archivo= "app/static/documentos/generados/apriori.txt"
        f= open(archivo,'w')
        
        
        for item in ResultadosC1:
  #El primer índice de la lista
                Emparejar = item[0]
                items = [x for x in Emparejar]
                print("Regla: " + str(item[0]))

  #El segundo índice de la lista
                print("Soporte: " + str(item[1]))

  #El tercer índice de la lista
                print("Confianza: " + str(item[2][0][2]))
                print("Lift: " + str(item[2][0][3])) 
                print("=====================================") 
                
                cadena="Regla: " + str(item[0]) +"\n"+ "Soporte: "+ str(item[1]) +"\n"+ "Confianza: " + str(item[2][0][2]) +"\n"+ "Lift: " + str(item[2][0][3])+"\n"+"====================================="+"\n"
    #print(cadena)
                cadena=str(cadena)

                f.write(cadena)
        
        
        f.close()
          
  
# save FPDF() class into 
# a variable pdf
        pdf = FPDF()   
   
# Add a page
        pdf.add_page()
   
# Elegimos tipo de letra y tamaño
        pdf.set_font("Times", size = 11)
  
# Abrimos el archivo en modo lectura
        f = open(archivo, "r")
  
# intertamos lo abierto dentro del pdf
        for x in f:
            pdf.cell(200, 10, txt = x, ln = 1, align = 'D')
   
# Guardamos el pdf
        pdf.output("app/static/documentos/generados/apriori.pdf")   
        D = pdf.output("app/static/documentos/generados/apriori.pdf") 

#________________________TEXTOFIN_________________




        return jsonify({
            "data": json_data,
            "transactions": json_transactions,
            "graph": "static/img/practica_1.png"
        })

    return jsonify({'status': 'error', 'message': 'Error al leer el archivo'})


@pagina.route('/medidasDistancias', methods=['POST'])
def read_csv2():
    if request.method == 'POST':
        input_a = int(request.form['input_a'])
        input_b = int(request.form['input_b'])
        flask_file = request.files['file']

        if not flask_file.filename.endswith('.csv'):
            return make_response(jsonify({'message': 'Seleccione un archivo CSV'}), 400)

        archivo = pd.read_csv(flask_file)
        # print(archivo)

        # Se crea una matriz (dataframe) usando la lista.
        nuevoArchivo = pd.DataFrame(archivo)

        json_data = nuevoArchivo.to_json(orient='records')

        # _________________ENTRANDO EN PRACTICA3_________________
        # _______________________________________________________
        # -- se crea la matriz de distancia ECUCLIDIANA

        DstEuclidiana = cdist(
            archivo.iloc[0:10], archivo.iloc[0:10], metric='euclidean')
        MEuclidiana = pd.DataFrame(DstEuclidiana)
        # print(MEuclidiana)  # revisar que s emuestre en consola
        # se desea que se muestre la distancia entre dos objetos
        # esto da un valor numerico.

        tabla_euclidiana = MEuclidiana.to_json(orient='records')

        # se solicita el elemento, a comparar 1 y 2
        Objeto1 = archivo.iloc[input_a]
        Objeto2 = archivo.iloc[input_b]
        dstEuclidiana = distance.euclidean(Objeto1, Objeto2)
        # print(dstEuclidiana)  # este es el valor flotante retornado,

        dist_euclidiana = float(dstEuclidiana)

        # -- se crea la matriz de distancia para Chebyshev

        DstChebyshev = cdist(
            archivo.iloc[0:10], archivo.iloc[0:10], metric='chebyshev')
        MChebyshev = pd.DataFrame(DstChebyshev)
        # print(MChebyshev)

        tabla_chebyshev = MChebyshev.to_json(orient='records')

        # nuevamente se desea conocer la distancia entre dos objetos, seleccionados
        # por el usuario.
        # se solicita el elemento, a comparar 1 y 2
        Objeto1 = archivo.iloc[input_a]
        Objeto2 = archivo.iloc[input_b]
        dstChebyshev = distance.chebyshev(Objeto1, Objeto2)
        # print(dstChebyshev)  # valor numerico retornado

        dist_chebyshev = float(dstChebyshev)

        # -- se crea la matriz de distancia para Manhattan

        DstManhattan = cdist(
            archivo.iloc[0:10], archivo.iloc[0:10], metric='cityblock')
        MManhattan = pd.DataFrame(DstManhattan)
        # print(MManhattan)

        tabla_manhattan = MManhattan.to_json(orient='records')

        # nuevamente se desea conocer la distancia entre dos objetos, seleccionados
        # por el usuario.

        Objeto1 = archivo.iloc[input_a]
        # se solicita el elemento, a comparar 1 y 2
        Objeto2 = archivo.iloc[input_b]
        dstManhattan = distance.cityblock(Objeto1, Objeto2)
        # print(dstManhattan)

        dist_manhattan = float(dstManhattan)

        # -- se crea la matriz de distancia para Minkowski

        DstMinkowski = cdist(
            archivo.iloc[0:10], archivo.iloc[0:10], metric='minkowski', p=1.5)
        MMinkowski = pd.DataFrame(DstMinkowski)
        # print(MMinkowski)

        tabla_minkowski = MMinkowski.to_json(orient='records')

        # nuevamente se desea conocer la distancia entre dos objetos, seleccionados
        # por el usuario.

        Objeto1 = archivo.iloc[input_a]
        # se solicita el elemento, a comparar 1 y 2
        Objeto2 = archivo.iloc[input_b]
        dstMinkowski = distance.minkowski(Objeto1, Objeto2, p=1.5)
        # print(dstMinkowski)

        dist_minkowski = float(dstMinkowski)

        return jsonify({
            "data": json_data,
            "data_euclidiana": tabla_euclidiana,
            "data_chebyshev": tabla_chebyshev,
            "data_manhattan": tabla_manhattan,
            "data_minkowski": tabla_minkowski,
            "dist_euclidiana": dist_euclidiana,
            "dist_chebyshev": dist_chebyshev,
            "dist_manhattan": dist_manhattan,
            "dist_minkowski": dist_minkowski
        })

    return jsonify({'status': 'error', 'message': 'Error al leer el archivo'})


# _________________________________________
# _____________Practica 4__________________
# _________________________________________
@pagina.route('/clusterJerarquico', methods=['POST'])
def read_csv3():

    if request.method == 'POST':

        VariableEval = request.form['variableEval']
        NumClusterJ = int(request.form['numCluster'])
        flask_file = request.files['file']

        if not flask_file.filename.endswith('.csv'):
            return make_response(jsonify({'message': 'Seleccione un archivo CSV'}), 400)

        Hipoteca = pd.read_csv(flask_file)

        print(Hipoteca)

        print(Hipoteca.groupby(VariableEval).size())

        data_table_1 = pd.DataFrame(Hipoteca)

        json_data_1 = data_table_1.head(10).to_json(orient='records')

# _________________________________________

# ___________________________GRAFICA DE CALOR________________________________

# # **2) Selección de características**


        CorrHipoteca = Hipoteca.corr(method='pearson')
        CorrHipoteca

#     print(CorrHipoteca['ingresos'].sort_values(
#         ascending=False)[:10], '\n')  # Top 10 valores
#
        plt.figure(figsize=(14, 7))
        MatrizInf = np.triu(CorrHipoteca)
        sns.heatmap(CorrHipoteca, cmap='RdBu_r', annot=True, mask=MatrizInf)
#     plt.show()
        buffer= BytesIO()
        
        
        nombre_temporal_uuid00 = str(uuid4().hex)
        nombre_temporal_png00 = 'app/static/img/' + nombre_temporal_uuid00 + '.png'

        # Replace "app" to ""
        calor = nombre_temporal_png00.replace('app/', '')
        

        plt.savefig(
            fname=nombre_temporal_png00,
            format='png',
        )
        buffer.close()
        


# ___________________________GRAFICA DE CLUSTER________________________________

        MatrizHipoteca = np.array(Hipoteca[['ingresos', 'gastos_comunes', 'pago_coche',
                        'gastos_otros', 'ahorros', 'vivienda', 'estado_civil', 'hijos', 'trabajo']])
#     pd.DataFrame(MatrizHipoteca)
# # MatrizHipoteca = Hipoteca.iloc[:, 0:9].values     #iloc para seleccionar filas y columnas según su posición

# # **3) Aplicación del algoritmo**

#     from sklearn.preprocessing import StandardScaler, MinMaxScaler
#     # Se instancia el objeto StandardScaler o MinMaxScaler
        estandarizar = StandardScaler()
#     # Se calculan la media y desviación y se escalan los datos
        MEstandarizada = estandarizar.fit_transform(MatrizHipoteca)

#     pd.DataFrame(MEstandarizada)

# # Se importan las bibliotecas de clustering jerárquico para crear el árbol

        plt.figure(figsize=(10, 7))
        plt.title("Casos de hipoteca")
        plt.xlabel('Hipoteca')
        plt.ylabel('Distancia')
        Arbol = shc.dendrogram(shc.linkage(
                MEstandarizada, method='complete', metric='euclidean'))
# #plt.axhline(y=5.4, color='orange', linestyle='--')
# # Probar con otras medciones de distancia (euclidean, chebyshev, cityblock)
        buffer= BytesIO()
        
        nombre_temporal_uuid001 = str(uuid4().hex)
        nombre_temporal_png001 = 'app/static/img/' + nombre_temporal_uuid001 + '.png'

        # Replace "app" to ""
        new_name001 = nombre_temporal_png001.replace('app/', '')
        

        plt.savefig(
            fname=nombre_temporal_png001,
            format='png',
        )
        buffer.close()
        
# __________________________________________
# ___________________________GRAFICA DE DISPERSION 1________________________________

        # Se genera un gráfico de dispersión
        fig = Figure()
        fig.set_size_inches(4, 4)
        ax = fig.add_subplot(111)
        # sns.scatterplot(x='ahorros', y='ingresos',
        #                 data=Hipoteca, hue='comprar')

        ax.scatter(Hipoteca['ahorros'], Hipoteca['ingresos'],
                   c=Hipoteca[VariableEval])
        ax.set_title('Grafico de dispersión')
        ax.set_xlabel('Ahorros')
        ax.set_ylabel('Ingresos')

        nombre_temporal_uuid = str(uuid4().hex)
        nombre_temporal_png = 'app/static/img/' + nombre_temporal_uuid + '.png'

        # Replace "app" to ""
        new_name = nombre_temporal_png.replace('app/', '')

        # Se guarda el gráfico en un archivo PNG
        fig.savefig(
            fname=nombre_temporal_png,
            format='png',
        )



# __________________________________________
# ___________________________GRAFICA DE FINAL ________________________________


# # Se crean las etiquetas de los elementos en los clústeres
        MJerarquico = AgglomerativeClustering(
                 n_clusters=NumClusterJ, linkage='complete', affinity='euclidean')
        MJerarquico.fit_predict(MEstandarizada)
        #MJerarquico.labels_

        Hipoteca = Hipoteca.drop(columns=[VariableEval])
        Hipoteca['clusterH'] = MJerarquico.labels_
#     Hipoteca  IMPRIMIR CON CLUSTERH

# # Cantidad de elementos en los clusters
        Hipoteca.groupby(['clusterH'])['clusterH'].count()

#     Hipoteca[Hipoteca.clusterH == 6]  impirmir los clusrter del 6

        CentroidesH = Hipoteca.groupby('clusterH').mean()
#     CentroidesH

        plt.figure(figsize=(10, 7))
        plt.scatter(MEstandarizada[:, 0],
                         MEstandarizada[:, 1], c=MJerarquico.labels_)
        #plt.grid()
        #plt.show()
        
        buffer3= BytesIO()
        
        
        nombre_temporal_uuid003 = str(uuid4().hex)
        nombre_temporal_png003 = 'app/static/img/' + nombre_temporal_uuid003 + '.png'

        # Replace "app" to ""
        imgfinal = nombre_temporal_png003.replace('app/', '')
        

        plt.savefig(
            fname=nombre_temporal_png003,
            format='png',
        )
        buffer3.close()


        # Retorna imagen en base64
        return jsonify({'status': 'success', 'data': json_data_1, 'image': new_name,'image2': new_name001,'image3': calor,'imageFinal': imgfinal})

    return jsonify({'status': 'error', 'message': 'Error al leer el archivo'})



# # _________________________________________
# # _____________Practica 5__________________
# # _________________________________________
# # COMENTARIO PARA CENTRARSE EN UNA PRACTICA


# """

@pagina.route('/clusterParticional', methods=['POST'])
def read_csv4():

    if request.method == 'POST':
        VariableEvalP = request.form['variableEvalP']

        NumClusterP = int(request.form['numClusterP'])
        flask_file = request.files['file']

        if not flask_file.filename.endswith('.csv'):
            return make_response(jsonify({'message': 'Seleccione un archivo CSV'}), 400)

        Hipoteca = pd.read_csv(flask_file)

        print(Hipoteca)

        print(Hipoteca.groupby(VariableEvalP).size())

        data_table_3 = pd.DataFrame(Hipoteca)
        json_data3 = data_table_3.head(10).to_json(orient='records')



#GRAFICAS_________________________________-


# #### **2) Selección de características**

        sns.pairplot(Hipoteca, hue=VariableEvalP)
        
        buffer3= BytesIO()
        
        
        nombre_temporal_inicio = str(uuid4().hex)
        nombre_temporal_pngini = 'app/static/img/' + nombre_temporal_inicio + '.png'

        # Replace "app" to ""
        imginicio = nombre_temporal_pngini.replace('app/', '')
        
        plt.savefig(
            fname=nombre_temporal_pngini,
            format='png',
        )
        buffer3.close()

#__________________GRAFICA2_________________________________-

        # Se genera un gráfico de dispersión
        fig = Figure()
        fig.set_size_inches(4, 4)
        ax = fig.add_subplot(111)
        # sns.scatterplot(x='ahorros', y='ingresos',
        #                 data=Hipoteca, hue='comprar')

        ax.scatter(Hipoteca['ahorros'], Hipoteca['ingresos'],
                   c=Hipoteca[VariableEvalP])
        ax.set_title('Grafico de dispersión')
        ax.set_xlabel('Ahorros')
        ax.set_ylabel('Ingresos')

        nombre_temporal_disper = str(uuid4().hex)
        nombre_temporal_pngdis = 'app/static/img/' + nombre_temporal_disper + '.png'

        # Replace "app" to ""
        imgdisp = nombre_temporal_pngdis.replace('app/', '')

        # Se guarda el gráfico en un archivo PNG
        fig.savefig(
            fname=nombre_temporal_pngdis,
            format='png',
        )




#__________________GRAFICA3 MAPA CALOR_________________________________-

        CorrHipoteca = Hipoteca.corr(method='pearson')
#     CorrHipoteca

        plt.figure(figsize=(14,7))
        MatrizInf = np.triu(CorrHipoteca)
        sns.heatmap(CorrHipoteca, cmap='RdBu_r', annot=True, mask=MatrizInf)

        buffer5= BytesIO()
        
        
        nombre_temporal_uuid003 = str(uuid4().hex)
        nombre_temporal_png003 = 'app/static/img/' + nombre_temporal_uuid003 + '.png'

        # Replace "app" to ""
        calor = nombre_temporal_png003.replace('app/', '')
        

        plt.savefig(
            fname=nombre_temporal_png003,
            format='png',
        )
        buffer5.close()

        MatrizHipoteca = np.array(Hipoteca[['ingresos', 'gastos_comunes', 'pago_coche', 'gastos_otros', 'ahorros', 'vivienda', 'estado_civil', 'hijos', 'trabajo']])
#     pd.DataFrame(MatrizHipoteca)  ---imprimir tabla
# #MatrizHipoteca = Hipoteca.iloc[:, 0:9].values     #iloc para seleccionar filas y columnas según su posición


#__________________GRAFICA3 CURVA_________________________________-
# #### **3) Aplicación del algoritmo**


        estandarizar = StandardScaler()                               # Se instancia el objeto StandardScaler o MinMaxScaler
        MEstandarizada = estandarizar.fit_transform(MatrizHipoteca)   # Se calculan la media y desviación y se escalan los datos

#     pd.DataFrame(MEstandarizada)  ---imprimir tabla


# #Definición de k clusters para K-means
# #Se utiliza random_state para inicializar el generador interno de números aleatorios
        SSE = []
        for i in range(2, 12):
            km = KMeans(n_clusters=i, random_state=0)
            km.fit(MEstandarizada)
            SSE.append(km.inertia_)

# #Se grafica SSE en función de k
        plt.figure(figsize=(10, 7))
        plt.plot(range(2, 12), SSE, marker='o')
        plt.xlabel('Cantidad de clusters *k*')
        plt.ylabel('SSE')
        plt.title('Elbow Method')
#     plt.show()

        buffer5= BytesIO()
        
        
        nombre_temporal_uuid004 = str(uuid4().hex)
        nombre_temporal_png004 = 'app/static/img/' + nombre_temporal_uuid004 + '.png'

        # Replace "app" to ""
        grafCurva = nombre_temporal_png004.replace('app/', '')
        

        plt.savefig(
            fname=nombre_temporal_png004,
            format='png',
        )
        buffer5.close()


# # !pip install kneed

#__________________GRAFICA3 CURVA2_________________________________

        kl = KneeLocator(range(2, 12), SSE, curve="convex", direction="decreasing")
#     kl.elbow

        plt.style.use('ggplot')
        kl.plot_knee()
        buffer6= BytesIO()
        
        
        nombre_temporal_uuid005 = str(uuid4().hex)
        nombre_temporal_png005 = 'app/static/img/' + nombre_temporal_uuid005 + '.png'

        # Replace "app" to ""
        grafCurva2 = nombre_temporal_png005.replace('app/', '')
        

        plt.savefig(
            fname=nombre_temporal_png005,
            format='png',
        )
        buffer5.close()



# #Se crean las etiquetas de los elementos en los clusters
        MParticional = KMeans(n_clusters=NumClusterP, random_state=0).fit(MEstandarizada)
        MParticional.predict(MEstandarizada)
#     MParticional.labels_

        Hipoteca = Hipoteca.drop(columns=[VariableEvalP])
        Hipoteca['clusterP'] = MParticional.labels_
#     Hipoteca

# #Cantidad de elementos en los clusters
        Hipoteca.groupby(['clusterP'])['clusterP'].count()

        Hipoteca[Hipoteca.clusterP == 0]

# #Obtención de los centroides
        CentroidesP = Hipoteca.groupby('clusterP').mean()
        #CentroidesP
        
        tabla2= pd.DataFrame(CentroidesP)
        #imprime la ultima tabla
        json_data2 = tabla2.head(10).to_json(orient='records')


# # Gráfica de los elementos y los centros de los clusters

#     plt.rcParams['figure.figsize'] = (10, 7)
#     plt.style.use('ggplot')
#     colores=['red', 'blue', 'green', 'yellow']
#     asignar=[]
#     for row in MParticional.labels_:
#         asignar.append(colores[row])

#     fig = plt.figure()
#     ax = Axes3D(fig)
#     ax.scatter(MEstandarizada[:, 0],
#             MEstandarizada[:, 1],
#             MEstandarizada[:, 2], marker='o', c=asignar, s=60)
#     ax.scatter(MParticional.cluster_centers_[:, 0],
#             MParticional.cluster_centers_[:, 1],
#             MParticional.cluster_centers_[:, 2], marker='o', c=colores, s=1000)
#     plt.show()

        # Retorna imagen en base64
        return jsonify({'status': 'success', 'data': json_data3, 'graph': imginicio, 'graph2': imgdisp,'graph3': calor})

    return jsonify({'status': 'error', 'message': 'Error al leer el archivo'})


# #_________________________________________
# #_____________Practica 7__________________
# #_________________________________________


@pagina.route('/regresionLineal', methods=['POST'])
def read_csv5():

    if request.method == 'POST':
        #====================================================================
        Profundidad1 = float(request.form['profundidad1'])
        R1a = float(request.form['r1'])
        R2a = float(request.form['r2'])
        R3a = float(request.form['r3'])
        
        print(Profundidad1)
        print(R1a)
        print(R2a)
        print(R3a)
        #====================================================================
        
        flask_file = request.files['file']
        


        if not flask_file.filename.endswith('.csv'):
            return make_response(jsonify({'message': 'Seleccione un archivo CSV'}), 400)

        RGeofisicos = pd.read_csv(flask_file)
        print(RGeofisicos)

        data_table_4 = pd.DataFrame(RGeofisicos)
        json_data4 = data_table_4.head(10).to_json(orient='records')

# ___________________________GRAFICA1________________________________

        # Se genera un gráfico
        fig = Figure()
        fig.set_size_inches(20, 5)
        ax = fig.subplots()
        ax.plot(RGeofisicos['Profundidad'], RGeofisicos['RC2'],
                color='purple', marker='o', label='RC2')
        ax.plot(RGeofisicos['Profundidad'], RGeofisicos['RC2'],
                color='purple', marker='o', label='RC2')
        ax.plot(RGeofisicos['Profundidad'], RGeofisicos['RC3'],
                color='blue', marker='o', label='RC3')
        ax.plot(RGeofisicos['Profundidad'], RGeofisicos['RC4'],
                color='yellow', marker='o', label='RC4')
        ax.set_xlabel('Profundidad')
        ax.set_ylabel('Porcentaje')
        ax.set_title('Registros_geofsicos convencionales')
        ax.grid(True)
        ax.legend()

        nombre_temporal_uuid = str(uuid4().hex)
        nombre_temporal_png = 'app/static/img/' + nombre_temporal_uuid + '.png'

        # Replace "app" to ""
        new_name2 = nombre_temporal_png.replace('app/', '')

        # Se guarda el gráfico en un archivo PNG
        fig.savefig(
            fname=nombre_temporal_png,
            format='png',
        )


# #### **3) Aplicación del algoritmo**


# #Se seleccionan las variables predictoras (X) y la variable a pronosticar (Y)

        X_train = np.array(RGeofisicos[['Profundidad', 'RC1', 'RC2', 'RC3']])
        Xpronostic = pd.DataFrame(X_train)

        Y_train = np.array(RGeofisicos[['RC4']])
        ypronostic = pd.DataFrame(Y_train)

# #Se entrena el modelo a través de una Regresión Lineal Múltiple

        RLMultiple = linear_model.LinearRegression()
        RLMultiple.fit(X_train, Y_train)  # Se entrena el modelo


# #Se genera el pronóstico
        Y_pronostico = RLMultiple.predict(X_train)
        Ypronostic = pd.DataFrame(Y_pronostico)
        RGeofisicos1 = RGeofisicos

        RGeofisicos1['Pronostico'] = Y_pronostico

# AQUI TABLA DONDE SE ANEXA LA COLUMNA PRONOSTICO

        data_table_5 = pd.DataFrame(RGeofisicos1)
        json_data5 = data_table_5.head(10).to_json(orient='records')


# #### **4) Obtención de los coeficientes, intercepto, error y Score**


#     print('Coeficientes: \n', RLMultiple.coef_)
#     print('Intercepto: \n', RLMultiple.intercept_)
#     print("Residuo: %.4f" % max_error(Y_train, Y_pronostico))
#     print("MSE: %.4f" % mean_squared_error(Y_train, Y_pronostico))
#     print("RMSE: %.4f" % mean_squared_error(Y_train, Y_pronostico, squared=False))  #True devuelve MSE, False devuelve RMSE
#     print('Score (Bondad de ajuste): %.4f' % r2_score(Y_train, Y_pronostico))


# #### **6) Proyección de los valores reales y pronosticados**

# ___________________________GRAFICA2________________________________

        # Se genera un gráfico
        fig = Figure()
        fig.set_size_inches(20, 5)
        ax = fig.subplots()
        ax.plot(RGeofisicos['Profundidad'], RGeofisicos['RC1'],
                color='green', marker='o', label='RC1')
        ax.plot(RGeofisicos['Profundidad'], RGeofisicos['RC2'],
                color='purple', marker='o', label='RC2')
        ax.plot(RGeofisicos['Profundidad'], RGeofisicos['RC3'],
                color='blue', marker='o', label='RC3')
        ax.plot(RGeofisicos['Profundidad'], RGeofisicos['RC4'],
                color='yellow', marker='o', label='RC4')
        ax.set_xlabel('Profundidad')
        ax.set_ylabel('Porcentaje')
        ax.set_title('Registros_geofsicos convencionales')
        ax.grid(True)
        ax.legend()

        nombre_temporal_uuid2 = str(uuid4().hex)
        nombre_temporal_png2 = 'app/static/img/' + nombre_temporal_uuid2 + '.png'

        # Replace "app" to ""
        new_name3 = nombre_temporal_png2.replace('app/', '')

        # Se guarda el gráfico en un archivo PNG
        fig.savefig(
            fname=nombre_temporal_png2,
            format='png',
        )


# ___________________________GRAFICA3________________________________

        # Se genera un gráfico
        fig = Figure()
        fig.set_size_inches(20, 5)
        ax = fig.subplots()
        ax.plot(RGeofisicos['Profundidad'], Y_pronostico,
                color='red', marker='o', label='Pronóstico')
        ax.set_xlabel('Profundidad')
        ax.set_ylabel('Porcentaje')
        ax.set_title('Registros_geofsicos convencionales')
        ax.grid(True)
        ax.legend()

        nombre_temporal_uuid3 = str(uuid4().hex)
        nombre_temporal_png3 = 'app/static/img/' + nombre_temporal_uuid3 + '.png'

        # Replace "app" to ""
        new_name4 = nombre_temporal_png3.replace('app/', '')

        # Se guarda el gráfico en un archivo PNG
        fig.savefig(
            fname=nombre_temporal_png3,
            format='png',
        )


# #### **7) Nuevos pronósticos**


        ROS = pd.DataFrame({'Profundidad': [Profundidad1], 'RC1': [R1a], 'RC2': [R2a], 'RC3': [R3a]})
        resultado= "".join(map(str, RLMultiple.predict(ROS)))
        print(resultado)

        # Retorna imagen en base64
        return jsonify({'status': 'success', 'data': json_data4, 'data2': json_data5, 'graph': new_name2, 'graph2': new_name3, 'graph3': new_name4,'newpronostico':resultado})

    return jsonify({'status': 'error', 'message': 'Error al leer el archivo'})





# #_________________________________________
# #_____________Practica 9__________________
# #_________________________________________



@pagina.route('/clasificacionRegresionLogistica', methods=['POST'])
def read_csv9():

  if request.method == 'POST':
        VariableEvalCRL = request.form['variableEvalCRL']
        PorcentajeCRL = float(request.form['porcentajeCRL'])

# para nuevos pronosticos

        TexturaCRL = float(request.form['Texture'])  
        PerimetroCRL = float(request.form['Perimeter']) 
        SuavidadCRL=float(request.form['Smoothness'])
        CompacidadCRL=float(request.form['Compactness'])  
        SimetriaCRL= float(request.form['Symmetry'])  
        DimensionFCRL= float(request.form['FractalDimension'])

        flask_file = request.files['file']

        if not flask_file.filename.endswith('.csv'):
            return make_response(jsonify({'message': 'Seleccione un archivo CSV'}), 400)

        BCancer = pd.read_csv(flask_file)

        datos_tabla9 = pd.DataFrame(BCancer)
        json_tabla9 = datos_tabla9.head(10).to_json(orient='records')


# ___________________________GRAFICA1________________________________



# #### **2) Selección de características** MAPA DE CALOR

        sns.pairplot(BCancer, hue=VariableEvalCRL)
        #plt.show()


        buffer1= BytesIO()
        
        
        nombre_temporal_uuid001 = str(uuid4().hex)
        nombre_temporal_png001 = 'app/static/img/' + nombre_temporal_uuid001 + '.png'

        # Replace "app" to ""
        grafica1 = nombre_temporal_png001.replace('app/', '')
        

        plt.savefig(
            fname=nombre_temporal_png001,
            format='png',
        )
        buffer1.close()


# ___________________________GRAFICA2________________________________


  # Se genera un gráfico de dispersión
#plt.plot(BCancer['Radius'], BCancer['Perimeter'], 'b+')

        fig, ax = plt.subplots(figsize=(10, 6))
        
        ax.scatter(x = BCancer['Radius'], y = BCancer['Perimeter'], color = "orange", edgecolors = "blue", linewidths = 0.1, alpha = 0.7)
        plt.title('Gráfico de dispersión')
        plt.xlabel('Radius')
        plt.ylabel('Perimeter')

        nombre_temporal_uuid002 = str(uuid4().hex)
        nombre_temporal_png002 = 'app/static/img/' + nombre_temporal_uuid002 + '.png'

        # Replace "app" to ""
        grafica2 = nombre_temporal_png002.replace('app/', '')
        

        plt.savefig(
            fname=nombre_temporal_png002,
            format='png',
        )


#___________________________Tabla2_______________________


        CorrBCancer = BCancer.corr(method='pearson')
  

        datos_tabla9_2 = pd.DataFrame(CorrBCancer)
        json_tabla9_2 = datos_tabla9_2.head(10).to_json(orient='records')
        
#__________________________FIN tabla2 _______________________________

#__________________________MAPA DE CALOR _______________________________

        plt.figure(figsize=(14,7))
        MatrizInf = np.triu(BCancer.corr())
        sns.heatmap(BCancer.corr(), cmap='RdBu_r', annot=True, mask=MatrizInf)

        buffer3= BytesIO()
        
        
        nombre_temporal_uuid003 = str(uuid4().hex)
        nombre_temporal_png003 = 'app/static/img/' + nombre_temporal_uuid003 + '.png'

        # Replace "app" to ""
        calor = nombre_temporal_png003.replace('app/', '')
        

        plt.savefig(
            fname=nombre_temporal_png003,
            format='png',
        )
        buffer3.close()

#__________________________FIN MAPA DE CALOR _______________________________

#______________3) Definición de variables predictoras y variable clase

        BCancer = BCancer.replace({'M': 0, 'B': 1})
        
        #Variables predictoras
        X = np.array(BCancer[['Texture', 'Area', 'Smoothness', 'Compactness', 'Symmetry', 'FractalDimension']])
#X = BCancer.iloc[:, [3, 5, 6, 7, 10, 11]].values  #iloc para seleccionar filas y columnas según su posición



#___________________________Tabla3_______________________


        CorrBCancer = BCancer.corr(method='pearson')
  #Variables predictoras
        X = np.array(BCancer[['Texture', 'Area', 'Smoothness', 'Compactness', 'Symmetry', 'FractalDimension']])
#X = BCancer.iloc[:, [3, 5, 6, 7, 10, 11]].values  #iloc para seleccionar filas y columnas según su posición



        datos_tabla9_3 = pd.DataFrame(X)
        json_tabla9_3 = datos_tabla9_3.head(10).to_json(orient='records')
#___________________________Tabla4_______________________
#Variable clase
        Y = np.array(BCancer[[VariableEvalCRL]])


        datos_tabla9_4 = pd.DataFrame(Y)
        
        json_tabla9_4 = datos_tabla9_4.head(10).to_json(orient='records')
        
        
# ___________________________GRAFICA4________________________________
        
        plt.figure(figsize=(10, 7))
        plt.scatter(X[:,0], X[:,1], c = BCancer.Diagnosis)
        plt.grid()
        plt.xlabel('Texture')
        plt.ylabel('Area')
        
        buffer4= BytesIO()
        
        
        nombre_temporal_uuid004 = str(uuid4().hex)
        nombre_temporal_png004 = 'app/static/img/' + nombre_temporal_uuid004 + '.png'

        # Replace "app" to ""
        grafica4 = nombre_temporal_png004.replace('app/', '')
        

        plt.savefig(
            fname=nombre_temporal_png004,
            format='png',
        )
        buffer4.close()
        
        
        
#Aplicación del algoritmo
#Regresión logística

#___________________________Tabla5 y 6_______________________



        X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(X, Y, 
                                                                                test_size = PorcentajeCRL, 
                                                                                random_state = 1234,
                                                                                shuffle = True)
        
        
        
        datos_tabla9_5 = pd.DataFrame(X_train)
        
        json_tabla9_5 = datos_tabla9_5.head(10).to_json(orient='records')
        
        
        datos_tabla9_6 = pd.DataFrame(Y_train)
        
        json_tabla9_6 = datos_tabla9_6.head(10).to_json(orient='records')
        
#___________________________FIN Tabla5 y 6_______________________

        #Se entrena el modelo a partir de los datos de entrada
        Clasificacion = linear_model.LogisticRegression()
        Clasificacion.fit(X_train, Y_train)
        
#___________________________Tabla7 y 8_______________________

        #Predicciones probabilísticas de los datos de prueba
        Probabilidad = Clasificacion.predict_proba(X_validation)
        
        datos_tabla9_7 = pd.DataFrame(Probabilidad)
        
        json_tabla9_7 = datos_tabla9_7.head(10).to_json(orient='records')
        
        
        Predicciones = Clasificacion.predict(X_validation)
        
        datos_tabla9_8 = pd.DataFrame(Predicciones)
        
        json_tabla9_8 = datos_tabla9_8.head(10).to_json(orient='records')
        
        #Se calcula el exactitud promedio de la validación
        #Clasificacion.score(),X_validation, Y_validation
        
        
#___________________________Tabla9_______________________
        #Matriz de clasificación
        Y_Clasificacion = Clasificacion.predict(X_validation)
        Matriz_Clasificacion = pd.crosstab(Y_validation.ravel(), 
                                   Y_Clasificacion, 
                                   rownames=['Real'], 
                                   colnames=['Clasificación']) 
        
        datos_tabla9_9 = pd.DataFrame(Matriz_Clasificacion)
        
        json_tabla9_9 = datos_tabla9_9.head(10).to_json(orient='records')
        
#___________Ecuación del modelo de clasificación

#Paciente saber si esta M y B
        PacienteID1 = pd.DataFrame({'Texture': [TexturaCRL], 
                            'Area': [PerimetroCRL], 
                            'Smoothness': [SuavidadCRL], 
                            'Compactness': [CompacidadCRL], 
                            'Symmetry': [SimetriaCRL], 
                            'FractalDimension': [DimensionFCRL]})

        
        resultadoCRL= "".join(map(str, Clasificacion.predict(PacienteID1)))
        print(resultadoCRL)
        
        # Retorna 
        return jsonify({'status': 'success', 'data': json_tabla9, 'data2': json_tabla9_2,'data3': json_tabla9_3,
                        'data4': json_tabla9_4, 'data5': json_tabla9_5,'data6': json_tabla9_6,'data7': json_tabla9_7,
                        'data8': json_tabla9_8,'data9': json_tabla9_9,
                        'graph':grafica1,'graph2':grafica2, 'imgcalor': calor,'graph4':grafica4, 'newpronostico2':resultadoCRL})

  return jsonify({'status': 'error', 'message': 'Error al leer el archivo'})
# #_________________________________________
# #_____________Practica 11__________________
# #_____________MEDICO______________________
# #_________________________________________


@pagina.route('/pronosticoArbol', methods=['POST'])
def read_csv6():
    if request.method == 'POST':
        
        flask_file = request.files['file']
        
        Textura = float(request.form['Texture'])
        
        Perimetro = float(request.form['Perimeter'])
        
        Suavidad=float(request.form['Smoothness'])
        
        Compacidad=float(request.form['Compactness'])
        
        Simetria= float(request.form['Symmetry'])
        
        DimensionF= float(request.form['FractalDimension'])
        #return make_response(jsonify({'message': 'ERROR YA MATATE'}), 200)


        
        if not flask_file.filename.endswith('.csv'):
            return make_response(jsonify({'message': 'Seleccione un archivo CSV'}), 400)

        BCancer = pd.read_csv(flask_file)

        data_table_11 = pd.DataFrame(BCancer)
        json_data11 = data_table_11.head(10).to_json(orient='records')


# ___________________________GRAFICA1________________________________


# **2) Gráfica del área del tumor por paciente**

        # Se genera un gráfico
        fig = Figure()
        fig.set_size_inches(20, 5)
        ax = fig.subplots()
        ax.plot(BCancer['IDNumber'], BCancer['Area'],
                color='green', marker='o', label='Area')
        ax.set_xlabel('Paciente')
        ax.set_ylabel('Tamaño del tumor')
        ax.set_title('Pacientes con tumores cancerígenos')
        ax.grid(True)
        ax.legend()

        nombre_temporal_uuid11 = str(uuid4().hex)
        nombre_temporal_png11 = 'app/static/img/' + nombre_temporal_uuid11 + '.png'

        # Replace "app" to ""
        new_name11 = nombre_temporal_png11.replace('app/', '')

     # Se guarda el gráfico en un archivo PNG
        fig.savefig(
            fname=nombre_temporal_png11,
            format='png',
        )


# #### **3) Selección de características** MAPA DE CALOR

        plt.figure(figsize=(14,7))
        MatrizInf = np.triu(BCancer.corr())
        sns.heatmap(BCancer.corr(), cmap='RdBu_r', annot=True, mask=MatrizInf)
        #plt.show()


        buffer3= BytesIO()
        
        
        nombre_temporal_uuid003 = str(uuid4().hex)
        nombre_temporal_png003 = 'app/static/img/' + nombre_temporal_uuid003 + '.png'

        # Replace "app" to ""
        calor = nombre_temporal_png003.replace('app/', '')
        

        plt.savefig(
            fname=nombre_temporal_png003,
            format='png',
        )
        buffer3.close()

# #### **4) Aplicación del algoritmo**


#Se seleccionan las variables predictoras (X) y la variable a pronosticar (Y)

        X = np.array(BCancer[['Texture',
                              'Perimeter',
                              'Smoothness',
                              'Compactness',
                              'Symmetry',
                              'FractalDimension']])
        tabla2= pd.DataFrame(X)
        
        json_data12 = tabla2.head(10).to_json(orient='records')
        
# #X = np.array(BCancer[['Radius', 'Texture', 'Perimeter', 'Smoothness', 'Compactness',	'Concavity', 'ConcavePoints', 'Symmetry',	'FractalDimension']
# #pd.DataFrame(X)

        Y = np.array(BCancer[['Area']])


 #Se hace la división de los datos

        X_train, X_test, Y_train, Y_test = model_selection.train_test_split(X, Y,
                                                                             test_size = 0.2,
                                                                              random_state = 1234,
                                                                              shuffle = True)


#DATOS QUE SE PIDEN EN INPUT  -------------->>>>>
# pd.DataFrame(X_train)
# #pd.DataFrame(X_test)

# pd.DataFrame(Y_train)
# #pd.DataFrame(Y_test)

# #Se entrena el modelo a través de un Árbol de Decisión (Regresión)

        PronosticoAD = DecisionTreeRegressor()
        PronosticoAD.fit(X_train, Y_train)

# #PronosticoAD = DecisionTreeRegressor(max_depth=8, min_samples_split=4, min_samples_leaf=2)
# #PronosticoAD.fit(X_train, Y_train)


 #Se genera el pronóstico
        Y_Pronostico = PronosticoAD.predict(X_test)
# pd.DataFrame(Y_Pronostico)

        Valores = pd.DataFrame(Y_test, Y_Pronostico)
# Valores


# ___________________________GRAFICA2________________________________


# **2) Gráfica del área del tumor por paciente**

        # Se genera un gráfico
        fig = Figure()
        fig.set_size_inches(20, 5)
        ax = fig.subplots()
        ax.plot(Y_test, color='green', marker='o', label='Y_test')
        ax.plot(Y_Pronostico, color='red', marker='o', label='Y_Pronostico')
        ax.set_xlabel('Paciente')
        ax.set_ylabel('Tamaño del tumor')
        ax.set_title('Pacientes con tumores cancerígenos')
        ax.grid(True)
        ax.legend()

        nombre_temporal_uuid12 = str(uuid4().hex)
        nombre_temporal_png12 = 'app/static/img/' + nombre_temporal_uuid12 + '.png'

        # Replace "app" to ""
        imgroja = nombre_temporal_png12.replace('app/', '')

     # Se guarda el gráfico en un archivo PNG
        fig.savefig(
            fname=nombre_temporal_png12,
            format='png',
        )





        r2_score(Y_test, Y_Pronostico)

# #### **5) Obtención de los parámetros del modelo**

# print('Criterio: \n', PronosticoAD.criterion)
# print('Importancia variables: \n', PronosticoAD.feature_importances_)
# print("MAE: %.4f" % mean_absolute_error(Y_test, Y_Pronostico))
# print("MSE: %.4f" % mean_squared_error(Y_test, Y_Pronostico))
# print("RMSE: %.4f" % mean_squared_error(Y_test, Y_Pronostico, squared=False))   #True devuelve MSE, False devuelve RMSE
# print('Score: %.4f' % r2_score(Y_test, Y_Pronostico))

        Importancia = pd.DataFrame({'Variable': list(BCancer[['Texture', 'Perimeter', 'Smoothness',
                                                             'Compactness', 'Symmetry', 'FractalDimension']]),
                                                             'Importancia': PronosticoAD.feature_importances_}).sort_values('Importancia', ascending=False)
# Importancia
        tabla3= pd.DataFrame(Importancia)
        
        json_data13 = tabla3.head(10).to_json(orient='records')
# #### **6) Conformación del modelo de pronóstico**


# #!pip install graphviz

# #import graphviz
# #


 # Se crea un objeto para visualizar el árbol
  # Se incluyen los nombres de las variables para imprimirlos en el árbol



        Elementos = export_graphviz(PronosticoAD, feature_names = ['Texture', 'Perimeter', 'Smoothness',
                                                                   'Compactness', 'Symmetry', 'FractalDimension'])
        
        
        
        Arbol = graphviz.Source(Elementos)
        

 
# Arbol

# 
        plt.figure(figsize=(16,16))
        plot_tree(PronosticoAD, feature_names = ['Texture', 'Perimeter', 'Smoothness',
                                                 'Compactness', 'Symmetry', 'FractalDimension'])
 

# plt.show()

        from sklearn.tree import export_text
        Reporte = export_text(PronosticoAD, feature_names = ['Texture', 'Perimeter', 'Smoothness',
                                                            'Compactness', 'Symmetry', 'FractalDimension'])
# print(Reporte)
#________________________TEXTO_________________
        from fpdf import FPDF


        archivo= "app/static/documentos/generados/arbolito11.txt"
        f= open(archivo,'w')
        cadena=str(Reporte)
        f.write(cadena)
        f.close()
          
  
# save FPDF() class into 
# a variable pdf
        pdf = FPDF()   
   
# Add a page
        pdf.add_page()
   
# Elegimos tipo de letra y tamaño
        pdf.set_font("Times", size = 11)
  
# Abrimos el archivo en modo lectura
        f = open(archivo, "r")
  
# intertamos lo abierto dentro del pdf
        for x in f:
            pdf.cell(200, 10, txt = x, ln = 1, align = 'C')
   
# Guardamos el pdf
        pdf.output("app/static/documentos/generados/arbolito11.pdf")   
        b = pdf.output("app/static/documentos/generados/arbolito11.pdf") 

#________________________TEXTOFIN_________________

        buffer2= BytesIO()
        
        
        nombre_temporal_uuid002 = str(uuid4().hex)
        nombre_temporal_png002 = 'app/static/img/' + nombre_temporal_uuid002 + '.png'

        # Replace "app" to ""
        arbol2 = nombre_temporal_png002.replace('app/', '')
        

        plt.savefig(
            fname=nombre_temporal_png002,
            format='png',
        )
        buffer2.close()


# #### **7) Nuevos pronósticos**

#PIDIENDO LAS VARIABLES AL USUARIO


        AreaTumorID1 = pd.DataFrame({'Texture': [Textura],
                                  'Perimeter': [Perimetro],
                                  'Smoothness': [Suavidad],
                                 'Compactness': [Compacidad],
                                 'Symmetry': [Simetria],
                                 'FractalDimension': [DimensionF]})
        

        resultadoArbol1= "".join(map(str, PronosticoAD.predict(AreaTumorID1)))

        

        # Retorna imagen en base64
        return jsonify({'status': 'success', 'data': json_data11, 'data2': json_data12,'data3': json_data13,'graph':new_name11,'graph2':imgroja, 'imgcalor': calor,'arbol2':arbol2,'newpronostico3':resultadoArbol1})

    return jsonify({'status': 'error', 'message': 'Error al leer el archivo'})


#__________________________________>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>__________________________________>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# #_________________________________________
# #_____________Practica 12__________________
# #_________________________________________

@pagina.route('/clasificacionArbol', methods=['POST'])
def read_csv7():

    if request.method == 'POST':
        
        flask_file = request.files['file']
        
        TexturaC = float(request.form['Texture'])
        
        PerimetroC = float(request.form['Perimeter'])
        
        SuavidaC=float(request.form['Smoothness'])
        
        CompacidadC=float(request.form['Compactness'])
        
        SimetriaC= float(request.form['Symmetry'])
        
        DimensionFC= float(request.form['FractalDimension'])
        

        if not flask_file.filename.endswith('.csv'):
            return make_response(jsonify({'message': 'Seleccione un archivo CSV'}), 400)

        BCancer = pd.read_csv(flask_file)

        data_table_12 = pd.DataFrame(BCancer)
        json_data12 = data_table_12.head(10).to_json(orient='records')

#TABLA 1

#GRAFICA DE MAPA COLOR

# #### **2) Selección de características**  MAPA DE CALOR

        plt.figure(figsize=(14,7))
        MatrizInf = np.triu(BCancer.corr())
        sns.heatmap(BCancer.corr(), cmap='RdBu_r', annot=True, mask=MatrizInf)
        #plt.show()


        buffer3= BytesIO()
        
        
        nombre_temporal_uuid012 = str(uuid4().hex)
        nombre_temporal_png012 = 'app/static/img/' + nombre_temporal_uuid012 + '.png'

        # Replace "app" to ""
        calor = nombre_temporal_png012.replace('app/', '')
        

        plt.savefig(
            fname=nombre_temporal_png012,
            format='png',
        )
        buffer3.close()


# #### **3) Definición de variables predictoras y variable clase**


        BCancer = BCancer.replace({'M': 'Malignant', 'B': 'Benign'})
        
#TABLA2

        data_table_13 = pd.DataFrame(BCancer)
        json_data13 = data_table_13.head(10).to_json(orient='records')
        
        # #Variables predictoras
        X = np.array(BCancer[['Texture',
                              'Area',
                              'Smoothness',
                              'Compactness',
                              'Symmetry',
                              'FractalDimension']])
#TABLA3

        data_table_14 = pd.DataFrame(X)
        json_data14 = data_table_14.head(10).to_json(orient='records')
        
        

        Y = np.array(BCancer[['Diagnosis']])
        
        
#TABLA4

        data_table_15 = pd.DataFrame(X)
        json_data15 = data_table_15.head(10).to_json(orient='records')
        
        
# #### **4) División de datos y aplicación del algoritmo**


        from sklearn.tree import DecisionTreeClassifier
        from sklearn.metrics import classification_report
        from sklearn.metrics import confusion_matrix
        from sklearn.metrics import accuracy_score
        from sklearn import model_selection

        X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(X, Y,
                                                                                        test_size = 0.2,
                                                                                        random_state = 0,
                                                                                        shuffle = True)
#TABLA5

        data_table_16 = pd.DataFrame(X_train)
        json_data16 = data_table_16.head(10).to_json(orient='records')

# #Se entrena el modelo a partir de los datos de entrada
        ClasificacionAD = DecisionTreeClassifier()
        ClasificacionAD.fit(X_train, Y_train)


        Y_Clasificacion = ClasificacionAD.predict(X_validation)
 

# #Se calcula la exactitud promedio de la validación
        ClasificacionAD.score(X_validation, Y_validation)


#_________________

# #### **5) Validación del modelo**


# #Matriz de clasificación
        Y_Clasificacion = ClasificacionAD.predict(X_validation)
        Matriz_Clasificacion = pd.crosstab(Y_validation.ravel(),
                                           Y_Clasificacion,
                                           rownames=['Real'],
                                           colnames=['Clasificación'])
# Matriz_Clasificacion
        json_data20 = Matriz_Clasificacion.head(10).to_json(orient='records')

# #Reporte de la clasificación
        print('Criterio: \n', ClasificacionAD.criterion)
        print('Importancia variables: \n', ClasificacionAD.feature_importances_)
        print("Exactitud", ClasificacionAD.score(X_validation, Y_validation))
        print(classification_report(Y_validation, Y_Clasificacion))

        Importancia = pd.DataFrame({'Variable': list(BCancer[['Texture', 'Area', 'Smoothness', 
                                                     'Compactness', 'Symmetry', 'FractalDimension']]),
                            'Importancia': ClasificacionAD.feature_importances_}).sort_values('Importancia', ascending=False)
        # Importancia


        tabla21= pd.DataFrame(Importancia)
        
        json_data21 = tabla21.head(10).to_json(orient='records')
        

# #### **6) Eficiencia y conformación del modelo de clasificación**


# #!pip install graphviz
# import graphviz
# from sklearn.tree import export_graphviz

# # Se crea un objeto para visualizar el árbol
        Elementos = export_graphviz(ClasificacionAD,
                                     feature_names = ['Texture', 'Area', 'Smoothness',
                                                      'Compactness', 'Symmetry', 'FractalDimension'],
                                      class_names = Y_Clasificacion)
        Arbol = graphviz.Source(Elementos)
# Arbol

# from sklearn.tree import plot_tree
        plt.figure(figsize=(30,20))
        plot_tree(ClasificacionAD,
                   feature_names = ['Texture', 'Area', 'Smoothness',
                                   'Compactness', 'Symmetry', 'FractalDimension'],
                  class_names = Y_Clasificacion)
# plt.show()

  
        
        nombre_temporal_uuidArbolFinal = str(uuid4().hex)
        nombre_temporal_pngArbolFinal = 'app/static/img/' + nombre_temporal_uuidArbolFinal + '.png'

        # Replace "app" to ""
        arbolfinal = nombre_temporal_pngArbolFinal.replace('app/', '')
        

        plt.savefig(
            fname=nombre_temporal_pngArbolFinal,
            format='png',
        )
   

        from sklearn.tree import export_text
        Reporte1 = export_text(ClasificacionAD,
                             feature_names = ['Texture', 'Area', 'Smoothness',
                                             'Compactness', 'Symmetry', 'FractalDimension'])
# print(Reporte)

#________________________TEXTO_________________
        from fpdf import FPDF


        archivo= "app/static/documentos/generados/arbolito12.txt"
        f= open(archivo,'w')
        cadena=str(Reporte1)
        f.write(cadena)
        f.close()
          
  
# save FPDF() class into 
# a variable pdf
        pdf = FPDF()   
   
# Add a page
        pdf.add_page()
   
# Elegimos tipo de letra y tamaño
        pdf.set_font("Times", size = 11)
  
# Abrimos el archivo en modo lectura
        f = open(archivo, "r")
  
# intertamos lo abierto dentro del pdf
        for x in f:
            pdf.cell(200, 10, txt = x, ln = 1, align = 'C')
   
# Guardamos el pdf
        pdf.output("app/static/documentos/generados/arbolito12.pdf")   
        C = pdf.output("app/static/documentos/generados/arbolito12.pdf") 

#________________________TEXTOFIN_________________



#Paciente saber si esta M y B
        
        PacienteID2 = pd.DataFrame({'Texture': [TexturaC], 
                            'Area': [PerimetroC], 
                            'Smoothness': [SuavidaC], 
                            'Compactness': [CompacidadC], 
                            'Symmetry': [SimetriaC], 
                            'FractalDimension': [DimensionFC]})
        resultadoArbol002= "".join(map(str, ClasificacionAD.predict(PacienteID2)))
        
        # Retorna imagen en base64
        return jsonify({'status': 'success', 'data': json_data12,
                        'data2': json_data13,'data3': json_data14,
                        'data4': json_data15,'data5': json_data16,
                        'data9': json_data20,'data10': json_data21,'imgcalor': calor, 'graph':arbolfinal})

    return jsonify({'status': 'error', 'message': 'Error al leer el archivo'})
# #___