import numpy as np
import pandas as pd

def add_column(df, new_col, conditions, choices):
    df[new_col] = np.select(conditions, choices)
    return df

def main():
    df = pd.read_csv("futplayers.csv", index_col=False)
    df_gk = pd.read_csv("futgk.csv", index_col=False)

    pos_condlist = [df['Pos'].isin(["ST", "LW", "RW", "CF"]), 
            df['Pos'].isin(["CAM", "CDM", "CM", "LM", "RM"]), 
            df['Pos'].isin(["CB", "LB", "LWB", "RB", "RWB"])]
    pos_choicelist = ["Attacker", "Midfielder", "Defender"]
    
    df = add_column(df, 'Position', pos_condlist, pos_choicelist)
    df_gk = add_column(df_gk, 'Position', [True], ["Goalkeeper"])

    headers = ['PAC', 'SHO', 'PAS', 'DRI', 'DEF', 'PHY', 'DIV', 'HAN', 'KIC', 'REF', 'SPE', 'POS', 'WF', 'Skill', 'Position', 'Rtg']
    df = df.reindex(columns=headers)
    df_gk = df_gk.reindex(columns=headers)
    df_all = df.append(df_gk)

    rarity_condlist = [df_all['Rtg'] >= 75, (65 <= df_all['Rtg']) & (df_all['Rtg'] <= 74), df_all['Rtg'] <= 64]
    rarity_choicelist = ["Gold", "Silver", "Bronze"]
    df_out = add_column(df_all, 'Rarity', rarity_condlist, rarity_choicelist)

    df_out.to_csv('clean_fut21_data.csv', index=False)

if __name__ == "__main__":
    main()