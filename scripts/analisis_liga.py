"""
PROY-2: Análisis estadístico de resultados de la Liga Argentina.

Lee datos/ARG.csv (football-data.co.uk), construye una tabla de posiciones
completa (Pos, PJ, G, E, P, GF, GC, DG, Pts) y genera gráficos comparativos
de rendimiento entre los equipos, todo basado en la temporada más reciente
disponible. Guarda los productos en /resultados.
"""
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
df = pd.read_csv(BASE / "datos" / "ARG.csv")

# Normalización de columnas: el feed "new" de football-data.co.uk usa nombres
# cortos (Home/Away/HG/AG/Res) para ligas extra como Argentina, mientras que
# el feed principal de ligas europeas usa nombres largos (HomeTeam/...). El
# resto del script asume los nombres largos, así que renombramos si hace falta.
if "Home" in df.columns and "HomeTeam" not in df.columns:
    df = df.rename(columns={
        "Home": "HomeTeam",
        "Away": "AwayTeam",
        "HG": "FTHG",
        "AG": "FTAG",
        "Res": "FTR",
    })

faltantes = {"HomeTeam", "AwayTeam", "FTHG", "FTAG", "FTR"} - set(df.columns)
if faltantes:
    raise SystemExit(
        f"Columnas faltantes en datos/ARG.csv: {faltantes}. "
        f"Columnas disponibles: {df.columns.tolist()}"
    )

# Date viene en formato dd/mm/yyyy; lo convertimos para poder filtrar por
# temporada (clave para que la salida no quede saturada con varios años).
df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")

# Filtramos a la temporada más reciente disponible.
if "Season" in df.columns:
    ultima_season = df["Season"].max()
    df = df[df["Season"] == ultima_season].copy()
else:
    ultima_season = df["Date"].dt.year.max()
    df = df[df["Date"].dt.year == ultima_season].copy()

print(f"Temporada analizada: {ultima_season}")
print(f"Partidos totales: {len(df)}")

# Construcción vectorizada de la tabla de posiciones:
# armamos dos sub-DataFrames (óptica local y visitante) y los concatenamos,
# después un único groupby suma los indicadores por equipo.
local = pd.DataFrame({
    "Equipo": df["HomeTeam"],
    "GF": df["FTHG"],
    "GC": df["FTAG"],
    "G": (df["FTR" ] == "H").astype(int),
    "E": (df["FTR"] == "D").astype(int),
    "P": (df["FTR"] == "A").astype(int),
})
visitante = pd.DataFrame({
    "Equipo": df["AwayTeam"],
    "GF": df["FTAG"],
    "GC": df["FTHG"],
    "G": (df["FTR"] == "A").astype(int),
    "E": (df["FTR"] == "D").astype(int),
    "P": (df["FTR"] == "H").astype(int),
})
combinado = pd.concat([local, visitante], ignore_index=True)

tabla = combinado.groupby("Equipo").agg(
    PJ=("G", "size"),
    G=("G", "sum"),
    E=("E", "sum"),
    P=("P", "sum"),
    GF=("GF", "sum"),
    GC=("GC", "sum"),
).reset_index()
tabla["DG"] = tabla["GF"] - tabla["GC"]
tabla["Pts"] = tabla["G"] * 3 + tabla["E"]

# Orden oficial estilo AFA: puntos, luego diferencia de gol, luego GF.
tabla = tabla.sort_values(["Pts", "DG", "GF"], ascending=False).reset_index(drop=True)
tabla.index = tabla.index + 1
tabla.index.name = "Pos"

tabla.to_csv(BASE / "resultados" / "tabla_posiciones.csv")
print(f"\nTabla de posiciones ({len(tabla)} equipos) guardada en /resultados/")
print(tabla.head(10))

# Indicadores agregados del torneo (resumen ejecutivo).
prom_goles = (df["FTHG"] + df["FTAG"]).mean()
total_goles = int((df["FTHG"] + df["FTAG"]).sum())
mejor_g = tabla.loc[tabla["G"].idxmax(), "Equipo"]
peor_def = tabla.loc[tabla["GC"].idxmax(), "Equipo"]
print(f"\nResumen de la temporada {ultima_season}:")
print(f"  - Promedio de goles por partido: {prom_goles:.2f}")
print(f"  - Goles totales del torneo: {total_goles}")
print(f"  - Equipo con mas partidos ganados: {mejor_g} ({tabla['G'].max()} G)")
print(f"  - Defensa mas batida: {peor_def} ({tabla['GC'].max()} GC)")

resumen = pd.DataFrame({
    "indicador": [
        "Temporada", "Partidos totales", "Goles totales",
        "Promedio goles/partido", "Equipo con mas G", "Defensa mas batida",
    ],
    "valor": [
        ultima_season, len(df), total_goles,
        round(prom_goles, 2), mejor_g, peor_def,
    ],
})
resumen.to_csv(BASE / "resultados" / "resumen_torneo.csv", index=False)

# Gráfico comparativo: dos subplots porque "rendimiento" es multidimensional.
top = tabla.head(10).copy()
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

top_pts = top[::-1]
axes[0].barh(top_pts["Equipo"], top_pts["Pts"], color="#1f77b4")
axes[0].set_xlabel("Puntos")
axes[0].set_title(f"Top 10 - Puntos (temporada {ultima_season})")
for i, v in enumerate(top_pts["Pts"]):
    axes[0].text(v + 0.5, i, str(v), va="center", fontsize=9)

labels = top["Equipo"].tolist()
axes[1].bar(labels, top["G"], label="Ganados", color="#2ca02c")
axes[1].bar(labels, top["E"], bottom=top["G"], label="Empatados", color="#ff7f0e")
axes[1].bar(labels, top["P"], bottom=(top["G"] + top["E"]), label="Perdidos", color="#d62728")
axes[1].set_xticks(range(len(labels)))
axes[1].set_xticklabels(labels, rotation=45, ha="right")
axes[1].set_ylabel("Partidos")
axes[1].set_title("Top 10 - Composicion G/E/P")
axes[1].legend(loc="upper right")

plt.suptitle(f"Liga Argentina - Analisis de rendimiento (temporada {ultima_season})", fontsize=13, fontweight="bold")
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig(BASE / "resultados" / "rendimiento_top10.png", dpi=120, bbox_inches="tight")
print("\nGrafico comparativo guardado en /resultados/rendimiento_top10.png")
