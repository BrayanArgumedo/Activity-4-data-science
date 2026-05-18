import pandas as pd
import re

# ─────────────────────────────────────────────
#  PASO 2 — Funciones de Texto
#  Ejercicio 1: Limpiar espacios en Método Envío
#  Ejercicio 2: Unificar fechas (Mes/Dia/Año → fecha completa)
#  Ejercicio 3: Crear columna ID_Venta
#  Ejercicio 4: Crear columna ID_Cliente
# ─────────────────────────────────────────────

print("=" * 60)
print("  PASO 2 — FUNCIONES DE TEXTO")
print("=" * 60)

# ── Cargar datos ──────────────────────────────
print("\nCargando datos...")
df = pd.read_excel("Dataset Venta.xlsx", sheet_name="Ventas Supermercado")
print(f"  Registros cargados: {len(df):,}")
print(f"  Columnas: {len(df.columns)}")


# ── Ejercicio 1: Limpiar espacios en Método Envío ─────────────
print("\n" + "─" * 60)
print("EJERCICIO 1 — Eliminar espacios innecesarios: 'Método Envio'")
print("─" * 60)

antes = df["Método Envio"].unique()
print(f"\nValores ANTES de limpiar ({len(antes)} únicos):")
for v in sorted(antes):
    print(f"  {repr(v)}")

# Quitar espacios al inicio/final y colapsar espacios internos múltiples
df["Método Envio"] = df["Método Envio"].apply(
    lambda x: re.sub(r"\s+", " ", str(x).strip())
)

despues = df["Método Envio"].unique()
print(f"\nValores DESPUÉS de limpiar ({len(despues)} únicos):")
for v in sorted(despues):
    print(f"  {repr(v)}")

print(f"\n  Valores únicos reducidos: {len(antes)} → {len(despues)}")


# ── Ejercicio 2: Unificar fechas ──────────────────────────────
print("\n" + "─" * 60)
print("EJERCICIO 2 — Unificar Mes/Dia/Año → columnas de fecha")
print("─" * 60)

df["Fecha_Salida"] = pd.to_datetime(
    df["Año Salida"].astype(str) + "-"
    + df["Mes Salida"].astype(str).str.zfill(2) + "-"
    + df["Dia Salida"].astype(str).str.zfill(2)
)

df["Fecha_Entrega"] = pd.to_datetime(
    df["Año Entrega"].astype(str) + "-"
    + df["Mes Entrega"].astype(str).str.zfill(2) + "-"
    + df["Dia Entrega"].astype(str).str.zfill(2)
)

print("\nEjemplos de fechas unificadas (primeras 5 filas):")
print(df[["Mes Salida", "Dia Salida", "Año Salida",
          "Fecha_Salida", "Mes Entrega", "Dia Entrega",
          "Año Entrega", "Fecha_Entrega"]].head(5).to_string(index=False))

rango_min = df["Fecha_Salida"].min().date()
rango_max = df["Fecha_Salida"].max().date()
print(f"\n  Rango de fechas de salida: {rango_min} → {rango_max}")


# ── Ejercicio 3: Crear ID_Venta ───────────────────────────────
print("\n" + "─" * 60)
print("EJERCICIO 3 — Crear columna ID_Venta")
print("  Formato: 2 iniciales País (mayúsc) + Año Salida + Número Venta")
print("  Ejemplo: Algeria, 2011, 2040 → AL-2011-2040")
print("─" * 60)

df["ID_Venta"] = (
    df["País"].str[:2].str.upper() + "-"
    + df["Año Salida"].astype(str) + "-"
    + df["Número Venta"].astype(str)
)

print("\nEjemplos de ID_Venta generados (primeras 8 filas):")
print(df[["País", "Año Salida", "Número Venta", "ID_Venta"]].head(8).to_string(index=False))

duplicados_id_venta = df["ID_Venta"].duplicated().sum()
print(f"\n  Total ID_Venta únicos: {df['ID_Venta'].nunique():,}")
print(f"  Duplicados detectados: {duplicados_id_venta}")


# ── Ejercicio 4: Crear ID_Cliente ─────────────────────────────
print("\n" + "─" * 60)
print("EJERCICIO 4 — Crear columna ID_Cliente")
print("  Formato: Inicial Nombre + Inicial Apellido + '-' + Número Cliente")
print("  Ejemplo: 'Toby Braunhardt', 11280 → TB-11280")
print("─" * 60)

def construir_id_cliente(nombre, numero):
    partes = str(nombre).strip().split()
    inicial_nombre = partes[0][0].upper() if len(partes) >= 1 else "X"
    inicial_apellido = partes[-1][0].upper() if len(partes) >= 2 else "X"
    return f"{inicial_nombre}{inicial_apellido}-{numero}"

df["ID_Cliente"] = df.apply(
    lambda row: construir_id_cliente(row["Nombre Cliente"], row["Número Cliente"]),
    axis=1
)

print("\nEjemplos de ID_Cliente generados (primeras 8 filas):")
print(df[["Nombre Cliente", "Número Cliente", "ID_Cliente"]].head(8).to_string(index=False))

print(f"\n  Total ID_Cliente generados: {len(df):,}")
print(f"  Clientes únicos (ID_Cliente distintos): {df['ID_Cliente'].nunique():,}")


# ── Resumen de columnas nuevas ────────────────────────────────
print("\n" + "=" * 60)
print("  RESUMEN — Columnas añadidas en este paso")
print("=" * 60)
print(f"  Columnas originales : 21")
print(f"  Columnas ahora      : {len(df.columns)}")
print("  Nuevas columnas     : Fecha_Salida, Fecha_Entrega, ID_Venta, ID_Cliente")


# ── Guardar resultado intermedio ──────────────────────────────
print("\nGuardando resultado intermedio...")
df.to_pickle("datos_paso2.pkl")
print("  Archivo guardado: datos_paso2.pkl")
print("\n¡Paso 2 completado exitosamente!")
