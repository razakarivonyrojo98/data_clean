import pandas as pd

file_path = "./fichier/benchmark_data_2019 with yield.xlsx"
df = pd.read_excel(file_path, header=None)

# nettoyer colonnes vides
df = df.dropna(axis=1, how='all')

# 🔥 trouver les débuts de blocs
block_starts = []

for col in range(df.shape[1]):
    val = str(df.iloc[0, col]).strip()

    if val == "Date" or val == "Security":
        block_starts.append(col)

# ajouter fin du fichier
block_starts.append(df.shape[1])

all_blocks = []

date_series = None

for i in range(len(block_starts) - 1):
    start = block_starts[i]
    end = block_starts[i + 1]

    block = df.iloc[:, start:end].copy()

    header = block.iloc[0].tolist()
    block = block[1:].reset_index(drop=True)

    # 🔥 Bloc 1 (avec Date)
    if "Date" in header:
        block.columns = header

        # garder Date
        date_series = block["Date"].reset_index(drop=True)

        all_blocks.append(block)

    else:
        block.columns = header

        # 🔥 injecter Date par ALIGNEMENT LIGNE
        block["Date"] = date_series[:len(block)]

        all_blocks.append(block)

# 🔥 fusion finale
final_df = pd.concat(all_blocks, ignore_index=True)

# remettre Date en première colonne
cols = ["Date"] + [c for c in final_df.columns if c != "Date"]
final_df = final_df[cols]

# 🔥 supprimer lignes sans données (hors Date)
cols_to_check = [col for col in final_df.columns if col != "Date"]
final_df = final_df.dropna(subset=cols_to_check, how='all')

final_df.to_excel("fusion_resultat_total_final.xlsx", index=False)

print("✔ Fusion parfaite avec alignement réel des blocs")