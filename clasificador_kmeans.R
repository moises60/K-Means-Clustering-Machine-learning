# Importar los datos
dataset = read.csv("car_purchasing.csv")
X <- as.matrix(dataset[, c(6, 9)])

# Método de codo
set.seed(1)
wcss = vector()
for (i in 1:10){
  wcss[i] <- sum(kmeans(X, i)$withinss)
}
plot(1:10, wcss, type = 'b', main = "Método del codo",
     xlab = "Número de clusters (k)", ylab = "WCSS(k)")

# Aplicar el algoritmo de k-means con k óptimo
set.seed(2)
kmeans <- kmeans(X, 2, iter.max = 300, nstart = 10)

#Visualización de los clusters
#install.packages("cluster")
library(cluster)
clusplot(X, 
         kmeans$cluster,
         lines = 0,
         shade = TRUE,
         color = TRUE,
         labels = 1,
         plotchar = TRUE,
         span = TRUE,
         main = "Clustering de clientes",
         xlab = "Ingresos anuales",
         ylab = "Gasto en vehículos"
)




