import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import matplotlib.patheffects as pe

# ─────────────────────────────────────────────
#  PASO 5 — Diagrama del Modelo de Datos Estrella
# ─────────────────────────────────────────────

print("=" * 60)
print("  PASO 5 — DIAGRAMA MODELO ESTRELLA")
print("=" * 60)

# ══════════════════════════════════════════════
#  DEFINICIÓN DE TABLAS Y COLUMNAS
# ══════════════════════════════════════════════
#  Tipos: PK = clave primaria, FK = clave foránea,
#         M  = medida,         A  = atributo descriptivo

TABLAS = {
    "Hechos_Ventas": {
        "pos":     (0.50, 0.47),
        "color_h": "#C0392B",
        "color_b": "#FADBD8",
        "ancho":   0.195,
        "columnas": [
            ("ID_Hecho",           "PK"),
            ("ID_Venta",           "A"),
            ("Número_Venta",       "A"),
            ("FK_Tiempo_Salida",   "FK"),
            ("FK_Tiempo_Entrega",  "FK"),
            ("FK_Cliente",         "FK"),
            ("FK_Producto",        "FK"),
            ("FK_Region",          "FK"),
            ("Método_Envio",       "A"),
            ("Prioridad_Envio",    "A"),
            ("Ventas",             "M"),
            ("Cantidad",           "M"),
            ("Descuento",          "M"),
            ("Utilidad",           "M"),
            ("Costo_Envio",        "M"),
        ],
    },
    "Dim_Tiempo": {
        "pos":     (0.50, 0.82),
        "color_h": "#1A5276",
        "color_b": "#D6EAF8",
        "ancho":   0.175,
        "columnas": [
            ("ID_Tiempo",   "PK"),
            ("Fecha",       "A"),
            ("Año",         "A"),
            ("Trimestre",   "A"),
            ("Mes",         "A"),
            ("Nombre_Mes",  "A"),
            ("Dia",         "A"),
            ("Dia_Semana",  "A"),
        ],
    },
    "Dim_Cliente": {
        "pos":     (0.115, 0.47),
        "color_h": "#1E8449",
        "color_b": "#D5F5E3",
        "ancho":   0.165,
        "columnas": [
            ("ID_Cliente",      "PK"),
            ("Número_Cliente",  "A"),
            ("Nombre_Cliente",  "A"),
            ("Segmento",        "A"),
        ],
    },
    "Dim_Producto": {
        "pos":     (0.885, 0.47),
        "color_h": "#6C3483",
        "color_b": "#E8DAEF",
        "ancho":   0.175,
        "columnas": [
            ("ID_Producto",    "PK"),
            ("Categoría",      "A"),
            ("Sub_Categoría",  "A"),
            ("Nombre_Producto","A"),
        ],
    },
    "Dim_Region": {
        "pos":     (0.50, 0.095),
        "color_h": "#784212",
        "color_b": "#FDEBD0",
        "ancho":   0.165,
        "columnas": [
            ("ID_Region", "PK"),
            ("Ciudad",    "A"),
            ("Estado",    "A"),
            ("País",      "A"),
            ("Mercado",   "A"),
            ("Región",    "A"),
        ],
    },
}

# Colores por tipo de campo
COLOR_TIPO = {
    "PK": "#F1C40F",   # dorado
    "FK": "#E74C3C",   # rojo
    "M":  "#2ECC71",   # verde
    "A":  "#FFFFFF",   # blanco
}
LABEL_TIPO = {"PK": "PK", "FK": "FK", "M": "M", "A": ""}

ALTO_FILA   = 0.023   # altura por fila de columna
ALTO_HEADER = 0.033   # altura del encabezado de tabla
PADDING     = 0.005   # padding interno


# ══════════════════════════════════════════════
#  FUNCIÓN: dibujar una tabla
# ══════════════════════════════════════════════
def dibujar_tabla(ax, nombre, datos):
    cx, cy   = datos["pos"]
    ancho    = datos["ancho"]
    columnas = datos["columnas"]
    color_h  = datos["color_h"]
    color_b  = datos["color_b"]

    n_cols = len(columnas)
    alto_total = ALTO_HEADER + n_cols * ALTO_FILA + PADDING * 2

    x0 = cx - ancho / 2
    y0 = cy - alto_total / 2

    # Sombra
    sombra = FancyBboxPatch(
        (x0 + 0.004, y0 - 0.004), ancho, alto_total,
        boxstyle="round,pad=0.005",
        linewidth=0, facecolor="#999999", alpha=0.35,
        transform=ax.transAxes, zorder=2,
    )
    ax.add_patch(sombra)

    # Cuerpo de la tabla
    cuerpo = FancyBboxPatch(
        (x0, y0), ancho, alto_total,
        boxstyle="round,pad=0.005",
        linewidth=1.5, edgecolor="#333333", facecolor=color_b,
        transform=ax.transAxes, zorder=3,
    )
    ax.add_patch(cuerpo)

    # Encabezado (header)
    header = FancyBboxPatch(
        (x0, y0 + alto_total - ALTO_HEADER), ancho, ALTO_HEADER,
        boxstyle="round,pad=0.003",
        linewidth=0, facecolor=color_h,
        transform=ax.transAxes, zorder=4,
    )
    ax.add_patch(header)

    # Texto del header
    ax.text(cx, y0 + alto_total - ALTO_HEADER / 2, nombre,
            ha="center", va="center", fontsize=9.5, fontweight="bold",
            color="white", transform=ax.transAxes, zorder=5)

    # Línea divisoria bajo el header
    y_linea = y0 + alto_total - ALTO_HEADER
    ax.plot([x0, x0 + ancho], [y_linea, y_linea],
            color="#333333", linewidth=1.2, transform=ax.transAxes, zorder=5)

    # Filas de columnas
    for i, (col_nombre, col_tipo) in enumerate(columnas):
        y_fila = y0 + alto_total - ALTO_HEADER - (i + 1) * ALTO_FILA
        y_centro = y_fila + ALTO_FILA / 2

        # Línea separadora entre filas
        if i > 0:
            ax.plot([x0 + PADDING, x0 + ancho - PADDING],
                    [y_fila + ALTO_FILA, y_fila + ALTO_FILA],
                    color="#CCCCCC", linewidth=0.5,
                    transform=ax.transAxes, zorder=4)

        # Badge de tipo (PK, FK, M)
        if col_tipo in ("PK", "FK", "M"):
            badge_w, badge_h = 0.028, 0.018
            badge = FancyBboxPatch(
                (x0 + PADDING, y_centro - badge_h / 2),
                badge_w, badge_h,
                boxstyle="round,pad=0.002",
                linewidth=0.8, edgecolor="#666666",
                facecolor=COLOR_TIPO[col_tipo],
                transform=ax.transAxes, zorder=5,
            )
            ax.add_patch(badge)
            ax.text(x0 + PADDING + badge_w / 2, y_centro,
                    LABEL_TIPO[col_tipo],
                    ha="center", va="center", fontsize=5.5,
                    fontweight="bold", color="#333333",
                    transform=ax.transAxes, zorder=6)
            x_texto = x0 + PADDING + badge_w + 0.007
        else:
            x_texto = x0 + PADDING + 0.010

        # Nombre de columna
        peso = "bold" if col_tipo == "PK" else "normal"
        ax.text(x_texto, y_centro, col_nombre,
                ha="left", va="center", fontsize=7.8,
                fontweight=peso, color="#1A1A1A",
                transform=ax.transAxes, zorder=5)

    # Devolver coordenadas del borde de la caja (para conectar líneas)
    return {
        "x0": x0, "x1": x0 + ancho,
        "y0": y0, "y1": y0 + alto_total,
        "cx": cx, "cy": cy,
    }


# ══════════════════════════════════════════════
#  FUNCIÓN: dibujar línea de relación
# ══════════════════════════════════════════════
def conectar(ax, box_origen, box_destino, lado_origen, lado_destino, etiqueta=""):
    puntos = {
        "arriba":    (box_origen["cx"], box_origen["y1"]),
        "abajo":     (box_origen["cx"], box_origen["y0"]),
        "derecha":   (box_origen["x1"], box_origen["cy"]),
        "izquierda": (box_origen["x0"], box_origen["cy"]),
    }
    destinos = {
        "arriba":    (box_destino["cx"], box_destino["y0"]),
        "abajo":     (box_destino["cx"], box_destino["y1"]),
        "derecha":   (box_destino["x0"], box_destino["cy"]),
        "izquierda": (box_destino["x1"], box_destino["cy"]),
    }
    x1, y1 = puntos[lado_origen]
    x2, y2 = destinos[lado_destino]

    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                xycoords="axes fraction", textcoords="axes fraction",
                arrowprops=dict(
                    arrowstyle="-|>",
                    color="#555555",
                    lw=1.8,
                    mutation_scale=14,
                    connectionstyle="arc3,rad=0.0",
                ),
                zorder=2)

    # Etiqueta "1:N" desplazada al 25% del recorrido (cerca del origen)
    if etiqueta:
        offset = 0.22  # posición relativa del 0 al 1
        lx = x1 + (x2 - x1) * offset
        ly = y1 + (y2 - y1) * offset
        # Desplazamiento perpendicular pequeño para no tapar la línea
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        perp_x = 0.025 if dy > dx else 0.0
        perp_y = 0.015 if dx > dy else 0.0
        ax.text(lx + perp_x, ly + perp_y, etiqueta,
                ha="center", va="center",
                fontsize=7.5, color="#C0392B", fontweight="bold",
                transform=ax.transAxes, zorder=6,
                bbox=dict(boxstyle="round,pad=0.18", fc="white",
                          ec="#C0392B", lw=0.9, alpha=0.92))


# ══════════════════════════════════════════════
#  CONSTRUCCIÓN DEL DIAGRAMA
# ══════════════════════════════════════════════
print("\nGenerando diagrama...")

fig, ax = plt.subplots(figsize=(22, 16))
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")

# Fondo degradado suave
fig.patch.set_facecolor("#F0F4F8")
ax.set_facecolor("#F0F4F8")

# Título principal
ax.text(0.5, 0.972,
        "Modelo de Datos Estrella  ·  Dataset Ventas Supermercado",
        ha="center", va="center", fontsize=13, fontweight="bold",
        color="#1A1A2E", transform=ax.transAxes, clip_on=False,
        bbox=dict(boxstyle="round,pad=0.45", fc="white",
                  ec="#1A1A2E", lw=1.5))

# Subtítulo
ax.text(0.5, 0.940,
        "Actividad 4  ·  Ciencia de Datos  ·  Universidad de Cartagena",
        ha="center", va="center", fontsize=8.5, color="#555555",
        transform=ax.transAxes)

# Dibujar tablas y guardar coordenadas
cajas = {}
for nombre, datos in TABLAS.items():
    cajas[nombre] = dibujar_tabla(ax, nombre, datos)

# Conectar dimensiones con la tabla de hechos
hec = cajas["Hechos_Ventas"]
conectar(ax, hec, cajas["Dim_Tiempo"],    "arriba",    "abajo",    "1:N")
conectar(ax, hec, cajas["Dim_Cliente"],   "izquierda", "derecha",  "1:N")
conectar(ax, hec, cajas["Dim_Producto"],  "derecha",   "izquierda","1:N")
conectar(ax, hec, cajas["Dim_Region"],    "abajo",     "arriba",   "1:N")

# ── LEYENDA ───────────────────────────────────
leyenda_items = [
    mpatches.Patch(facecolor="#F1C40F", edgecolor="#666", label="PK  Clave Primaria"),
    mpatches.Patch(facecolor="#E74C3C", edgecolor="#666", label="FK  Clave Foránea"),
    mpatches.Patch(facecolor="#2ECC71", edgecolor="#666", label="M   Medida"),
    mpatches.Patch(facecolor="#FFFFFF", edgecolor="#999", label="A   Atributo Descriptivo"),
]
ax.legend(handles=leyenda_items,
          loc="lower left", bbox_to_anchor=(0.01, 0.01),
          fontsize=8, title="Tipos de Campo",
          title_fontsize=8.5, framealpha=0.95,
          edgecolor="#AAAAAA", fancybox=True)

# ── Guardar ───────────────────────────────────
nombre_archivo = "Diagrama_Modelo_Estrella.png"
plt.savefig(nombre_archivo, dpi=150, bbox_inches="tight",
            facecolor=fig.get_facecolor())
plt.close()

print(f"  Diagrama guardado: {nombre_archivo}")
print("\n¡Paso 5 completado exitosamente!")
