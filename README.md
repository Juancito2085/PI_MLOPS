# PI -MLOPS

## Introducción
<p align="justify">
En el presente proyecto se realiza un MVP (Minimun Viable Product) desarrollando el rol de un <strong>Data Scientis</strong> para una empresa multinacional de videojuegos.</p>
<p align="justify">
Se realiza un  Análisis Exploratorio de Datos (EDA) y un proceso ETL para poder generar datasets acordes a los recursos de la plataforma de despliegue, en este caso <strong>Render</strong>.</p>
<p align="justify">
Se genera una API donde se pueden realizar las consultas de los Endpoints correspondientes.</p>
<p align="justify">
También se incluye en este proyecto un sistema de recomendación de juegos, el modelo de ML utilizado es el <strong>modelo de similitud del coseno</strong>.</p>
<p align="justify">
El link de la <a href="https://pi-mlops-skl1.onrender.com">API</a> es el siguiente y tiene valores por defecto para que se pueda ver que tipo de respuesta arroja cada consulta.</p>

## Desarrollo 
<p align="justify">
En esta sección no se profundizará demasiado ya que en los notebooks correspondiente a cada subsección está el proceso debidamente detallado.
</p>

### EDA
<p align="justify">
Ni bien se reciben los datos se procede a hacer un análisis de los mismos para poder tener una visión general de los mismos. Se reciben tres archivos con los juegos, los juegos de los usuarios y el último con las críticas de los usuarios.
</p>

<p align="justify">
La primera acción llevada aquí fue desanidar los archivos los cuales eran de formato JSON comprimidos en formato gzip. Una vez realizado esto se eliminaron los datos irrelevantes para este proyecto debido a que es un MVP y su despliegue es en una capa gratuita por lo que los recursos son reducidos y hay que adaptarse a la situación.
</p>

<p align="justify">
En el caso de valores nulos o faltantes, muchos de ellos no podían estimar mediante algún método de imputación de datos ya que en algunos casos el porcentaje de datos faltantes era importante y de un tamaño considerable, faltaban datos en variables clave para el proyecto y tampoco se detectó un patron adecuado de falta de datos.
</p

<p align="justify">
Al momento de reducir los datos se trata de explorar los estadísticos para ver el tipo de distrbución y ver los valores atípicos si es que los hay. También se eliminaron los duplicados en datos claves, como los id de juegos o usuarios.
</p>
<p align="justify">
El criterio tomado el tratamiento de los datos atípicos en el caso de las horas jugadas fue ver el valor de los cuartiles, donde en el cuarto cuartil se presentaba un rango demasiado amplio de horas jugadas y se trato de tomar valores típicos de horas de juego.
</p>
<p align="justify">
Para posteriores tratamientos de los datos se tuvieron en cuenta los años de lanzamientos de juegos, los juegos mas jugados y los géneros y tags principales para las transformaciones. Lo cual será explicado más adelante.
</p>

### ETL
<p align="justify">
Para el proceso de transformación de datos a datasets se realizaron 4 datasets los cuales serán explicados a continuación.
</p>

<p align="justify">

- developers.parquet

En este dataset se encuentra toda la información para hacer las consultas a sobre los desarrolladores. Este contiene los desarrolladores, el año de lanzamiento de los juegos junto con su precio y su clave de identificación. Ademas contiene las recomendaciones de los usuarios para cada juego y un análisis de sentimiento para cada review donde se le asigna una valor entero significando 0 : reseña negativa, 1 : reseña neutral y 2 : reseña positiva.</p>

<p align="justify">

- users.parquet

En este dataset se encuentran los usuarios identificados por su clave , la cantidad de items que tienen, junto con cada juego el precio y las horas jugadas para cada uno además de la fecha de su lanzamiento.</p>

<p align="justify">

- users_recommend.parquet

Este es un documento simple que solo contiene la cantidad de recomendaciones por usuarios y se creó para simplificar las cosas y no generar dataframes con tantos registros.</p>
<p align="justify">

- data.parquet

Aquí se encuentran los datos para el sistema de recomendación, este documento contiene los nombres de los juegos, los generos y los tags. Para hacer este dataset se consideraon los juegos donde las horas jugadas eran mayores a cero. En el caso del genero solo se tomo el género principal de dicha columna y se hizo lo mismo con los tags o etiquetas, esto se hizo para reducir la cantidad de información y dejar solo la más importante.</p>

### Sistema de recomendación
<p align="justify">
El sistema de recomendación se realizo con el modelo de similitud del coseno que es una medida de similitud entre dos vectores no nulos en un espacio que tiene una medida de ángulo. En el contexto de los sistemas de recomendación, se utiliza para calcular la similitud entre los elementos (por ejemplo, productos, películas, libros, etc.) o entre los usuarios.</p>

<p align="justify">
La idea es representar los elementos o usuarios como vectores en un espacio multidimensional. Cada dimensión en este espacio puede representar una característica del elemento o una preferencia del usuario. Luego, la similitud del coseno se calcula como el coseno del ángulo entre estos dos vectores.</p>

<p align="justify">
Para esto se utilizó el dataset <strong>data</strong> y el sistema recomienda en base al nombre del juego, el género y la etiqueta que tenga, esto debido a que los gamers tienden a jugar juegos de similares géneros o características (englobadas en las tags).</p>

### Endpoints
<p align="justify">
A continuación se dará una breve explicación de cadad Endpoint que se encontrará en la API para saber que respuesta esperar de los mismos y con que variables hay que hacer solicitudes.</p>

<p align="justify">
1) def developer( desarrollador : str ): 
Devuelve la cantidad de items y porcentaje de contenido gratis por año según empresa desarrolladora.</p>

<p align="justify">
2) def userdata( User_id : str ):
Devuelve la cantidad de dinero gastado por el usuario, el porcentaje de recomendación en base a los reviews y la cantidad de items.</p>

<p align="justify">
3) def UserForGenre( genero : str ):
Devuelve el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año de lanzamiento.</p>

<p align="justify">
4) def best_developer_year( año : int ):
Devuelve el top 3 de desarrolladores con juegos mas recomendados por usuarios para el año dado.</p>

<p align="justify">
5) def developer_reviews_analysis( desarrolladora : str ):
Devuelve el nombre del desarrollador como llave y una lista con la cantidad total de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento como valor positivo o negativo.</p>

<p align="justify">
6) def recomendacion_juego( id de producto ):
Ingresando el id de producto, deberíamos recibir una lista con 5 juegos recomendados similares al ingresado.
</p>

### Tecnologías utilizadas
<p align="justify">

- Python 
Se utilizo lenguaje python para este proyecto junto con las siguientes librerías
    1) fastapi
    2) uvicorn
    3) pandas
    4) numpy
    6) pyarrow
    7) scikit-learn
    8) ast
    9) textblob
</p>
<p align="justify">

- Render
El despliegue se realizo en Render en la capa gratuita con 512 MB de memoria ram y 0.1 CPU según su <a href="https://render.com/pricing">página web</a>.</p>

<p align="justify">

- Github
En este repositorio se puede encontrar el archivo principal de la API, el archivo <strong>requirements.txt</strong> que contiene todas las librerias que utilizarán. En la carpeta <strong>Datasets</strong> se encuentran todos los archivos necesarios y en la carpeta <strong>Notebooks</strong> se encuentran los Jupiter Notebooks de las secciones.</p>