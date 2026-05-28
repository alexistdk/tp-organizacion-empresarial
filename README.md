# TP Célula Deportiva — Liga Argentina

Trabajo Práctico de **Organización Empresarial** — Universidad Tecnológica Nacional, Tecnicatura Universitaria en Programación a Distancia, 2026.

## Integrantes (Célula de Desarrollo)

| Rol | Nombre | Responsabilidad |
|-----|--------|-----------------|
| P1  | Hugo   | Líder y Organizador — estructura del repo, README, gobernanza |
| P2  | Paco   | Desarrollador Técnico — script de análisis estadístico |
| P3  | Luis   | Revisor y QA — peer review, documentación, seguridad |

## Escenario

**Escenario D — Estadísticas de Resultados Deportivos.**
Procesamiento de resultados de la **Liga Profesional Argentina** para generar
indicadores básicos del torneo: partidos ganados por equipo, tabla de
posiciones completa, promedio de goles por partido y gráfico comparativo
de rendimiento entre equipos.

## Estructura del repositorio

```
tp-organizacion-empresarial/
├── datos/
│   └── ARG.csv                    # dataset de partidos (football-data.co.uk)
├── scripts/
│   └── analisis_liga.py           # script principal de análisis
├── resultados/
│   ├── tabla_posiciones.csv       # tabla completa: Pos, Equipo, PJ, G, E, P, GF, GC, DG, Pts
│   ├── resumen_torneo.csv         # indicadores agregados del torneo
│   └── rendimiento_top10.png      # gráfico comparativo top 10
├── README.md
└── .gitignore
```

## Dataset

- **Fuente:** football-data.co.uk — Argentina Primera División.
- **URL:** https://www.football-data.co.uk/new/ARG.csv
- **Licencia:** Datos públicos. Uso educativo y de investigación.
- **Cobertura:** múltiples temporadas históricas. El script analiza
  automáticamente la temporada más reciente disponible.
- **Columnas relevantes:** `Date`, `Home`/`HomeTeam`, `Away`/`AwayTeam`,
  `HG`/`FTHG`, `AG`/`FTAG`, `Res`/`FTR`.

## Cómo ejecutar el análisis

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/alexistdk/tp-organizacion-empresarial.git
   cd tp-organizacion-empresarial
   ```
2. Asegurarse de tener Python 3.10+ con `pandas` y `matplotlib`:
   ```bash
   pip install pandas matplotlib
   ```
3. Ejecutar el script:
   ```bash
   python scripts/analisis_liga.py
   ```
4. Los productos del análisis se generan en `/resultados/`:
   - **`tabla_posiciones.csv`** — tabla completa estilo AFA con 9 columnas.
   - **`resumen_torneo.csv`** — indicadores agregados del torneo.
   - **`rendimiento_top10.png`** — gráfico comparativo en dos paneles.

## Reproducibilidad en Google Colab

El script usa rutas relativas a la raíz del repo, por lo que se puede
ejecutar tanto localmente como dentro de un notebook de Colab sin modificar
el código. El dataset se descarga desde la fuente pública sin credenciales.

## Gestión del proyecto

- **Tablero Jira:** proyecto **PROY** con 3 Issues — `PROY-1`, `PROY-2`,
  `PROY-3` — uno por rol.
- **Trazabilidad de commits:** todos los commits siguen el formato
  **Conventional Commits con ID de Jira**: `PROY-N: <descripción>`.
- **Colaboración:** integración mediante Pull Request desde la rama
  `feature/analisis-liga-argentina` hacia `main`, con revisión por pares
  y hilos de discusión técnica.

## Seguridad

- El **Personal Access Token (PAT)** de GitHub se gestiona fuera del
  repositorio (se inyecta en Colab vía `getpass`, nunca se hardcodea).
- El archivo `.gitignore` excluye archivos sensibles y temporales.
- En caso de filtración, el PAT se revoca desde GitHub y se genera uno nuevo.
