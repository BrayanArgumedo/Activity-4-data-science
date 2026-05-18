import pandas as pd

# ─────────────────────────────────────────────
#  PASO 3 — Funciones de Búsqueda y Referencia
#  Ejercicio 1: Agregar Mercado y Región desde hoja Regiones (por País)
#  Ejercicio 2: Agregar Categoría, Sub-Categoría y Nombre Producto
#               desde hoja Productos (por ID Producto)
# ─────────────────────────────────────────────

print("=" * 60)
print("  PASO 3 — FUNCIONES DE BÚSQUEDA Y REFERENCIA")
print("=" * 60)

# ── Cargar datos del paso anterior ───────────
print("\nCargando datos del Paso 2...")
df = pd.read_pickle("datos_paso2.pkl")
print(f"  Registros: {len(df):,}  |  Columnas: {len(df.columns)}")


# ── Ejercicio 1: Cruzar con hoja Regiones ─────────────────────
print("\n" + "─" * 60)
print("EJERCICIO 1 — Agregar 'Mercado' y 'Región' desde hoja Regiones")
print("  Clave de cruce: columna 'País'")
print("─" * 60)

df_regiones = pd.read_excel("Dataset Venta.xlsx", sheet_name="Regiones")
print(f"\n  Hoja Regiones cargada: {len(df_regiones)} filas")

# La hoja tiene países con múltiples filas (Austria, Mongolia y EE.UU.).
# Al igual que BUSCARV, conservamos solo la primera coincidencia por País.
duplicados_reg = df_regiones["País"].duplicated().sum()
df_regiones = df_regiones.drop_duplicates(subset="País", keep="first")
print(f"  Países duplicados eliminados: {duplicados_reg}")
print(f"  Países únicos para el cruce: {len(df_regiones)}")

# Verificar países del dataset que NO estén en la tabla Regiones
paises_ventas   = set(df["País"].unique())
paises_regiones = set(df_regiones["País"].unique())
sin_region      = paises_ventas - paises_regiones
if sin_region:
    print(f"\n  AVISO: {len(sin_region)} países sin coincidencia en Regiones:")
    for p in sorted(sin_region):
        print(f"    - {p}")
else:
    print("  Todos los países tienen coincidencia en la tabla Regiones.")

# Merge (equivalente a BUSCARV en Excel)
df = df.merge(df_regiones, on="País", how="left")

# Verificar resultado
nulos_mercado = df["Mercado"].isna().sum()
nulos_region  = df["Región"].isna().sum()
print(f"\n  Columna 'Mercado' añadida — Valores nulos: {nulos_mercado}")
print(f"  Columna 'Región' añadida  — Valores nulos: {nulos_region}")

print("\n  Muestra (primeras 6 filas):")
print(df[["País", "Mercado", "Región"]].head(6).to_string(index=False))

print("\n  Distribución de registros por Mercado:")
dist_mercado = df["Mercado"].value_counts().reset_index()
dist_mercado.columns = ["Mercado", "Registros"]
print(dist_mercado.to_string(index=False))


# ── Ejercicio 2: Cruzar con hoja Productos ────────────────────
print("\n" + "─" * 60)
print("EJERCICIO 2 — Agregar 'Categoría', 'Sub-Categoría' y 'Nombre Producto'")
print("  desde hoja Productos (clave de cruce: 'ID Producto')")
print("─" * 60)

df_productos = pd.read_excel("Dataset Venta.xlsx", sheet_name="Productos")
print(f"\n  Hoja Productos cargada: {len(df_productos):,} filas")

# La hoja tiene 476 IDs duplicados con nombres distintos (problema de calidad del catálogo).
# Al igual que VLOOKUP, conservamos solo la primera coincidencia por ID.
duplicados_prod = df_productos["ID Producto"].duplicated().sum()
df_productos = df_productos.drop_duplicates(subset="ID Producto", keep="first")
print(f"  IDs duplicados eliminados: {duplicados_prod}")
print(f"  Productos únicos para el cruce: {len(df_productos):,}")

# Verificar productos del dataset que NO estén en el catálogo
ids_ventas    = set(df["ID Producto"].unique())
ids_productos = set(df_productos["ID Producto"].unique())
sin_producto  = ids_ventas - ids_productos
if sin_producto:
    print(f"\n  AVISO: {len(sin_producto)} ID Producto sin coincidencia en catálogo:")
    for p in sorted(list(sin_producto))[:10]:
        print(f"    - {p}")
else:
    print("  Todos los ID Producto tienen coincidencia en el catálogo.")

# Merge
df = df.merge(df_productos, on="ID Producto", how="left")

# Verificar resultado
nulos_cat    = df["Categoría"].isna().sum()
nulos_subcat = df["Sub-Categoría"].isna().sum()
nulos_nombre = df["Nombre Producto"].isna().sum()
print(f"\n  Columna 'Categoría'      — Valores nulos: {nulos_cat}")
print(f"  Columna 'Sub-Categoría'  — Valores nulos: {nulos_subcat}")
print(f"  Columna 'Nombre Producto'— Valores nulos: {nulos_nombre}")

print("\n  Muestra (primeras 6 filas):")
print(df[["ID Producto", "Categoría", "Sub-Categoría", "Nombre Producto"]]
      .head(6).to_string(index=False))

print("\n  Distribución de registros por Categoría:")
dist_cat = df["Categoría"].value_counts().reset_index()
dist_cat.columns = ["Categoría", "Registros"]
print(dist_cat.to_string(index=False))


# ── Resumen final ─────────────────────────────
print("\n" + "=" * 60)
print("  RESUMEN — Estado del dataset tras el Paso 3")
print("=" * 60)
print(f"  Columnas antes del paso : 25")
print(f"  Columnas ahora          : {len(df.columns)}")
print(f"  Nuevas columnas         : Mercado, Región, Categoría,")
print(f"                            Sub-Categoría, Nombre Producto")
print(f"  Total registros         : {len(df):,}")

print("\nColumnas actuales del dataset:")
for i, col in enumerate(df.columns, 1):
    print(f"  {i:02d}. {col}")


# ── Guardar resultado intermedio ──────────────
print("\nGuardando resultado intermedio...")
df.to_pickle("datos_paso3.pkl")
print("  Archivo guardado: datos_paso3.pkl")
print("\n¡Paso 3 completado exitosamente!")
