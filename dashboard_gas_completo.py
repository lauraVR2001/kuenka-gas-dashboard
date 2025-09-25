import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Output, Input
import dash_bootstrap_components as dbc
from datetime import datetime

# Configuración de datos - Análisis Real con tus archivos Excel
import os

def cargar_datos():
    """Cargar datos reales de Excel con manejo de rutas para local y producción"""
    
    # Rutas para desarrollo local
    ruta_local_excel = r'D:\Analisis producción de gas 2025\Bases_produccion_gas\produccion_gas_resumenes.xlsx'
    ruta_local_serie = r'D:\Analisis producción de gas 2025\Bases_produccion_gas\serie_tiempo_gas.xlsx'
    
    # Rutas para producción (archivos en el mismo directorio)
    ruta_prod_excel = 'produccion_gas_resumenes.xlsx'
    ruta_prod_serie = 'serie_tiempo_gas.xlsx'
    
    # Detectar si estamos en local o producción
    if os.path.exists(ruta_local_excel):
        # Desarrollo local
        ruta_excel = ruta_local_excel
        ruta_serie_tiempo = ruta_local_serie
        print("🏠 Cargando datos desde desarrollo local")
    else:
        # Producción
        ruta_excel = ruta_prod_excel
        ruta_serie_tiempo = ruta_prod_serie
        print("☁️ Cargando datos desde producción")
    
    try:
        # Cargar datos principales
        df_anual = pd.read_excel(ruta_excel, sheet_name='Totales_Anuales')
        df_anual.columns = df_anual.columns.str.strip()

        df_cuenca = pd.read_excel(ruta_excel, sheet_name='Anual_Por_Cuenca')
        df_cuenca.columns = df_cuenca.columns.str.strip()

        df_campo = pd.read_excel(ruta_excel, sheet_name='Anual_Por_Campo')
        df_campo.columns = df_campo.columns.str.strip()

        df_departamento = pd.read_excel(ruta_excel, sheet_name='Sumatoria_Anual_Producción_Gas')
        df_departamento.columns = df_departamento.columns.str.strip()
        
        print(f"✅ Datos cargados exitosamente desde: {ruta_excel}")
        return df_anual, df_cuenca, df_campo, df_departamento
        
    except FileNotFoundError as e:
        print(f"❌ Error: No se encontraron los archivos Excel: {e}")
        print("📧 Contacta al administrador para configurar los archivos de datos")
        # Retornar DataFrames vacíos para evitar errores
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
    except Exception as e:
        print(f"❌ Error inesperado al cargar datos: {e}")
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

# Cargar datos reales
df_anual, df_cuenca, df_campo, df_departamento = cargar_datos()

# Limpiar datos
df_anual = df_anual.dropna(subset=['PRODUCCION FISCALIZADA'])
df_cuenca = df_cuenca.dropna(subset=['PRODUCCION FISCALIZADA'])
df_campo = df_campo.dropna(subset=['PRODUCCION FISCALIZADA'])
df_departamento = df_departamento.dropna(subset=['PRODUCCION FISCALIZADA'])

# Convertir AÑO a numérico
df_anual['AÑO'] = pd.to_numeric(df_anual['AÑO'], errors='coerce')
df_cuenca['AÑO'] = pd.to_numeric(df_cuenca['AÑO'], errors='coerce')
df_campo['AÑO'] = pd.to_numeric(df_campo['AÑO'], errors='coerce')
df_departamento['AÑO'] = pd.to_numeric(df_departamento['AÑO'], errors='coerce')

# Remover filas con años inválidos
df_anual = df_anual.dropna(subset=['AÑO'])
df_cuenca = df_cuenca.dropna(subset=['AÑO'])
df_campo = df_campo.dropna(subset=['AÑO'])
df_departamento = df_departamento.dropna(subset=['AÑO'])

# Configuración de colores y estilo - KuenKa Branding
colores = ['#00a693', '#008b7a', '#006b5d', '#004d40', '#66c2b3', '#4db8a6', '#33ad99', '#1a9b8c', '#80ccc0', '#99d6cc', '#b3e0d9']
color_primario = '#00a693'  # Verde KuenKa principal
color_secundario = '#ffc107'  # Amarillo KuenKa
color_texto = '#2c3e50'  # Azul oscuro para texto
color_fondo = '#f8f9fa'  # Fondo claro

# Inicializar app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "KuenKa - Gas Production Executive Dashboard"
server = app.server  # Necesario para el despliegue

# Layout principal con branding KuenKa
app.layout = dbc.Container([
    # Encabezado con branding KuenKa
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Div([
                    html.H1("KuenKa", 
                           style={'color': color_primario, 'fontWeight': 'bold', 'fontSize': '42px', 'marginBottom': '0'}),
                    html.H3("Gas Production Executive Dashboard", 
                           style={'color': color_texto, 'fontWeight': '300', 'fontSize': '24px', 'marginTop': '0'}),
                    html.P("� Real Production Data Analysis 2013-2024", 
                           style={'color': color_primario, 'fontWeight': '500', 'fontSize': '14px', 'marginTop': '10px', 'fontStyle': 'italic'})
                ], className="text-center")
            ], style={
                'background': f'linear-gradient(135deg, {color_fondo} 0%, #ffffff 100%)',
                'padding': '30px',
                'borderRadius': '15px',
                'boxShadow': '0 8px 32px rgba(0, 166, 147, 0.1)',
                'border': f'1px solid {color_primario}20',
                'marginBottom': '30px'
            })
        ], width=12)
    ]),
    
    # Filtro de año con estilo KuenKa
    dbc.Row([
        dbc.Col([
            html.Label("Filter by Year:", style={'fontWeight': 'bold', 'color': color_texto, 'fontSize': '18px', 'marginBottom': '15px'}),
            dcc.RangeSlider(
                id='year-slider',
                min=int(df_anual['AÑO'].min()),
                max=int(df_anual['AÑO'].max()),
                value=[int(df_anual['AÑO'].min()), int(df_anual['AÑO'].max())],
                marks={year: {'label': str(year), 'style': {'color': color_texto, 'fontSize': '14px', 'fontWeight': '500'}} 
                       for year in range(int(df_anual['AÑO'].min()), int(df_anual['AÑO'].max()) + 1)},
                step=1,
                tooltip={"placement": "bottom", "always_visible": True}
            )
        ], width=12, style={
            'padding': '20px 30px', 
            'backgroundColor': 'white', 
            'borderRadius': '10px',
            'boxShadow': '0 4px 12px rgba(0, 0, 0, 0.08)',
            'marginBottom': '20px'
        })
    ], className="mb-4"),
    
    # Pestañas con estilo KuenKa
    dcc.Tabs(id="tabs", value="tab-general", 
             style={'height': '60px', 'marginBottom': '20px'},
             children=[
        dcc.Tab(label="General Analysis", value="tab-general", 
                style={
                    'backgroundColor': 'white', 'color': color_texto, 'padding': '15px 30px', 
                    'fontSize': '16px', 'fontWeight': '600', 'border': f'2px solid {color_primario}20',
                    'borderRadius': '8px 8px 0 0', 'marginRight': '5px'
                },
                selected_style={
                    'backgroundColor': color_primario, 'color': 'white', 'padding': '15px 30px',
                    'fontSize': '16px', 'fontWeight': '600', 'border': f'2px solid {color_primario}',
                    'borderRadius': '8px 8px 0 0', 'marginRight': '5px'
                }),
        dcc.Tab(label="Production by Field", value="tab-campo",
                style={
                    'backgroundColor': 'white', 'color': color_texto, 'padding': '15px 30px',
                    'fontSize': '16px', 'fontWeight': '600', 'border': f'2px solid {color_primario}20',
                    'borderRadius': '8px 8px 0 0', 'marginRight': '5px'
                },
                selected_style={
                    'backgroundColor': color_primario, 'color': 'white', 'padding': '15px 30px',
                    'fontSize': '16px', 'fontWeight': '600', 'border': f'2px solid {color_primario}',
                    'borderRadius': '8px 8px 0 0', 'marginRight': '5px'
                }),
        dcc.Tab(label="Production by Basin", value="tab-cuenca",
                style={
                    'backgroundColor': 'white', 'color': color_texto, 'padding': '15px 30px',
                    'fontSize': '16px', 'fontWeight': '600', 'border': f'2px solid {color_primario}20',
                    'borderRadius': '8px 8px 0 0', 'marginRight': '5px'
                },
                selected_style={
                    'backgroundColor': color_primario, 'color': 'white', 'padding': '15px 30px',
                    'fontSize': '16px', 'fontWeight': '600', 'border': f'2px solid {color_primario}',
                    'borderRadius': '8px 8px 0 0', 'marginRight': '5px'
                }),
        dcc.Tab(label="Production by Department", value="tab-departamento",
                style={
                    'backgroundColor': 'white', 'color': color_texto, 'padding': '15px 30px',
                    'fontSize': '16px', 'fontWeight': '600', 'border': f'2px solid {color_primario}20',
                    'borderRadius': '8px 8px 0 0'
                },
                selected_style={
                    'backgroundColor': color_primario, 'color': 'white', 'padding': '15px 30px',
                    'fontSize': '16px', 'fontWeight': '600', 'border': f'2px solid {color_primario}',
                    'borderRadius': '8px 8px 0 0'
                })
    ]),
    
    # Contenido de las pestañas
    html.Div(id="tab-content", style={'padding': '0 10px'})
    
], fluid=True, style={
    'backgroundColor': color_fondo, 
    'minHeight': '100vh', 
    'padding': '20px',
    'fontFamily': '"Segoe UI", Tahoma, Geneva, Verdana, sans-serif'
})

# Callbacks para las pestañas
@app.callback(Output('tab-content', 'children'),
              [Input('tabs', 'value'),
               Input('year-slider', 'value')])
def render_content(active_tab, year_range):
    # Filtrar datos por año
    df_anual_filtered = df_anual[
        (df_anual['AÑO'] >= year_range[0]) & 
        (df_anual['AÑO'] <= year_range[1])
    ]
    
    df_cuenca_filtered = df_cuenca[
        (df_cuenca['AÑO'] >= year_range[0]) & 
        (df_cuenca['AÑO'] <= year_range[1])
    ]
    
    df_campo_filtered = df_campo[
        (df_campo['AÑO'] >= year_range[0]) & 
        (df_campo['AÑO'] <= year_range[1])
    ]
    
    df_departamento_filtered = df_departamento[
        (df_departamento['AÑO'] >= year_range[0]) & 
        (df_departamento['AÑO'] <= year_range[1])
    ]
    
    if active_tab == 'tab-general':
        return crear_tab_general(df_anual_filtered)
    elif active_tab == 'tab-campo':
        return crear_tab_campo(df_campo_filtered)
    elif active_tab == 'tab-cuenca':
        return crear_tab_cuenca(df_cuenca_filtered)
    elif active_tab == 'tab-departamento':
        return crear_tab_departamento(df_departamento_filtered)

def crear_tab_general(df_filtered):
    """Create general tab content"""
    
    # KPIs
    if not df_filtered.empty:
        prod_total = df_filtered['PRODUCCION FISCALIZADA'].sum()
        mejor_año = df_filtered.loc[df_filtered['PRODUCCION FISCALIZADA'].idxmax()]
        peor_año = df_filtered.loc[df_filtered['PRODUCCION FISCALIZADA'].idxmin()]
        var_ult = df_filtered['PRODUCCION FISCALIZADA'].pct_change(fill_method=None).iloc[-1] * 100 if len(df_filtered) > 1 else 0
    else:
        prod_total = 0
        mejor_año = pd.Series({'AÑO': 'N/A', 'PRODUCCION FISCALIZADA': 0})
        peor_año = pd.Series({'AÑO': 'N/A', 'PRODUCCION FISCALIZADA': 0})
        var_ult = 0
    
    # Gráfica de línea de tiempo
    fig_timeline = px.line(df_filtered, x='AÑO', y='PRODUCCION FISCALIZADA',
                          title='Timeline - Annual Gas Production',
                          markers=True, line_shape='spline')
    fig_timeline.update_traces(line=dict(color=color_primario, width=4),
                              marker=dict(size=8, color=color_primario))
    fig_timeline.update_layout(
        plot_bgcolor='white', paper_bgcolor='white',
        font=dict(family='Segoe UI', size=14, color=color_texto),
        title_font=dict(size=20, color=color_texto, family='Segoe UI'),
        xaxis_title='Year', yaxis_title='Fiscalized Production',
        yaxis_tickformat=',.0f',
        xaxis=dict(dtick=1, tickmode='linear')
    )
    
    # Gráfica de barras
    fig_barras = px.bar(df_filtered, x='AÑO', y='PRODUCCION FISCALIZADA',
                       title='Annual Production - Bar Chart View',
                       text_auto='.2s')
    fig_barras.update_traces(marker_color=color_primario, texttemplate='%{y:,.0f}', textposition='outside')
    fig_barras.update_layout(
        plot_bgcolor='white', paper_bgcolor='white',
        font=dict(family='Segoe UI', size=14, color=color_texto),
        title_font=dict(size=20, color=color_texto, family='Segoe UI'),
        xaxis_title='Year', yaxis_title='Fiscalized Production',
        yaxis_tickformat=',.0f',
        showlegend=False,
        xaxis=dict(dtick=1, tickmode='linear'),
        yaxis=dict(range=[0, df_filtered['PRODUCCION FISCALIZADA'].max() * 1.15])
    )
    
    # Gráfica de variación porcentual
    var_pct = df_filtered[['AÑO', 'PRODUCCION FISCALIZADA']].copy()
    var_pct['VARIACION %'] = var_pct['PRODUCCION FISCALIZADA'].pct_change(fill_method=None) * 100
    
    fig_variacion = px.line(var_pct, x='AÑO', y='VARIACION %', 
                           markers=True, title='Annual Percentage Variation')
    fig_variacion.update_traces(line=dict(color=color_secundario, width=3),
                               marker=dict(size=6, color=color_secundario))
    fig_variacion.update_layout(
        plot_bgcolor='white', paper_bgcolor='white',
        font=dict(family='Segoe UI', size=14, color=color_texto),
        title_font=dict(size=20, color=color_secundario, family='Segoe UI'),
        xaxis_title='Year', yaxis_title='Variation %',
        xaxis=dict(dtick=1, tickmode='linear')
    )
    
    return [
        # KPIs con estilo KuenKa
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Total Production", className="card-title text-center mb-3", 
                               style={'color': color_texto, 'fontSize': '16px', 'fontWeight': '600'}),
                        html.H2(f"{prod_total:,.0f}", className="text-center", 
                               style={'fontSize': '28px', 'fontWeight': 'bold', 'color': color_primario})
                    ], style={'padding': '25px'})
                ], style={
                    'boxShadow': '0 8px 32px rgba(0, 166, 147, 0.15)', 
                    'border': f'1px solid {color_primario}30', 
                    'borderRadius': '15px',
                    'background': 'linear-gradient(135deg, #ffffff 0%, #f8fffd 100%)'
                })
            ], width=3, className="mb-3"),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Best Year", className="card-title text-center mb-3", 
                               style={'color': color_texto, 'fontSize': '16px', 'fontWeight': '600'}),
                        html.H2(f"{mejor_año['AÑO']:.0f}", className="text-center", 
                               style={'fontSize': '28px', 'fontWeight': 'bold', 'color': color_primario}),
                        html.P(f"{mejor_año['PRODUCCION FISCALIZADA']:,.0f}", className="text-center text-muted",
                              style={'fontSize': '14px', 'marginBottom': '0'})
                    ], style={'padding': '25px'})
                ], style={
                    'boxShadow': '0 8px 32px rgba(0, 166, 147, 0.15)', 
                    'border': f'1px solid {color_primario}30', 
                    'borderRadius': '15px',
                    'background': 'linear-gradient(135deg, #ffffff 0%, #f8fffd 100%)'
                })
            ], width=3, className="mb-3"),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Lowest Year", className="card-title text-center mb-3", 
                               style={'color': color_texto, 'fontSize': '16px', 'fontWeight': '600'}),
                        html.H2(f"{peor_año['AÑO']:.0f}", className="text-center", 
                               style={'fontSize': '28px', 'fontWeight': 'bold', 'color': '#ff9800'}),
                        html.P(f"{peor_año['PRODUCCION FISCALIZADA']:,.0f}", className="text-center text-muted",
                              style={'fontSize': '14px', 'marginBottom': '0'})
                    ], style={'padding': '25px'})
                ], style={
                    'boxShadow': '0 8px 32px rgba(255, 152, 0, 0.15)', 
                    'border': '1px solid #ff980030', 
                    'borderRadius': '15px',
                    'background': 'linear-gradient(135deg, #ffffff 0%, #fff8f0 100%)'
                })
            ], width=3, className="mb-3"),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Last Year Var.", className="card-title text-center mb-3", 
                               style={'color': color_texto, 'fontSize': '16px', 'fontWeight': '600'}),
                        html.H2(f"{var_ult:.1f}%", 
                                className="text-center",
                                style={'fontSize': '28px', 'fontWeight': 'bold', 
                                      'color': color_primario if var_ult >= 0 else '#e74c3c'})
                    ], style={'padding': '25px'})
                ], style={
                    'boxShadow': f'0 8px 32px rgba(0, 166, 147, 0.15)' if var_ult >= 0 else '0 8px 32px rgba(231, 76, 60, 0.15)', 
                    'border': f'1px solid {color_primario if var_ult >= 0 else "#e74c3c"}30', 
                    'borderRadius': '15px',
                    'background': f'linear-gradient(135deg, #ffffff 0%, {"#f8fffd" if var_ult >= 0 else "#fdf8f8"} 100%)'
                })
            ], width=3, className="mb-3")
        ], className="mb-5", style={'marginLeft': '10px', 'marginRight': '10px'}),
        
        # Gráficas
        dbc.Row([
            dbc.Col([
                dcc.Graph(figure=fig_timeline, style={'height': '400px'})
            ], width=12)
        ], className="mb-3"),
        
        dbc.Row([
            dbc.Col([
                dcc.Graph(figure=fig_barras, style={'height': '400px'})
            ], width=6),
            dbc.Col([
                dcc.Graph(figure=fig_variacion, style={'height': '400px'})
            ], width=6)
        ])
    ]

def crear_tab_campo(df_filtered):
    """Create field tab content"""
    
    if df_filtered.empty:
        return [html.P("No data available for the selected range", style={'color': color_texto, 'fontSize': '16px', 'textAlign': 'center'})]
    
    # Top 10 campos por producción total
    top_campos = df_filtered.groupby('CAMPO_LIMPIO')['PRODUCCION FISCALIZADA'].sum().nlargest(10).reset_index()
    
    # Calcular campos que concentran el 70% de la producción
    produccion_total = df_filtered['PRODUCCION FISCALIZADA'].sum()
    campos_totales = df_filtered.groupby('CAMPO_LIMPIO')['PRODUCCION FISCALIZADA'].sum().sort_values(ascending=False).reset_index()
    campos_totales['ACUMULADO'] = campos_totales['PRODUCCION FISCALIZADA'].cumsum()
    campos_totales['PORCENTAJE_ACUM'] = (campos_totales['ACUMULADO'] / produccion_total) * 100
    
    # Campos que representan el 70% de la producción
    campos_70_pct = campos_totales[campos_totales['PORCENTAJE_ACUM'] <= 70]['CAMPO_LIMPIO'].tolist()
    
    # Si no hay suficientes campos para llegar al 70%, tomar al menos los primeros 5
    if len(campos_70_pct) < 3:
        campos_70_pct = campos_totales.head(5)['CAMPO_LIMPIO'].tolist()
    
    # Serie de tiempo por campo (top 5)
    top_5_campos = top_campos.head(5)['CAMPO_LIMPIO'].tolist()
    df_top_campos = df_filtered[df_filtered['CAMPO_LIMPIO'].isin(top_5_campos)]
    
    fig_campos_tiempo = px.line(df_top_campos, x='AÑO', y='PRODUCCION FISCALIZADA', 
                               color='CAMPO_LIMPIO', markers=True,
                               title='Time Evolution - Top 5 Fields',
                               color_discrete_sequence=colores)
    fig_campos_tiempo.update_layout(
        plot_bgcolor='white', paper_bgcolor='white',
        font=dict(family='Segoe UI', size=14, color=color_texto),
        title_font=dict(size=20, color=color_texto, family='Segoe UI'),
        xaxis_title='Year', yaxis_title='Fiscalized Production',
        yaxis_tickformat=',.0f',
        xaxis=dict(dtick=1, tickmode='linear')
    )
    
    # Gráfica de barras top campos
    fig_top_campos = px.bar(top_campos, x='CAMPO_LIMPIO', y='PRODUCCION FISCALIZADA',
                           color='PRODUCCION FISCALIZADA', 
                           color_continuous_scale=[[0, '#e8f5f2'], [1, color_primario]],
                           title='Top 10 Fields by Total Production')
    fig_top_campos.update_layout(
        plot_bgcolor='white', paper_bgcolor='white',
        font=dict(family='Segoe UI', size=14, color=color_texto),
        title_font=dict(size=20, color=color_texto, family='Segoe UI'),
        xaxis_title='Field', yaxis_title='Total Production',
        yaxis_tickformat=',.0f',
        xaxis={'tickangle': 45}
    )
    
    # Crear gráficas individuales para campos que concentran el 70%
    campos_individuales = []
    
    for i, campo in enumerate(campos_70_pct):
        try:
            df_campo = df_filtered[df_filtered['CAMPO_LIMPIO'] == campo]
            
            if not df_campo.empty and len(df_campo) > 0:
                # Crear gráfica individual para el campo
                fig_individual = px.line(df_campo, x='AÑO', y='PRODUCCION FISCALIZADA',
                                       markers=True, title=f'Evolution of {campo}',
                                       line_shape='spline')
                
                # Usar un color específico del array de colores
                color_campo = colores[i % len(colores)]
                fig_individual.update_traces(line=dict(color=color_campo, width=3),
                                           marker=dict(size=8, color=color_campo))
                
                # Calcular el porcentaje de producción de este campo
                prod_campo = df_campo['PRODUCCION FISCALIZADA'].sum()
                if produccion_total > 0:
                    porcentaje_campo = (prod_campo / produccion_total) * 100
                    
                    fig_individual.update_layout(
                        plot_bgcolor='white', paper_bgcolor='white',
                        font=dict(family='Segoe UI', size=12, color=color_texto),
                        title_font=dict(size=16, color=color_texto, family='Segoe UI'),
                        xaxis_title='Year', yaxis_title='Fiscalized Production',
                        yaxis_tickformat=',.0f',
                        height=300,
                        xaxis=dict(dtick=1, tickmode='linear'),
                        annotations=[
                            dict(
                                text=f"Represents {porcentaje_campo:.1f}% of total",
                                x=0.5, y=1.05, xref="paper", yref="paper",
                                showarrow=False, font=dict(size=10, color=color_texto, family='Segoe UI'),
                                bgcolor="rgba(0, 166, 147, 0.15)", 
                                bordercolor=color_primario, 
                                borderwidth=1,
                                borderpad=4,
                                xanchor='center',
                                yanchor='bottom'
                            )
                        ]
                    )
                else:
                    fig_individual.update_layout(
                        plot_bgcolor='white', paper_bgcolor='white',
                        font=dict(family='Segoe UI', size=12, color=color_texto),
                        title_font=dict(size=16, color=color_texto, family='Segoe UI'),
                        xaxis_title='Year', yaxis_title='Fiscalized Production',
                        yaxis_tickformat=',.0f',
                        height=300,
                        xaxis=dict(dtick=1, tickmode='linear')
                    )
                
                campos_individuales.append(
                    dbc.Col([
                        dcc.Graph(figure=fig_individual, style={'height': '320px'})
                    ], width=6, className="mb-3")
                )
        except Exception as e:
            # Si hay error con un campo específico, continúa con el siguiente
            print(f"Error with field {campo}: {str(e)}")
            continue
    
    # Organizar las gráficas individuales en filas de 2 columnas
    filas_individuales = []
    for i in range(0, len(campos_individuales), 2):
        fila = campos_individuales[i:i+2]
        # Si solo hay una gráfica en la última fila, completar con columna vacía
        if len(fila) == 1:
            fila.append(dbc.Col(width=6))
        filas_individuales.append(dbc.Row(fila))
    
    return [
        dbc.Row([
            dbc.Col([
                dcc.Graph(figure=fig_campos_tiempo, style={'height': '500px'})
            ], width=12)
        ], className="mb-3"),
        
        dbc.Row([
            dbc.Col([
                dcc.Graph(figure=fig_top_campos, style={'height': '500px'})
            ], width=12)
        ], className="mb-4"),
        
        # Información sobre los campos principales
        dbc.Row([
            dbc.Col([
                html.H3(f"Main Fields - Concentrate 70% of Production ({len(campos_70_pct)} fields)", 
                       className="text-center mb-4",
                       style={'color': color_texto, 'fontWeight': '600', 'fontFamily': 'Segoe UI'})
            ], width=12)
        ]),
        
        # Gráficas individuales de campos principales
        *filas_individuales
    ]

def crear_tab_cuenca(df_filtered):
    """Create basin tab content"""
    
    if df_filtered.empty:
        return [html.P("No data available for the selected range", style={'color': color_texto, 'fontSize': '16px', 'textAlign': 'center'})]
    
    # Serie de tiempo por cuenca
    fig_cuencas_tiempo = px.line(df_filtered, x='AÑO', y='PRODUCCION FISCALIZADA', 
                                color='CUENCA', markers=True,
                                title='Time Evolution by Basin',
                                color_discrete_sequence=colores)
    fig_cuencas_tiempo.update_layout(
        plot_bgcolor='white', paper_bgcolor='white',
        font=dict(family='Segoe UI', size=14, color=color_texto),
        title_font=dict(size=20, color=color_texto, family='Segoe UI'),
        xaxis_title='Year', yaxis_title='Fiscalized Production',
        yaxis_tickformat=',.0f',
        xaxis=dict(dtick=1, tickmode='linear')
    )
    
    # Producción total por cuenca
    cuencas_total = df_filtered.groupby('CUENCA')['PRODUCCION FISCALIZADA'].sum().reset_index()
    cuencas_total = cuencas_total.sort_values('PRODUCCION FISCALIZADA', ascending=False)
    
    fig_cuencas_total = px.bar(cuencas_total, x='CUENCA', y='PRODUCCION FISCALIZADA',
                              color='PRODUCCION FISCALIZADA', 
                              color_continuous_scale=[[0, '#e8f5f2'], [1, color_primario]],
                              title='Total Production by Basin')
    fig_cuencas_total.update_layout(
        plot_bgcolor='white', paper_bgcolor='white',
        font=dict(family='Segoe UI', size=14, color=color_texto),
        title_font=dict(size=20, color=color_texto, family='Segoe UI'),
        xaxis_title='Basin', yaxis_title='Total Production',
        yaxis_tickformat=',.0f'
    )
    
    # Gráfica de área apilada
    fig_area = px.area(df_filtered, x='AÑO', y='PRODUCCION FISCALIZADA', 
                      color='CUENCA', title='Production Composition by Basin',
                      color_discrete_sequence=colores)
    fig_area.update_layout(
        plot_bgcolor='white', paper_bgcolor='white',
        font=dict(family='Segoe UI', size=14, color=color_texto),
        title_font=dict(size=20, color=color_texto, family='Segoe UI'),
        xaxis_title='Year', yaxis_title='Fiscalized Production',
        yaxis_tickformat=',.0f',
        xaxis=dict(dtick=1, tickmode='linear')
    )
    
    # Crear gráficas individuales por cuenca
    cuencas_individuales = []
    cuencas_unicas = df_filtered['CUENCA'].unique()
    
    for i, cuenca in enumerate(cuencas_unicas):
        df_cuenca = df_filtered[df_filtered['CUENCA'] == cuenca]
        
        # Crear gráfica individual para la cuenca
        fig_individual = px.line(df_cuenca, x='AÑO', y='PRODUCCION FISCALIZADA',
                               markers=True, title=f'Evolution of {cuenca}',
                               line_shape='spline')
        
        # Usar un color específico del array de colores
        color_cuenca = colores[i % len(colores)]
        fig_individual.update_traces(line=dict(color=color_cuenca, width=3),
                                   marker=dict(size=8, color=color_cuenca))
        
        # Calcular el total de producción de esta cuenca
        total_cuenca = df_cuenca['PRODUCCION FISCALIZADA'].sum()
        
        fig_individual.update_layout(
            plot_bgcolor='white', paper_bgcolor='white',
            font=dict(family='Segoe UI', size=12, color=color_texto),
            title_font=dict(size=16, color=color_texto, family='Segoe UI'),
            xaxis_title='Year', yaxis_title='Fiscalized Production',
            yaxis_tickformat=',.0f',
            height=300,
            xaxis=dict(dtick=1, tickmode='linear'),
            annotations=[
                dict(
                    text=f"Total Production: {total_cuenca:,.0f}",
                    x=0.5, y=1.05, xref="paper", yref="paper",
                    showarrow=False, font=dict(size=10, color=color_texto, family='Segoe UI'),
                    bgcolor="rgba(0, 166, 147, 0.15)", 
                    bordercolor=color_primario, 
                    borderwidth=1,
                    borderpad=4,
                    xanchor='center',
                    yanchor='bottom'
                )
            ]
        )
        
        cuencas_individuales.append(
            dbc.Col([
                dcc.Graph(figure=fig_individual, style={'height': '320px'})
            ], width=6, className="mb-3")
        )
    
    # Organizar las gráficas individuales en filas de 2 columnas
    filas_individuales = []
    for i in range(0, len(cuencas_individuales), 2):
        fila = cuencas_individuales[i:i+2]
        # Si solo hay una gráfica en la última fila, completar con columna vacía
        if len(fila) == 1:
            fila.append(dbc.Col(width=6))
        filas_individuales.append(dbc.Row(fila))
    
    return [
        dbc.Row([
            dbc.Col([
                dcc.Graph(figure=fig_cuencas_tiempo, style={'height': '450px'})
            ], width=12)
        ], className="mb-3"),
        
        dbc.Row([
            dbc.Col([
                dcc.Graph(figure=fig_cuencas_total, style={'height': '400px'})
            ], width=6),
            dbc.Col([
                dcc.Graph(figure=fig_area, style={'height': '400px'})
            ], width=6)
        ], className="mb-4"),
        
        # Título para las gráficas individuales
        dbc.Row([
            dbc.Col([
                html.H3("Individual Analysis by Basin", 
                       className="text-center mb-4",
                       style={'color': color_texto, 'fontWeight': '600', 'fontFamily': 'Segoe UI'})
            ], width=12)
        ]),
        
        # Gráficas individuales por cuenca
        *filas_individuales
    ]

def crear_tab_departamento(df_filtered):
    """Create department tab content with interactive maps and analysis"""
    
    if df_filtered.empty:
        return [html.P("No data available for the selected range", style={'color': color_texto, 'fontSize': '16px', 'textAlign': 'center'})]
    
    # Agrupar datos por departamento
    df_dept_grouped = df_filtered.groupby(['AÑO', 'DEPARTAMENTO'])['PRODUCCION FISCALIZADA'].sum().reset_index()
    
    # Producción total por departamento
    dept_totales = df_filtered.groupby('DEPARTAMENTO')['PRODUCCION FISCALIZADA'].sum().sort_values(ascending=False).reset_index()
    
    # KPIs específicos de departamentos
    total_departamentos = len(dept_totales)
    dept_principal = dept_totales.iloc[0] if not dept_totales.empty else {'DEPARTAMENTO': 'N/A', 'PRODUCCION FISCALIZADA': 0}
    produccion_total = dept_totales['PRODUCCION FISCALIZADA'].sum()
    
    # Top 3 departamentos representan qué % del total
    top_3_produccion = dept_totales.head(3)['PRODUCCION FISCALIZADA'].sum()
    pct_top_3 = (top_3_produccion / produccion_total * 100) if produccion_total > 0 else 0
    
    # Crear mapa de Colombia (choropleth)
    # Para esto necesitamos crear un mapeo de nombres de departamentos
    dept_mapping = {
        'ARAUCA': 'Arauca',
        'BOYACA': 'Boyacá',
        'CASANARE': 'Casanare',
        'CESAR': 'Cesar',
        'CUNDINAMARCA': 'Cundinamarca',
        'HUILA': 'Huila',
        'LA GUAJIRA': 'La Guajira',
        'META': 'Meta',
        'PUTUMAYO': 'Putumayo',
        'SANTANDER': 'Santander',
        'TOLIMA': 'Tolima',
        'NORTE DE SANTANDER': 'Norte de Santander',
        'ANTIOQUIA': 'Antioquia',
        'CORDOBA': 'Córdoba',
        'MAGDALENA': 'Magdalena',
        'BOLIVAR': 'Bolívar',
        'VALLE DEL CAUCA': 'Valle del Cauca',
        'CAUCA': 'Cauca',
        'NARIÑO': 'Nariño',
        'CHOCO': 'Chocó'
    }
    
    # Preparar datos para el mapa
    dept_totales_mapa = dept_totales.copy()
    dept_totales_mapa['DEPARTAMENTO_MAPA'] = dept_totales_mapa['DEPARTAMENTO'].map(dept_mapping).fillna(dept_totales_mapa['DEPARTAMENTO'])
    
    # Mapa de burbujas por departamento (más simple y efectivo)
    # Coordenadas aproximadas de las capitales de departamentos de Colombia
    coordenadas_dept = {
        'ARAUCA': {'lat': 7.0889, 'lon': -70.7591},
        'BOYACA': {'lat': 5.4544, 'lon': -73.3624},
        'CASANARE': {'lat': 5.3356, 'lon': -72.4056},
        'CESAR': {'lat': 10.4636, 'lon': -73.2532},
        'CUNDINAMARCA': {'lat': 4.7110, 'lon': -74.0721},
        'HUILA': {'lat': 2.9273, 'lon': -75.2819},
        'LA GUAJIRA': {'lat': 11.5444, 'lon': -72.9072},
        'META': {'lat': 4.1420, 'lon': -73.6266},
        'PUTUMAYO': {'lat': 0.5136, 'lon': -76.3567},
        'SANTANDER': {'lat': 7.1193, 'lon': -73.1227},
        'TOLIMA': {'lat': 4.4389, 'lon': -75.2322},
        'NORTE DE SANTANDER': {'lat': 7.8939, 'lon': -72.5078},
        'ANTIOQUIA': {'lat': 6.2442, 'lon': -75.5812},
        'CORDOBA': {'lat': 8.7479, 'lon': -75.8814},
        'MAGDALENA': {'lat': 11.2408, 'lon': -74.1990},
        'BOLIVAR': {'lat': 10.3910, 'lon': -75.4794},
        'VALLE DEL CAUCA': {'lat': 3.4516, 'lon': -76.5320},
        'CAUCA': {'lat': 2.4418, 'lon': -76.6063},
        'NARIÑO': {'lat': 1.2136, 'lon': -77.2811},
        'CHOCO': {'lat': 5.6837, 'lon': -76.6581},
        'SUCRE': {'lat': 9.3017, 'lon': -75.3975},
        'ATLANTICO': {'lat': 10.9685, 'lon': -74.7813},
        'CALDAS': {'lat': 5.0689, 'lon': -75.5174},
        'QUINDIO': {'lat': 4.5389, 'lon': -75.6661},
        'RISARALDA': {'lat': 4.8133, 'lon': -75.6961},
        'CAQUETA': {'lat': 1.6145, 'lon': -75.6062},
        'VICHADA': {'lat': 6.1167, 'lon': -67.4167},
        'GUAVIARE': {'lat': 2.5649, 'lon': -72.6409},
        'VAUPES': {'lat': 1.2500, 'lon': -70.2333},
        'GUAINIA': {'lat': 2.5833, 'lon': -67.9167},
        'AMAZONAS': {'lat': -4.2158, 'lon': -69.9406},
        'SAN ANDRES Y PROVIDENCIA': {'lat': 12.5847, 'lon': -81.7006}
    }
    
    # Preparar datos para el mapa con TODOS los departamentos
    dept_mapa_data = []
    total_nacional = dept_totales_mapa['PRODUCCION FISCALIZADA'].sum()
    max_produccion = dept_totales_mapa['PRODUCCION FISCALIZADA'].max()
    min_produccion = dept_totales_mapa['PRODUCCION FISCALIZADA'].min()
    
    for _, row in dept_totales_mapa.iterrows():
        dept = row['DEPARTAMENTO']
        produccion = row['PRODUCCION FISCALIZADA']
        participacion = (produccion / total_nacional * 100) if total_nacional > 0 else 0
        
        # Buscar coordenadas o asignar coordenadas por defecto si no existe
        if dept in coordenadas_dept:
            lat = coordenadas_dept[dept]['lat']
            lon = coordenadas_dept[dept]['lon']
        else:
            # Coordenadas por defecto para departamentos no encontrados (centro de Colombia)
            lat = 4.5 + (len(dept_mapa_data) * 0.1)  # Distribución vertical para evitar superposición
            lon = -74.0 + (len(dept_mapa_data) * 0.1)  # Distribución horizontal
        
        # Calcular tamaño de burbuja proporcional a la producción
        if max_produccion > min_produccion:
            # Escala logarítmica para mejor visualización de rangos amplios
            import math
            if produccion > 0:
                log_ratio = math.log(produccion / min_produccion) / math.log(max_produccion / min_produccion)
                size = 8 + (log_ratio * 45)  # Tamaños entre 8 y 53
            else:
                size = 8
        else:
            size = 25  # Tamaño uniforme si todos tienen la misma producción
        
        dept_mapa_data.append({
            'DEPARTAMENTO': dept,
            'PRODUCCION': produccion,
            'PARTICIPACION': participacion,
            'PRODUCCION_FORMATTED': f"{produccion:,.0f}",
            'PARTICIPACION_FORMATTED': f"{participacion:.1f}%",
            'lat': lat,
            'lon': lon,
            'size': size
        })
    
    df_mapa = pd.DataFrame(dept_mapa_data)
    
    # Crear mapa con fondo geográfico real usando scatter_mapbox
    fig_mapa = px.scatter_mapbox(
        df_mapa,
        lat='lat',
        lon='lon',
        size='size',
        color='PRODUCCION',
        hover_name='DEPARTAMENTO',
        hover_data=['PRODUCCION_FORMATTED', 'PARTICIPACION_FORMATTED'],
        color_continuous_scale=[
            [0, '#10b981'],     # Verde medio
            [0.3, '#059669'],   # Verde medio oscuro
            [0.5, color_primario],  # Verde KuenKa (#00a693)
            [0.7, '#047857'],   # Verde oscuro
            [0.9, '#065f46'],   # Verde muy oscuro
            [1, '#064e3b']      # Verde más oscuro
        ],
        size_max=60,
        title='Geographic Distribution - Gas Production by Department',
        mapbox_style="open-street-map",  # Mapa de fondo real
        zoom=5,
        center={"lat": 4.5, "lon": -74.0}  # Centrado en Colombia
    )
    
    # Actualizar el hover template para mostrar la información correctamente
    fig_mapa.update_traces(
        hovertemplate='<b>%{hovertext}</b><br>' +
                     'Total Production: %{customdata[0]}<br>' +
                     'National Share: %{customdata[1]}<br>' +
                     '<extra></extra>',
        customdata=df_mapa[['PRODUCCION_FORMATTED', 'PARTICIPACION_FORMATTED']].values
    )
    
    fig_mapa.update_layout(
        font=dict(family='Segoe UI', size=14, color=color_texto),
        title_font=dict(size=20, color=color_texto, family='Segoe UI'),
        height=500,
        showlegend=False,
        margin=dict(t=60, b=40, l=40, r=40),
        paper_bgcolor='white',
        coloraxis_colorbar=dict(
            title="Production Volume",
            tickformat=",.0f"
        )
    )
    
    # Gráfica de ranking departamental mejorada
    top_10_depts = dept_totales.head(10).copy()
    top_10_depts['RANK'] = range(1, len(top_10_depts) + 1)
    top_10_depts['PARTICIPACION'] = (top_10_depts['PRODUCCION FISCALIZADA'] / total_nacional * 100)
    top_10_depts['DEPT_LABEL'] = top_10_depts['DEPARTAMENTO'] + ' (' + top_10_depts['PARTICIPACION'].round(1).astype(str) + '%)'
    
    # Crear colores graduales personalizados
    colors = []
    for i, val in enumerate(top_10_depts['PRODUCCION FISCALIZADA']):
        if i == 0:  # Primer lugar
            colors.append('#004d40')  # Verde oscuro
        elif i == 1:  # Segundo lugar
            colors.append(color_primario)  # Verde KuenKa
        elif i == 2:  # Tercer lugar
            colors.append('#26a69a')  # Verde medio
        else:
            # Gradiente para el resto
            intensity = 0.8 - (i-3) * 0.1
            colors.append(f'rgba(0, 166, 147, {max(intensity, 0.3)})')
    
    fig_ranking = go.Figure(go.Bar(
        y=top_10_depts['DEPT_LABEL'],
        x=top_10_depts['PRODUCCION FISCALIZADA'],
        orientation='h',
        marker=dict(
            color=colors,
            line=dict(color='white', width=1)
        ),
        text=[f"{val:,.0f}" for val in top_10_depts['PRODUCCION FISCALIZADA']],
        textposition='outside',
        textfont=dict(size=12, color=color_texto, family='Segoe UI'),
        hovertemplate='<b>%{customdata[0]}</b><br>' +
                      'Production: %{x:,.0f}<br>' +
                      'National Share: %{customdata[1]:.1f}%<br>' +
                      'Ranking: #%{customdata[2]}' +
                      '<extra></extra>',
        customdata=list(zip(top_10_depts['DEPARTAMENTO'], 
                           top_10_depts['PARTICIPACION'],
                           top_10_depts['RANK']))
    ))
    
    fig_ranking.update_layout(
        title='Top 10 Departments by Total Production<br><span style="font-size:14px; color:#666">Percentage shows national market share</span>',
        plot_bgcolor='white', 
        paper_bgcolor='white',
        font=dict(family='Segoe UI', size=12, color=color_texto),
        title_font=dict(size=20, color=color_texto, family='Segoe UI'),
        title_x=0.5,
        xaxis_title='Total Production (Million Cubic Feet)', 
        yaxis_title='Department',
        xaxis=dict(
            tickformat=',.0f',
            showgrid=True,
            gridcolor='rgba(0,0,0,0.1)',
            gridwidth=1
        ),
        yaxis=dict(
            categoryorder='total ascending',
            showgrid=False
        ),
        height=520,
        margin=dict(l=200, r=80, t=100, b=60)
    )
    
    # Serie de tiempo por departamentos principales (Top 5) mejorada
    top_5_dept = dept_totales.head(5)['DEPARTAMENTO'].tolist()
    df_top_dept = df_dept_grouped[df_dept_grouped['DEPARTAMENTO'].isin(top_5_dept)]
    
    # Colores específicos para cada departamento
    color_mapping = {
        top_5_dept[0]: '#004d40',     # Verde oscuro para #1
        top_5_dept[1]: color_primario, # Verde KuenKa para #2
        top_5_dept[2]: '#26a69a',     # Verde medio para #3
        top_5_dept[3]: '#4db6ac',     # Verde claro para #4
        top_5_dept[4]: '#80cbc4'      # Verde muy claro para #5
    }
    
    fig_dept_tiempo = go.Figure()
    
    # Agregar línea para cada departamento
    for i, dept in enumerate(top_5_dept):
        dept_data = df_top_dept[df_top_dept['DEPARTAMENTO'] == dept].sort_values('AÑO')
        
        if not dept_data.empty:
            # Calcular tendencia
            first_val = dept_data.iloc[0]['PRODUCCION FISCALIZADA']
            last_val = dept_data.iloc[-1]['PRODUCCION FISCALIZADA']
            trend = "📈" if last_val > first_val else "📉" if last_val < first_val else "➖"
            
            fig_dept_tiempo.add_trace(go.Scatter(
                x=dept_data['AÑO'],
                y=dept_data['PRODUCCION FISCALIZADA'],
                mode='lines+markers',
                name=f'{trend} {dept}',
                line=dict(
                    color=color_mapping[dept], 
                    width=3,
                    shape='spline'
                ),
                marker=dict(
                    size=8, 
                    color=color_mapping[dept],
                    line=dict(color='white', width=2)
                ),
                hovertemplate='<b>%{fullData.name}</b><br>' +
                              'Year: %{x}<br>' +
                              'Production: %{y:,.0f}<br>' +
                              '<extra></extra>',
                connectgaps=True
            ))
    
    fig_dept_tiempo.update_layout(
        title='Time Evolution - Top 5 Departments<br><span style="font-size:14px; color:#666">Trend direction by department</span>',
        plot_bgcolor='white', 
        paper_bgcolor='white',
        font=dict(family='Segoe UI', size=12, color=color_texto),
        title_font=dict(size=18, color=color_texto, family='Segoe UI'),
        title_x=0.5,
        xaxis_title='Year', 
        yaxis_title='Fiscalized Production (Million Cubic Feet)',
        yaxis=dict(
            tickformat=',.0f',
            showgrid=True,
            gridcolor='rgba(0,0,0,0.1)',
            gridwidth=1
        ),
        xaxis=dict(
            dtick=1, 
            tickmode='linear',
            showgrid=True,
            gridcolor='rgba(0,0,0,0.1)',
            gridwidth=1
        ),
        height=420,
        margin=dict(t=80, b=60, l=80, r=20),
        legend=dict(
            orientation="v",
            yanchor="top",
            y=0.98,
            xanchor="left",
            x=1.02,
            bgcolor="rgba(255, 255, 255, 0.9)",
            bordercolor=color_primario,
            borderwidth=1
        ),
        hovermode='x unified'
    )
    

    

    
    return [
        # KPIs específicos de departamentos mejorados
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Active Departments", className="card-title text-center mb-3", 
                               style={'color': color_texto, 'fontSize': '16px', 'fontWeight': '600'}),
                        html.H2(f"{total_departamentos}", className="text-center", 
                               style={'fontSize': '36px', 'fontWeight': 'bold', 'color': color_primario}),
                        html.P("departments producing gas", className="text-center text-muted",
                              style={'fontSize': '12px', 'marginBottom': '0', 'fontStyle': 'italic'})
                    ], style={'padding': '25px'})
                ], style={
                    'boxShadow': '0 8px 32px rgba(0, 166, 147, 0.15)', 
                    'border': f'1px solid {color_primario}30', 
                    'borderRadius': '15px',
                    'background': 'linear-gradient(135deg, #ffffff 0%, #f8fffd 100%)',
                    'cursor': 'pointer',
                    'transition': 'all 0.3s ease'
                }, id="kpi-departments")
            ], width=3, className="mb-3"),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Leading Department", className="card-title text-center mb-3", 
                               style={'color': color_texto, 'fontSize': '16px', 'fontWeight': '600'}),
                        html.H2(f"{dept_principal['DEPARTAMENTO']}", className="text-center", 
                               style={'fontSize': '18px', 'fontWeight': 'bold', 'color': color_primario}),
                        html.P(f"{dept_principal['PRODUCCION FISCALIZADA']:,.0f}", className="text-center",
                              style={'fontSize': '14px', 'marginBottom': '5px', 'color': color_texto, 'fontWeight': '500'}),
                        html.P(f"{(dept_principal['PRODUCCION FISCALIZADA'] / total_nacional * 100):.1f}% of total", 
                              className="text-center text-muted",
                              style={'fontSize': '12px', 'marginBottom': '0', 'fontStyle': 'italic'})
                    ], style={'padding': '25px'})
                ], style={
                    'boxShadow': '0 8px 32px rgba(0, 166, 147, 0.15)', 
                    'border': f'1px solid {color_primario}30', 
                    'borderRadius': '15px',
                    'background': 'linear-gradient(135deg, #ffffff 0%, #f8fffd 100%)'
                })
            ], width=3, className="mb-3"),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Geographic Concentration", className="card-title text-center mb-3", 
                               style={'color': color_texto, 'fontSize': '16px', 'fontWeight': '600'}),
                        html.H2(f"{pct_top_3:.1f}%", className="text-center", 
                               style={'fontSize': '32px', 'fontWeight': 'bold', 'color': color_secundario}),
                        html.P(f"produced by top 3 departments", className="text-center text-muted",
                              style={'fontSize': '12px', 'marginBottom': '0', 'fontStyle': 'italic'})
                    ], style={'padding': '25px'})
                ], style={
                    'boxShadow': '0 8px 32px rgba(255, 193, 7, 0.15)', 
                    'border': f'1px solid {color_secundario}30', 
                    'borderRadius': '15px',
                    'background': 'linear-gradient(135deg, #ffffff 0%, #fffdf0 100%)'
                })
            ], width=3, className="mb-3"),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Total Production", className="card-title text-center mb-3", 
                               style={'color': color_texto, 'fontSize': '16px', 'fontWeight': '600'}),
                        html.H2(f"{produccion_total:,.0f}", className="text-center", 
                               style={'fontSize': '28px', 'fontWeight': 'bold', 'color': color_primario}),
                        html.P("million cubic feet", className="text-center text-muted",
                              style={'fontSize': '12px', 'marginBottom': '0', 'fontStyle': 'italic'})
                    ], style={'padding': '25px'})
                ], style={
                    'boxShadow': '0 8px 32px rgba(0, 166, 147, 0.15)', 
                    'border': f'1px solid {color_primario}30', 
                    'borderRadius': '15px',
                    'background': 'linear-gradient(135deg, #ffffff 0%, #f8fffd 100%)'
                })
            ], width=3, className="mb-3")
        ], className="mb-5", style={'marginLeft': '10px', 'marginRight': '10px'}),
        
        # Mapa principal de Colombia
        dbc.Row([
            dbc.Col([
                dcc.Graph(figure=fig_mapa, style={'height': '520px'})
            ], width=12)
        ], className="mb-4"),
        
        # Análisis de ranking y evolución temporal
        dbc.Row([
            dbc.Col([
                dcc.Graph(figure=fig_ranking, style={'height': '520px'})
            ], width=6),
            dbc.Col([
                dcc.Graph(figure=fig_dept_tiempo, style={'height': '520px'})
            ], width=6)
        ], className="mb-4"),
        

    ]

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8052))  # Cambio de puerto para evitar caché
    app.run(debug=False, host='0.0.0.0', port=port)