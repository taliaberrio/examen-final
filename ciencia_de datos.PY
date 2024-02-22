import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    confusion_matrix,
    ConfusionMatrixDisplay,
)
from sklearn.model_selection import train_test_split

# Cargar el dataset desde un archivo CSV
datos = pd.read_csv("C:/Users/USUARIO/Desktop/EXAMENES/EmployeesData.csv")

# Verificar si existen valores faltantes
print(datos.isnull().sum())

# Convertir la columna 'LeaveOrNot' a etiquetas categóricas
datos["LeaveOrNot"] = datos["LeaveOrNot"].map({0: "Not Leave", 1: "Leave"})

# Eliminar filas con valores faltantes en las columnas ExperienceInCurrentDomain y JoiningYear
datos.dropna(subset=["ExperienceInCurrentDomain", "JoiningYear"], inplace=True)

# Imputar datos faltantes en la columna Age con la media
datos["Age"].fillna(datos["Age"].mean(), inplace=True)

# Imputar datos faltantes en la columna PaymentTier con la moda
datos["PaymentTier"].fillna(datos["PaymentTier"].mode()[0], inplace=True)
# Seleccionar solo las columnas numéricas del DataFrame
columnas_numericas = datos.select_dtypes(include=[np.number])

# Calcular los cuantiles sobre las columnas numéricas
Q1 = columnas_numericas.quantile(0.25)
Q3 = columnas_numericas.quantile(0.75)
IQR = Q3 - Q1

# Identificar los registros atípicos
mascara_outliers = (
    (columnas_numericas < (Q1 - 1.5 * IQR)) | (columnas_numericas > (Q3 + 1.5 * IQR))
).any(axis=1)

# Eliminar registros con valores atípicos
datos = datos[~mascara_outliers]

# 2- Análisis Exploratorio de Datos (EDA)

# Graficar la distribución de los sexos con un gráfico de torta
plt.figure(figsize=(6, 6))
datos["Gender"].value_counts().plot(kind="pie", autopct="%1.1f%%")
plt.title("Distribución de Sexos")
plt.ylabel("")
plt.show()

# Graficar la distribución de niveles de estudio
fig, axes = plt.subplots(1, 2, figsize=(12, 6))

datos["Education"].value_counts().plot(kind="bar", ax=axes[0])
axes[0].set_title("Distribución de Niveles de Estudio")
axes[0].set_ylabel("Cantidad")

datos["Education"].value_counts().plot(kind="pie", autopct="%1.1f%%", ax=axes[1])
axes[1].set_title("Distribución de Niveles de Estudio")
axes[1].set_ylabel("")

plt.show()

# Histograma para responder la pregunta sobre los jóvenes y licencias
plt.figure(figsize=(8, 6))
datos[datos["Age"] < 30]["LeaveOrNot"].hist()
plt.title("Propensión de los Jóvenes a Tomar Licencias")
plt.xlabel("LeaveOrNot")
plt.ylabel("Count")
plt.xticks([0, 1], ["Not Leave", "Leave"])
plt.show()

# Distribución de clases
plt.figure(figsize=(6, 6))
datos["LeaveOrNot"].value_counts().plot(kind="pie", autopct="%1.1f%%")
plt.title("Distribución de Clases")
plt.ylabel("")
plt.show()

# 3-Modelado de Datos
# Preparar datos para el modelado
X = datos.drop(columns=["LeaveOrNot"])
y = datos["LeaveOrNot"]
X = pd.get_dummies(X)

# Partición estratificada del dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y)

# Entrenar dos RandomForests
rf_model = RandomForestClassifier(random_state=42)
rf_model_balanced = RandomForestClassifier(class_weight="balanced", random_state=42)

rf_model.fit(X_train, y_train)
rf_model_balanced.fit(X_train, y_train)


# Calcular métricas de desempeño
def calculate_metrics(model, X_train, X_test, y_train, y_test):
    y_pred_train = model.predict(X_train)
    y_pred_test = model.predict(X_test)

    train_accuracy = accuracy_score(y_train, y_pred_train)
    test_accuracy = accuracy_score(y_test, y_pred_test)

    f1_train = f1_score(y_train, y_pred_train, average="weighted")
    f1_test = f1_score(y_test, y_pred_test, average="weighted")

    cm = confusion_matrix(y_test, y_pred_test)

    return train_accuracy, test_accuracy, f1_train, f1_test, cm


train_accuracy, test_accuracy, f1_train, f1_test, cm = calculate_metrics(
    rf_model, X_train, X_test, y_train, y_test
)
print("Random Forest sin balanceo:")
print("Accuracy (train):", train_accuracy)
print("Accuracy (test):", test_accuracy)
print("F1 Score (train):", f1_train)
print("F1 Score (test):", f1_test)
print("Confusion Matrix:\n", cm)

(
    train_accuracy_balanced,
    test_accuracy_balanced,
    f1_train_balanced,
    f1_test_balanced,
    cm_balanced,
) = calculate_metrics(rf_model_balanced, X_train, X_test, y_train, y_test)
print("\nRandom Forest con balanceo:")
print("Accuracy (train):", train_accuracy_balanced)
print("Accuracy (test):", test_accuracy_balanced)
print("F1 Score (train):", f1_train_balanced)
print("F1 Score (test):", f1_test_balanced)
print("Confusion Matrix:\n", cm_balanced)

# Graficar matriz de confusión
disp = ConfusionMatrixDisplay(
    confusion_matrix=cm, display_labels=["Leave", "Not Leave"]
)
disp.plot()
plt.title("Confusion Matrix - Random Forest sin balanceo")
plt.show()

disp_balanced = ConfusionMatrixDisplay(
    confusion_matrix=cm_balanced, display_labels=["Leave", "Not Leave"]
)
disp_balanced.plot()
plt.title("Confusion Matrix - Random Forest con balanceo")
plt.show()
