import pandas as pd
pd.set_option('display.float_format', '{:,.0f}'.format)
import glob
import os
import re


# Ruta donde están los archivos
ruta_archivos = r"D:\Analisis producción de gas 2025\Bases_produccion_gas"

# Buscar todos los archivos Excel de gas
archivos = glob.glob(os.path.join(ruta_archivos, "Produccion_Fiscalizada_Gas_*.xlsx"))

print("Archivos encontrados:")
for archivo in archivos:
	print(archivo)

tablas_mensuales = []
resumen_anual = []
produccion_anual_por_campo = []


# Leer y acumular todos los datos originales en una lista de DataFrames
data_original = []

for archivo in archivos:
	nombre_archivo = os.path.basename(archivo)
	match = re.search(r'(20\d{2})', nombre_archivo)
	if match:
		anio = int(match.group(1))
	else:
		print(f"No se pudo extraer el año de: {nombre_archivo}")
		continue
	xls = pd.ExcelFile(archivo)
	for hoja in xls.sheet_names[1:]:  # Omitir la primera hoja (Campos Mpcpd)
		mes_match = re.match(r'([a-zA-Záéíóúñ]+)[- ]?\d{2}', hoja)
		if mes_match:
			mes = mes_match.group(1).lower()
		else:
			print(f"No se pudo extraer el mes de la hoja: {hoja}")
			continue
		df = pd.read_excel(xls, sheet_name=hoja)
		df.columns = df.columns.str.replace('\n', ' ', regex=True).str.replace('\r', ' ', regex=True)
		df.columns = df.columns.str.strip().str.upper()
		# Normalizar nombre de columna de producción fiscalizada
		prod_cols = [c for c in df.columns if 'PRODUCCION' in c and 'FISCALIZADA' in c]
		if prod_cols:
			prod_col = prod_cols[0]
			if prod_col != 'PRODUCCION FISCALIZADA':
				df['PRODUCCION FISCALIZADA'] = df[prod_col]
		# Agregar año y mes
		df['AÑO'] = anio
		df['MES'] = mes
		data_original.append(df)

# Concatenar todos los datos originales
df_all = pd.concat(data_original, ignore_index=True)

# Mostrar las columnas disponibles en los datos para diagnóstico
print("Columnas disponibles en los datos:")
print(sorted(df_all.columns.tolist()))

# Normalizar nombres de columnas y campos para consistencia
columnas_requeridas = [
	'AÑO', 'MES', 'CAMPO', 'CONTRATO', 'EMPRESA', 'DEPARTAMENTO', 'MUNICIPIO',
	'PRODUCCION FISCALIZADA', 'GAS LIFT', 'GAS REINYECTADO', 'GAS QUEMADO',
	'CONSUMO EN CAMPO', 'ENVIADO A PLANTA', 'GAS TRANSFORMADO', 'ENTREGADO A GASEODUCTOS'
]
for col in columnas_requeridas:
	if col not in df_all.columns:
		df_all[col] = 0

# Mapeo para corregir nombres problemáticos de campos
MAPEO_CAMPOS = {
	'Alligator': 'ALLIGATOR',
	'CARAMELO UNIFICADO': 'CARAMELO',
	'CHÁCHARO': 'CHACHARO',
	'Canaguay': 'CANAGUAY',
	'Coralillo': 'CORALILLO',
	'LA LOMA': 'LA LOMA ynf',
	'Lorito': 'LORITO',
	'MAGICO EXPLORATORIO': 'CAMPO EXPLORATORIO MAGICO',
	'MANA': 'MANÁ',
	'Pandereta': 'PANDERETA',
	'RECETPR WEST': 'RECETOR WEST',
	'UNIFICADO PALOGRANDE': 'PALOGRANDE UNIFICADO',
	'Unificado Río Ceibas': 'RIO CEIBAS',
	'TIGANA ': 'TIGANA',
	'TECA-COCORNA': 'AREA TECA-COCORNA',
	'SANTO DOMINGO UNIFICADO': 'SANTO DOMINGO',
}
df_all['CAMPO_LIMPIO'] = df_all['CAMPO'].replace(MAPEO_CAMPOS)
df_all['CAMPO_LIMPIO'] = df_all['CAMPO_LIMPIO'].fillna(df_all['CAMPO'])
for col in ['PRODUCCION FISCALIZADA', 'GAS LIFT', 'GAS REINYECTADO', 'GAS QUEMADO',
			'CONSUMO EN CAMPO', 'ENVIADO A PLANTA', 'GAS TRANSFORMADO', 'ENTREGADO A GASEODUCTOS']:
	if col not in df_all.columns:
		df_all[col] = 0
df_anual = df_all.groupby(['AÑO', 'CAMPO_LIMPIO', 'CONTRATO', 'EMPRESA', 'DEPARTAMENTO', 'MUNICIPIO'], as_index=False)[
	[
		'PRODUCCION FISCALIZADA', 'GAS LIFT', 'GAS REINYECTADO', 'GAS QUEMADO',
		'CONSUMO EN CAMPO', 'ENVIADO A PLANTA', 'GAS TRANSFORMADO', 'ENTREGADO A GASEODUCTOS'
	]
].sum(numeric_only=True)

# TOTALES MENSUALES (todas las variables)
df_mensual = df_all.groupby(['AÑO', 'MES'], as_index=False)[
	[
		'PRODUCCION FISCALIZADA', 'GAS LIFT', 'GAS REINYECTADO', 'GAS QUEMADO',
		'CONSUMO EN CAMPO', 'ENVIADO A PLANTA', 'GAS TRANSFORMADO', 'ENTREGADO A GASEODUCTOS'
	]
].sum(numeric_only=True)

# TOTALES ANUALES (todas las variables)
df_totales_anuales = df_all.groupby(['AÑO'], as_index=False)[
	[
		'PRODUCCION FISCALIZADA', 'GAS LIFT', 'GAS REINYECTADO', 'GAS QUEMADO',
		'CONSUMO EN CAMPO', 'ENVIADO A PLANTA', 'GAS TRANSFORMADO', 'ENTREGADO A GASEODUCTOS'
	]
].sum(numeric_only=True)

# ANUAL POR CAMPO
df_anual_campo = df_all.groupby(['AÑO', 'CAMPO_LIMPIO'], as_index=False)[
	[
		'PRODUCCION FISCALIZADA', 'GAS LIFT', 'GAS REINYECTADO', 'GAS QUEMADO',
		'CONSUMO EN CAMPO', 'ENVIADO A PLANTA', 'GAS TRANSFORMADO', 'ENTREGADO A GASEODUCTOS'
	]
].sum(numeric_only=True)


# ANUAL POR CUENCA Y ASIGNACIÓN MANUAL DE CUENCA
archivo_cuencas = r"D:\Analisis producción de gas 2025\cuencas_campos_gas.xlsx"
df_cuencas = pd.read_excel(archivo_cuencas)
df_cuencas.columns = df_cuencas.columns.str.strip().str.upper()

df_merge = pd.merge(df_all, df_cuencas, how='left', left_on='CAMPO_LIMPIO', right_on='CAMPO')
df_merge['CUENCA'] = df_merge['CUENCA'].fillna('SIN CUENCA')

# Asignación manual de cuenca para campos faltantes
import unicodedata
MAPEO_CUENCAS_EXTRA = {
	'CORAZON WEST 4': 'VMM',
	'DIVIDIVI': 'VIM',
	'GIGANTE CABALLOS': 'VSM',
	'LOS ANGELES 12': 'VMM',
	'PALERMO - SANTA CLARA UNIFICADO': 'VSM',
	'TENAX': 'VSM',
}
def normalizar_campo(nombre):
	if pd.isnull(nombre):
		return ''
	nombre = str(nombre).strip().upper()
	nombre = unicodedata.normalize('NFKD', nombre).encode('ASCII', 'ignore').decode('utf-8')
	nombre = nombre.replace('  ', ' ')
	return nombre
mapeo_cuencas_extra_norm = {normalizar_campo(k): v for k, v in MAPEO_CUENCAS_EXTRA.items()}
df_merge['CUENCA'] = df_merge.apply(
	lambda row: mapeo_cuencas_extra_norm.get(normalizar_campo(row['CAMPO_LIMPIO']), row['CUENCA'])
	if row['CUENCA'] == 'SIN CUENCA' else row['CUENCA'], axis=1)


# Mostrar solo los nombres de los campos que no coinciden exactamente con los del Excel de cuencas
campos_cuencas = set(df_cuencas['CAMPO'].astype(str).str.strip().str.upper())
campos_limpios = set(df_all['CAMPO_LIMPIO'].astype(str).str.strip().str.upper())
no_coinciden = sorted(list(campos_limpios - campos_cuencas))
if no_coinciden:
	print("Campos en datos que no coinciden con el Excel de cuencas:")
	for campo in no_coinciden:
		print(campo)

df_anual_cuenca = df_merge.groupby(['AÑO', 'CUENCA'], as_index=False)[
	[
		'PRODUCCION FISCALIZADA', 'GAS LIFT', 'GAS REINYECTADO', 'GAS QUEMADO',
		'CONSUMO EN CAMPO', 'ENVIADO A PLANTA', 'GAS TRANSFORMADO', 'ENTREGADO A GASEODUCTOS'
	]
].sum(numeric_only=True)

# Mostrar en consola los nombres de los campos que no tienen cuenca asignada
campos_sin_cuenca = df_merge[df_merge['CUENCA'] == 'SIN CUENCA']['CAMPO_LIMPIO'].drop_duplicates().tolist()
if campos_sin_cuenca:
	print("\nCampos sin cuenca asignada (no aparecen en el Excel de cuencas ni en el mapeo extra):")
	for campo in campos_sin_cuenca:
		print(campo)


# EXPORTAR TODO EN UN SOLO EXCEL
output_excel = os.path.join(ruta_archivos, "produccion_gas_resumenes.xlsx")
# Agrupar solo por AÑO y CAMPO_LIMPIO para la hoja Sumatoria_Anual
df_sum_anual = df_all.groupby(['AÑO', 'CAMPO_LIMPIO'], as_index=False)[
	[
		'PRODUCCION FISCALIZADA', 'GAS LIFT', 'GAS REINYECTADO', 'GAS QUEMADO',
		'CONSUMO EN CAMPO', 'ENVIADO A PLANTA', 'GAS TRANSFORMADO', 'ENTREGADO A GASEODUCTOS'
	]
].sum(numeric_only=True)
# Agregar departamento, municipio y cuenca
campos_info = df_merge.drop_duplicates(subset=['CAMPO_LIMPIO'])[['CAMPO_LIMPIO', 'DEPARTAMENTO', 'MUNICIPIO', 'CUENCA']]
df_sum_anual = pd.merge(df_sum_anual, campos_info, how='left', left_on='CAMPO_LIMPIO', right_on='CAMPO_LIMPIO')
cols = [c for c in ['AÑO', 'CAMPO_LIMPIO', 'DEPARTAMENTO', 'MUNICIPIO', 'CUENCA', 'PRODUCCION FISCALIZADA', 'GAS LIFT', 'GAS REINYECTADO', 'GAS QUEMADO',
	'CONSUMO EN CAMPO', 'ENVIADO A PLANTA', 'GAS TRANSFORMADO', 'ENTREGADO A GASEODUCTOS'] if c in df_sum_anual.columns]
with pd.ExcelWriter(output_excel) as writer:
	df_sum_anual[cols].to_excel(writer, sheet_name="Sumatoria_Anual", index=False)
	df_anual_campo.to_excel(writer, sheet_name="Anual_Por_Campo", index=False)
	df_anual_cuenca.to_excel(writer, sheet_name="Anual_Por_Cuenca", index=False)
	df_mensual.to_excel(writer, sheet_name="Totales_Mensuales", index=False)
	df_totales_anuales.to_excel(writer, sheet_name="Totales_Anuales", index=False)
print(f"\nArchivo Excel generado con todas las hojas: {output_excel}")

# Exportar segundo Excel tipo serie de tiempo anual solo fiscalizada

# Pivot: años como columnas, campos/cuencas como filas
serie_campo_pivot = df_anual_campo.pivot(index='CAMPO_LIMPIO', columns='AÑO', values='PRODUCCION FISCALIZADA').sort_index()
serie_campo_pivot = serie_campo_pivot.reset_index()
serie_cuenca_pivot = df_anual_cuenca.pivot(index='CUENCA', columns='AÑO', values='PRODUCCION FISCALIZADA').sort_index()
serie_cuenca_pivot = serie_cuenca_pivot.reset_index()
output_excel_serie = os.path.join(ruta_archivos, "serie_tiempo_gas.xlsx")
with pd.ExcelWriter(output_excel_serie) as writer:
	serie_campo_pivot.to_excel(writer, sheet_name="Serie_Campo", index=False)
	serie_cuenca_pivot.to_excel(writer, sheet_name="Serie_Cuenca", index=False)
	# Nueva hoja: CAMPO, CUENCA y serie de tiempo anual
	# Unir df_anual_campo con cuenca
	campos_cuenca = df_merge.drop_duplicates(subset=['CAMPO_LIMPIO', 'CUENCA'])[['CAMPO_LIMPIO', 'CUENCA']]
	serie_campo = df_anual_campo.pivot(index='CAMPO_LIMPIO', columns='AÑO', values='PRODUCCION FISCALIZADA').reset_index()
	serie_campo = pd.merge(serie_campo, campos_cuenca, how='left', left_on='CAMPO_LIMPIO', right_on='CAMPO_LIMPIO')
	# Reordenar columnas: CAMPO, CUENCA, años...
	cols = ['CAMPO_LIMPIO', 'CUENCA'] + [c for c in serie_campo.columns if c not in ['CAMPO_LIMPIO', 'CUENCA']]
	serie_campo = serie_campo[cols]
	serie_campo = serie_campo.rename(columns={'CAMPO_LIMPIO': 'CAMPO'})
	serie_campo.to_excel(writer, sheet_name="Serie_Campo_Cuenca", index=False)
print(f"\nArchivo de serie de tiempo generado: {output_excel_serie}")

# Mostrar sumatoria mensual y anual de gas fiscalizada
print("SUMATORIA MENSUAL DE GAS FISCALIZADA: ")

if 'PRODUCCION FISCALIZADA' in df_mensual.columns:
	print(df_mensual[['AÑO', 'MES', 'PRODUCCION FISCALIZADA']].to_string(index=False))

	# Mostrar tabla pivote: años como filas, meses como columnas
	meses_orden = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
	df_pivot = df_mensual.pivot(index='AÑO', columns='MES', values='PRODUCCION FISCALIZADA')
	# Reordenar columnas de meses si existen
	df_pivot = df_pivot.reindex(columns=meses_orden, fill_value=0)
	print("\nTOTAL MENSUAL DE CADA AÑO (PRODUCCION FISCALIZADA):")
	print(df_pivot.to_string())
else:
	print("No hay datos de PRODUCCION FISCALIZADA en los totales mensuales.")


print("SUMATORIA ANUAL DE GAS FISCALIZADA:")

if 'PRODUCCION FISCALIZADA' in df_totales_anuales.columns:
	print(df_totales_anuales[['AÑO', 'PRODUCCION FISCALIZADA']].to_string(index=False))
else:
	print("No hay datos de PRODUCCION FISCALIZADA en los totales anuales.")


