# KuenKa - Dashboard de Producción de Gas 🔥⚡

Dashboard interactivo ejecutivo para análisis de producción de gas natural desarrollado con Plotly Dash y Python.

![KuenKa Dashboard](https://img.shields.io/badge/KuenKa-Dashboard-00a693?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![Dash](https://img.shields.io/badge/Dash-Interactive-red?style=for-the-badge&logo=plotly)

## 📊 Características Principales

- **Dashboard Ejecutivo Completo**: Visualizaciones interactivas con branding KuenKa
- **Análisis Multi-dimensional**: Por año, campo, cuenca y departamento
- **Mapas Geográficos Interactivos**: Visualización de producción por departamento en Colombia
- **KPIs Dinámicos**: Métricas clave con actualización en tiempo real
- **Filtros Temporales**: Análisis flexible por rangos de años
- **Responsive Design**: Compatible con diferentes dispositivos

## 🏗️ Estructura del Dashboard

### 📈 Análisis General
- Producción total anual
- Evolución temporal con tendencias
- Variaciones porcentuales año a año
- KPIs principales (mejor año, peor año, variación)

### 🏭 Producción por Campo
- Top 10 campos productores
- Evolución temporal de campos principales
- Análisis individual de campos que concentran el 70% de la producción
- Participación porcentual por campo

### 🌊 Producción por Cuenca
- Comparación entre cuencas
- Análisis de composición con gráficas de área apilada
- Evolución temporal por cuenca
- Análisis individual detallado

### 🗺️ Producción por Departamento
- Mapa interactivo de Colombia con burbujas proporcionales
- Ranking de departamentos productores
- Concentración geográfica de la producción
- Análisis de tendencias departamentales

## 🛠️ Tecnologías Utilizadas

- **Python 3.8+**
- **Plotly Dash**: Framework para aplicaciones web interactivas
- **Pandas**: Manipulación y análisis de datos
- **Plotly Express**: Visualizaciones interactivas
- **Dash Bootstrap Components**: Componentes UI responsivos
- **OpenPyXL**: Lectura de archivos Excel

## 🚀 Instalación y Configuración

### Prerrequisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Instalación Local

1. **Clonar el repositorio:**
```bash
git clone https://github.com/tu-usuario/dashboard-gas-kuenka.git
cd dashboard-gas-kuenka
```

2. **Crear entorno virtual (recomendado):**
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

3. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

4. **Configurar archivos de datos:**
   - Coloca los archivos Excel en la ruta especificada en el código
   - Asegúrate de que los archivos `produccion_gas_resumenes.xlsx` y `serie_tiempo_gas.xlsx` estén disponibles

5. **Ejecutar la aplicación:**
```bash
python dashboard_gas_completo.py
```

6. **Acceder al dashboard:**
   - Abre tu navegador en: `http://localhost:8052`

## 📁 Estructura de Archivos Requeridos

```
📂 Datos requeridos:
├── produccion_gas_resumenes.xlsx
│   ├── Sheet: Totales_Anuales
│   ├── Sheet: Anual_Por_Cuenca
│   ├── Sheet: Anual_Por_Campo
│   └── Sheet: Sumatoria_Anual_Producción_Gas
└── serie_tiempo_gas.xlsx (opcional para análisis temporal extendido)
```

### Columnas Requeridas en Excel:
- `AÑO`: Año de producción
- `PRODUCCION FISCALIZADA`: Volumen de producción
- `CAMPO_LIMPIO`: Nombre del campo (para análisis por campo)
- `CUENCA`: Nombre de la cuenca (para análisis por cuenca)
- `DEPARTAMENTO`: Nombre del departamento (para análisis geográfico)

## 🌐 Despliegue en Producción

### Heroku
```bash
# Instalar Heroku CLI y luego:
heroku create tu-app-dashboard-gas
git push heroku main
```

### Railway
```bash
# Conectar con Railway y hacer deploy automático desde GitHub
```

### Render
- Conectar repositorio GitHub
- Configurar build command: `pip install -r requirements.txt`
- Configurar start command: `python dashboard_gas_completo.py`

## 🎨 Personalización y Branding

El dashboard utiliza la paleta de colores oficial de KuenKa:
- **Color Primario**: `#00a693` (Verde KuenKa)
- **Color Secundario**: `#ffc107` (Amarillo KuenKa)
- **Color de Texto**: `#2c3e50` (Azul oscuro)
- **Color de Fondo**: `#f8f9fa` (Fondo claro)

### Modificar Colores
```python
# En el archivo dashboard_gas_completo.py, líneas 45-50
color_primario = '#00a693'  # Cambiar aquí
color_secundario = '#ffc107'  # Cambiar aquí
color_texto = '#2c3e50'  # Cambiar aquí
```

## 🔧 Configuración Avanzada

### Cambiar Puerto de Ejecución
```python
# Línea final del archivo
port = int(os.environ.get('PORT', 8052))  # Cambiar 8052 por el puerto deseado
```

### Modificar Rutas de Archivos
```python
# Líneas 8-9
ruta_excel = r'NUEVA_RUTA\produccion_gas_resumenes.xlsx'
ruta_serie_tiempo = r'NUEVA_RUTA\serie_tiempo_gas.xlsx'
```

## 📊 Métricas y KPIs Disponibles

- **Producción Total**: Suma acumulada de toda la producción
- **Mejor Año**: Año con mayor producción registrada
- **Peor Año**: Año con menor producción registrada
- **Variación Anual**: Cambio porcentual respecto al año anterior
- **Concentración Geográfica**: Porcentaje de producción en top 3 departamentos
- **Participación por Campo/Cuenca**: Distribución porcentual de la producción

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE.md](LICENSE.md) para detalles.

## 🆘 Soporte y Contacto

Si tienes preguntas o necesitas soporte:
- 📧 Email: soporte@kuenka.com
- 🐛 Issues: Usar el sistema de issues de GitHub
- 📖 Documentación: Ver este README

## 📈 Roadmap Futuro

- [ ] Integración con APIs en tiempo real
- [ ] Exportación de reportes en PDF
- [ ] Alertas automáticas por thresholds
- [ ] Dashboard móvil nativo
- [ ] Análisis predictivo con ML
- [ ] Integración con bases de datos

---

**Desarrollado con ❤️ por el equipo KuenKa**

![KuenKa Logo](https://img.shields.io/badge/KuenKa-Analytics-00a693?style=flat-square)