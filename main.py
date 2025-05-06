from astropy.io import fits
from analysis import analyze_headers_dict

# Lista de arquivos FITS
arquivos = ["espectro1.fits", "espectro2.fits"]

# Extrai os headers como dicionário
headers_dict = {
    nome: fits.getheader(nome)
    for nome in arquivos
}

# Analisa os headers e retorna um DataFrame
df = analyze_headers_dict(headers_dict)

# Exporta para CSV
df.to_csv("resumo_headers.csv", index=False)

print(df.head())