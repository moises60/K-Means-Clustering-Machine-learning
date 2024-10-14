import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import seaborn as sns
import chardet

# 2. Detectar la codificación del archivo (opcional pero recomendado)
# Puedes comentar esta sección si ya conoces la codificación
with open("car_purchasing.csv", 'rb') as f:
    result = chardet.detect(f.read(10000))  # Leer los primeros 10000 bytes
print(f"Codificación detectada: {result['encoding']}")

# 3. Cargar los datos con la codificación correcta
dataset = pd.read_csv("car_purchasing.csv", encoding='cp1252')  # Reemplaza si usas otra codificación

# 4. Exploración Inicial de Datos
print("Primeras filas del dataset:")
print(dataset.head())

print("\nInformación del dataset:")
print(dataset.info())

print("\nResumen estadístico:")
print(dataset.describe())

# 5. Manejo de Valores Faltantes
print("\nValores faltantes por columna:")
print(dataset.isnull().sum())

# valores faltantes
dataset = dataset.dropna()

# 6. Selección de Características
X = dataset.iloc[:, [5, 8]].values

# 7. Escalado de Características
scaler = StandardScaler()
X_scaled = X #en este caso no es necesari

# 8. Método del Codo para determinar el número óptimo de clusters
wcss = []
range_clusters = range(1, 11)
for i in range_clusters:
    kmeans = KMeans(n_clusters=i, init="k-means++", max_iter=300, n_init=10, random_state=42)
    kmeans.fit(X_scaled)
    wcss.append(kmeans.inertia_)

plt.figure(figsize=(10,6))
plt.plot(range_clusters, wcss, marker='o')
plt.title("Método del Codo")
plt.xlabel("Número de Clusters")
plt.ylabel("WCSS")
plt.xticks(range_clusters)
plt.grid(True)
plt.show()

# 9. Evaluación con el Coeficiente de Silueta
silhouette_scores = []
for i in range(2, 11):
    kmeans = KMeans(n_clusters=i, init="k-means++", max_iter=300, n_init=10, random_state=42)
    labels = kmeans.fit_predict(X_scaled)
    score = silhouette_score(X_scaled, labels)
    silhouette_scores.append(score)

plt.figure(figsize=(10,6))
plt.plot(range(2, 11), silhouette_scores, marker='o', color='green')
plt.title("Coeficiente de Silueta para diferentes números de clusters")
plt.xlabel("Número de Clusters")
plt.ylabel("Coeficiente de Silueta")
plt.xticks(range(2, 11))
plt.grid(True)
plt.show()

# Basándonos en el Método del Codo y el Coeficiente de Silueta
optimal_clusters = 2

# 10. Aplicar K-Means con el número óptimo de clusters
kmeans = KMeans(n_clusters=optimal_clusters, init="k-means++", max_iter=300, n_init=10, random_state=42)
y_kmeans = kmeans.fit_predict(X_scaled)

# 11. Añadir los labels de clusters al dataset original
dataset['Cluster'] = y_kmeans

# 12. Visualización de los Clusters
plt.figure(figsize=(10,6))
colors = ['red', 'blue', 'green', 'cyan', 'magenta', 'yellow', 'black', 'orange', 'purple', 'brown']
for i in range(optimal_clusters):
    plt.scatter(
        X_scaled[y_kmeans == i, 0], 
        X_scaled[y_kmeans == i, 1], 
        s=100, 
        c=colors[i],
        label=f"Cluster {i+1}"
    )
plt.scatter(
    kmeans.cluster_centers_[:, 0], 
    kmeans.cluster_centers_[:, 1], 
    s=300, 
    c='yellow', 
    label='Centroides',
    marker='X',
    edgecolor='black'
)
plt.title("Clusters de Clientes")
plt.xlabel("Ingresos Anuales")
plt.ylabel("Gastos")
plt.legend()
plt.grid(True)
plt.show()

# 13. Análisis de los Clusters
print("\nDescripción de los clusters:")
for i in range(optimal_clusters):
    cluster_data = dataset[dataset['Cluster'] == i]
    print(f"\nCluster {i+1}:")
    print(cluster_data.describe())


