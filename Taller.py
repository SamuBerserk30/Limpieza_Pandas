import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import os

os.makedirs('images', exist_ok=True)

# #1 CARGAR DATOS
data = pd.read_csv("dataset_banco.csv")
print(f"#1 Tamaño inicial: {data.shape}\n")

# #2 ELIMINAR DATOS FALTANTES
print("=== #2 DATOS FALTANTES ===")
print(data.isnull().sum())
print()
data.dropna(inplace=True)
print(f" Datos faltantes eliminados → Nuevo tamaño: {data.shape}\n")

# #3 ELIMINAR DUPLICADOS
print("=== #3 DUPLICADOS ===")
print(f"Duplicados encontrados: {data.duplicated().sum()}")
data.drop_duplicates(inplace=True)
print(f" Duplicados eliminados → Nuevo tamaño: {data.shape}\n")

# #4 ELIMINAR OUTLIERS
print("=== #4 OUTLIERS ===")
print(f"Filas antes de limpiar outliers: {data.shape[0]}")

data = data[data['age'] <= 100]
print(f"  Después de eliminar age > 100:        {data.shape[0]} filas")

data = data[data['duration'] > 0]
print(f"  Después de eliminar duration <= 0:    {data.shape[0]} filas")

data = data[data['previous'] <= 100]
print(f"  Después de eliminar previous > 100:   {data.shape[0]} filas")

print(f" Outliers eliminados\n")

# #5 HISTOGRAMAS DE VARIABLES NUMÉRICAS
print("=== #5 GENERANDO HISTOGRAMAS ===")
cols_num = ['age', 'balance', 'day', 'duration', 'campaign', 'pdays', 'previous']

sns.set_style("whitegrid")

for col in cols_num:
    plt.figure(figsize=(12, 5))
    sns.histplot(data[col], color='skyblue', bins=30)
    plt.title(f'Histograma de {col}')
    plt.tight_layout()
    plt.savefig(f'images/{col}.png')
    plt.close()
    print(f"  images/{col}.png guardada")

print(f"\n Histogramas generados\n")

# #6 VALIDAR COLUMNAS NUMÉRICAS
print("=== #6 VALIDACIÓN DE COLUMNAS NUMÉRICAS ===")
print(data.describe())
print(f"\n Validación de columnas numéricas completada\n")

# #7 CORRECCIÓN DE ERRORES TIPOGRÁFICOS
print("=== #7 CORRECCIÓN TIPOGRÁFICA ===")
cols_cat = ['job', 'marital', 'education', 'default', 'housing',
            'loan', 'contact', 'month', 'poutcome', 'y']

# 7.1 Countplots ANTES de corregir
print("  Generando countplots ANTES de la corrección...")
fig, ax = plt.subplots(nrows=10, ncols=1, figsize=(10, 40))
fig.subplots_adjust(hspace=1)
for i, col in enumerate(cols_cat):
    sns.countplot(x=col, data=data, ax=ax[i], color='skyblue')
    ax[i].set_title(f'{col} (antes)')
    ax[i].set_xticklabels(ax[i].get_xticklabels(), rotation=30)
plt.savefig('images/countplot_antes.png')
plt.close()
print(f"  images/countplot_antes.png guardada")

# 7.2 Pasar todo a minúsculas
for column in data.columns:
    if column in cols_cat:
        data[column] = data[column].str.lower()
print("   Todo a minúsculas")

# 7.3 Unificar subniveles
data['job'] = data['job'].str.replace('admin.', 'administrative', regex=False)
data['marital'] = data['marital'].str.replace('div.', 'divorced', regex=False)
data['education'] = data['education'].str.replace('sec.', 'secondary', regex=False)
data.loc[data['education'] == 'unk', 'education'] = 'unknown'
data.loc[data['contact'] == 'phone', 'contact'] = 'telephone'
data.loc[data['contact'] == 'mobile', 'contact'] = 'cellular'
data.loc[data['poutcome'] == 'unk', 'poutcome'] = 'unknown'
print("   Subniveles unificados")

# 7.4 Countplots DESPUÉS de corregir
print("  Generando countplots DESPUÉS de la corrección...")
fig, ax = plt.subplots(nrows=10, ncols=1, figsize=(10, 40))
fig.subplots_adjust(hspace=1)
for i, col in enumerate(cols_cat):
    sns.countplot(x=col, data=data, ax=ax[i], color='#34d399')
    ax[i].set_title(f'{col} (después)')
    ax[i].set_xticklabels(ax[i].get_xticklabels(), rotation=30)
plt.savefig('images/countplot_despues.png')
plt.close()
print(f"   images/countplot_despues.png guardada")

print(f"\n Corrección tipográfica completada\n")

# #8 VALIDAR COLUMNAS CATEGÓRICAS
print("=== #8 VALIDACIÓN DE COLUMNAS CATEGÓRICAS ===")
for col in cols_cat:
    print(f"  Columna {col}: {data[col].nunique()} subniveles → {sorted(data[col].unique())}")
print(f"\n Validación de columnas categóricas completada\n")

# #9 GUARDAR DATASET LIMPIO
data.to_csv("dataset_banco_limpio.csv", index=False)
print("=== RESUMEN FINAL ===")
print(f"  Tamaño original:  45215 filas × 17 columnas")
print(f"  Tamaño final:     {data.shape[0]} filas × {data.shape[1]} columnas")
print(f"  Filas eliminadas: {45215 - data.shape[0]}")
print(f"\n Dataset limpio guardado en 'dataset_banco_limpio.csv'")