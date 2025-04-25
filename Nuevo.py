import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Cargamos el archivo CSV
leer = pd.read_csv('./Datos_Colombia.csv')
# Convertimos a DataFrame
colombia = pd.DataFrame(leer)
# Convertimos la Columna 'Fecha' a tipo Entero
colombia['year'] = colombia['year'].astype(int)
# Filtramos los datos entre 2015 y 2023
filtrado = colombia[(colombia['year']>= 2015) & (colombia['year']<= 2023)]
# Nuevas Columnas

# ¿Qué tanto del total es renovable? #
filtrado['%_energia_renovable'] = (filtrado['consumo_renovables']/filtrado['consumo_energia_primaria'])*100
# graficamos
plt.figure(figsize=(10, 6))
plt.plot(filtrado['year'], filtrado['%_energia_renovable'], color='green', marker='o')
plt.title('Porcentaje de Energía Renovable en el Total (Colombia)')
plt.xlabel('Año')
plt.ylabel('Participación Renovable (%)')
plt.grid(True)
plt.tight_layout()
plt.show()

# -------------------------------------------------- #
# ¿Cuánto crece el consumo año a año? #
filtrado['crecimiento_total'] = filtrado['consumo_energia_primaria'].pct_change()*100
# ---- Graficamos el crecimiento ---- #
plt.figure(figsize=(10, 6))
plt.plot(filtrado['year'], filtrado['crecimiento_total'], color='blue', marker='o')
plt.axhline(0, color='gray', linestyle='--')  # Línea de referencia en 0
plt.title('Crecimiento Anual del Consumo de Energía en Colombia')
plt.xlabel('Año')
plt.ylabel('Crecimiento (%)')
plt.grid(True)
plt.tight_layout()
plt.show()
# -------------------------------------------------- #

# ¿Qué tan dependientes somos de fósiles? #
filtrado['consumo_fosiles'] = (filtrado['consumo_combustibles_fosiles']/colombia['consumo_energia_primaria']*100)
# ---- Graficamos las dependencias fosiles ---- #
plt.figure(figsize=(10, 6))
plt.plot(filtrado['year'], filtrado['consumo_fosiles'], marker='o', color='firebrick')
plt.title('Dependencia de Colombia en Combustibles Fósiles (%)')
plt.xlabel('Año')
plt.ylabel('% de Energía Primaria de Origen Fósil')
plt.grid(True)
plt.tight_layout()
plt.show()


# Evolución de renovables vs fósiles #

# ---- Graficamos la evolucion ---- #
plt.figure(figsize=(10, 6))
plt.plot(filtrado['year'], filtrado['consumo_renovables'], label='Renovables', color='green', marker='o')
plt.plot(filtrado['year'], filtrado['consumo_combustibles_fosiles'], label='Fósiles', color='gray', marker='o')
plt.title('Consumo de Energía Renovable vs Fósil en Colombia')
plt.xlabel('Año')
plt.ylabel('Consumo de Energía (TWh)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Suma total de renovables y energía primaria en todos los años
total_renovables = filtrado['consumo_renovables'].sum()
total_general = filtrado['consumo_energia_primaria'].sum()

# Calcular no renovables
total_no_renovables = total_general - total_renovables
# Gráfica de pastel
plt.figure(figsize=(6, 6))
plt.pie([total_renovables, total_no_renovables],
         labels=['Renovables acumuladas', 'No Renovables acumuladas'],
         autopct='%1.1f%%',
         colors=['green', 'gray'],
         startangle=90)
plt.title('Consumo Energético Acumulado en Colombia (Renovables vs No Renovables)')
plt.axis('equal')
plt.tight_layout()
plt.show()



# Año más reciente con datos completos
año_actual = filtrado['year'].max()
datos_recientes = filtrado[filtrado['year'] == año_actual]
# Datos por fuente
fuentes = {
    'Hidroeléctrica': float(datos_recientes['electricidad_hidroelectrica']),
    'Gas': float(datos_recientes['electricidad_gas']),
    'Carbón': float(datos_recientes['electricidad_carbon']),
    'Petróleo': float(datos_recientes['electricidad_petroleo']),
    'Biocombustibles': float(datos_recientes['electricidad_biocombustibles']),
    'Otras Renovables': float(datos_recientes['electricidad_otras_renovables']),
}

# Gráfica de pastel
plt.figure(figsize=(8, 8))
plt.pie(fuentes.values(), labels=fuentes.keys(), autopct='%1.1f%%', startangle=140, colors=plt.cm.Set3.colors)
plt.title(f'Generación de Electricidad por Fuente en Colombia ({año_actual})')
plt.axis('equal')  # Círculo perfecto
plt.tight_layout()
plt.show()

# ¿Cuál ha sido la evolución del consumo de energía renovable vs fósil?
plt.figure(figsize=(10, 6))
plt.plot(filtrado['year'], filtrado['consumo_renovables'], label='Renovables', color='green', marker='o')
plt.plot(filtrado['year'], filtrado['consumo_combustibles_fosiles'], label='Fósiles', color='gray', marker='o')
plt.title('Evolución del Consumo de Energía Renovable vs Fósil en Colombia')
plt.xlabel('Año')
plt.ylabel('Consumo de Energía (TWh)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# ¿Qué fuente de energía renovable ha crecido más?
fuentes = ['electricidad_hidroelectrica', 'electricidad_biocombustibles', 'electricidad_otras_renovables']
crecimientos = {}

for fuente in fuentes:
     valor_inicial = filtrado.iloc[0][fuente]
     valor_final = filtrado.iloc[-1][fuente]
     crecimiento = valor_final - valor_inicial
     crecimientos[fuente] = crecimiento

# Ordenamos y mostramos como gráfico de barras
plt.figure(figsize=(8, 6))
plt.bar(crecimientos.keys(), crecimientos.values(), color='mediumseagreen')
plt.title('Crecimiento de Fuentes Renovables (2015-2023)')
plt.ylabel('Crecimiento (TWh)')
plt.xticks(rotation=30)
plt.grid(True, axis='y')
plt.tight_layout()
plt.show()

# ¿Cómo ha evolucionado la intensidad de carbono en la electricidad?
plt.figure(figsize=(10, 6))
plt.plot(filtrado['year'], filtrado['intensidad_carbono_electricidad'], color='darkred', marker='o')
plt.title('Evolución de la Intensidad de Carbono en la Electricidad (gCO2/kWh)')
plt.xlabel('Año')
plt.ylabel('gCO2 por kWh')
plt.grid(True)
plt.tight_layout()
plt.show()

# ¿Cuál ha sido la evolución de las emisiones de gases de efecto invernadero?
plt.figure(figsize=(10, 6))
plt.plot(filtrado['year'], filtrado['emisiones_gases_efecto_invernadero'], marker='o', color='darkorange')
plt.title('Emisiones de Gases de Efecto Invernadero en Colombia')
plt.xlabel('Año')
plt.ylabel('Emisiones (Millones de toneladas de CO₂ eq)')
plt.grid(True)
plt.tight_layout()
plt.show()


# ¿Qué tipo de fuente genera más electricidad? (año más reciente)
# Año más reciente
año_actual = colombia['year'].max()
reciente = colombia[colombia['year'] == año_actual]

fuentes = {
    'Hidroeléctrica': float(reciente['electricidad_hidroelectrica']),
    'Gas': float(reciente['electricidad_gas']),
    'Carbón': float(reciente['electricidad_carbon']),
    'Petróleo': float(reciente['electricidad_petroleo']),
    'Solar': float(reciente['electricidad_solar']),
    'Eólica': float(reciente['electricidad_eolica']),
    'Biocombustibles': float(reciente['electricidad_biocombustibles']),
    'Otras Renovables': float(reciente['electricidad_otras_renovables']),
}

# Pastel
plt.figure(figsize=(8, 8))
plt.pie(fuentes.values(), labels=fuentes.keys(), autopct='%1.1f%%', startangle=140, colors=plt.cm.Pastel1.colors)
plt.title(f'Generación de Electricidad por Fuente en Colombia ({año_actual})')
plt.axis('equal')
plt.tight_layout()
plt.show()