# IronHack-Final-Project


FREE FIX 

Se intentará crear un ítem based recommender dado que un usuario introduzca el nombre de una película y se mostrará las 5 películas mas similares a la película introducida. Para hacer esto utilizamos una matriz de distancias y con la similitud del coseno determinará cual será la mas similar tomando en cuenta el genero, palabras en comunes, año y ratings. Adicionalmente estos features tendrán unos pesos determinados según su relevancia a la hora de detectar la similitud.


Este Repositorio contiene 4 Carpetas (Images, Input, Presentacion y Scr) dentro de la carpeta de Scr podemos encontrar el archivo FreeFixFinal.py donde se ve el pipeline del proyecto. Al ser ejecutado por el terminal luego de 46 segundos se le pedirá introducir el nombre de una película, la introducimos y esperamos 30 segundos mas y veremos el resultado reflejado por pantalla. Podrás obtener 2 resultados 

-    La película introducida y sus recomendaciones.
-    No se encontró la película.

Si aparece la opción de no se encontró la película, es posible que este mal escrita o que no este identificando el nombre completo de la película y para este caso debemos revisar los [“title”] de el data frame para poder ver si la película esta en los registros.

En la carpeta input encontramos los 4 .csv con los cuales trabajaremos y fueron obtenidos de https://grouplens.org/datasets/movielens/ . En imagen tenemos 4 archivo que detallan exploración de los datos como por ejemplo mejor ranking de películas o mayor cantidad de genero por película. 

