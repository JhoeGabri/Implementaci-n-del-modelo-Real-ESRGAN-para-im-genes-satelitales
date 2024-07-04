import pandas as pd

# Leer el archivo CSV
df = pd.read_csv('metrics_DIV2K_900K_Chainner_x2/DIV2K_900K_Chainner_x2_metrics_report.csv')

# Ordenar los datos
df_sorted = df.sort_values(by=['PSNR', 'SSIM', 'MSE'], ascending=[False, False, True])

# Guardar el archivo ordenado en un nuevo archivo CSV
df_sorted.to_csv('DIV2K_900K_sorted.csv', index=False)

print("Archivo ordenado y guardado como 'AID_900K_sorted.csv'.")
