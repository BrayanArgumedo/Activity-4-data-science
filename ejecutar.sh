#!/bin/bash
# ─────────────────────────────────────────────────────────────
#  Script de ejecución completa — Actividad 4 Ciencia de Datos
# ─────────────────────────────────────────────────────────────

echo ""
echo "╔══════════════════════════════════════════════════════╗"
echo "║   Actividad 4 — Análisis de Ventas Supermercado     ║"
echo "║   Ciencia de Datos · Universidad de Cartagena       ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""

source venv/bin/activate

echo "▶  Paso 2 — Funciones de Texto..."
python3 paso2_funciones_texto.py
echo ""

echo "▶  Paso 3 — Funciones de Búsqueda..."
python3 paso3_funciones_busqueda.py
echo ""

echo "▶  Paso 4 — Modelo Estrella..."
python3 paso4_modelo_estrella.py
echo ""

echo "▶  Paso 5 — Diagrama del Modelo Estrella..."
python3 paso5_diagrama_estrella.py
echo ""

echo "▶  Paso 6 — Tablas Dinámicas..."
python3 paso6_tablas_dinamicas.py
echo ""

echo "╔══════════════════════════════════════════════════════╗"
echo "║   ¡Actividad completada! Archivos generados:        ║"
echo "║   · Modelo_Estrella_Ventas.xlsx                     ║"
echo "║   · Diagrama_Modelo_Estrella.png                    ║"
echo "║   · Tablas_Dinamicas_Ventas.xlsx                    ║"
echo "╚══════════════════════════════════════════════════════╝"
