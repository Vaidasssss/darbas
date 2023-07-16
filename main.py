#Importuojame bibliotekas kurios bus naudojamos analizei atlikti
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
# Nuskaitome duomenų failą
df = pd.read_csv('gim_mir.csv', encoding="utf8")


#Formatuojame duomenis
df['Laikotarpis'] = pd.to_datetime(df['Laikotarpis'], format='%Y')
df['Metai'] = df['Laikotarpis'].dt.year
df['Metai'] = df['Metai'].astype(str)


# Pakeičiame reikšmes stulpelyje "Lytis" žodį 'ir' į simbolį '&'
df['Lytis'] = df['Lytis'].str.replace('ir', '&')
lytis = df['Lytis']



# Filtruojame tik 'gimusius', grupuodami pagal metus ir lytį gauname gimusiųjų skaičių
gimusieji = df[(df['Rodiklis'] == 'Gimusieji') & (df['Lytis']== 'Vyrai & moterys')]
gimusieji = gimusieji.groupby('Metai')['Reikšmė'].sum()

#Spausdiname duomenis gimusius
print(f"\nGimusieji:\n {gimusieji}\n")


# Filtruojame tik mirusius, grupuodami pagal metus ir pagal lytį gauname mirusiųjų skaičių
mirusieji = df[(df['Rodiklis'] == 'Mirusieji') & (df['Lytis']== 'Vyrai & moterys')]
mirusieji = mirusieji.groupby(['Metai'])['Reikšmė'].sum()

#Spausdiname duomenis apie mirusius
print(f"\nMirusieji:\n {mirusieji}\n")

#Aprašomas linijinės diagramos kodas
plt.figure(figsize=(10, 6))
plt.subplots_adjust(bottom=0.3)
gimusieji.plot()
mirusieji.plot()
plt.title('Gimusiųjų ir mirusiųjų kreivė pagal metus')
plt.xlabel('Metai')
plt.ylabel('Skaičius')
plt.legend(['Gimstamumas', 'Mirštamumas'])
plt.show()


# Filtruojame tik mirusias moteris, grupuodami pagal metus, gauname mirusiųjų skaičių
mirusieji_mot = df[(df['Rodiklis']== 'Mirusieji') & (df['Lytis']== 'Moterys')]
mirusieji_mot = mirusieji_mot.groupby('Metai')['Reikšmė'].sum()

#Spausdiname duomenis apie moteris
print(f"\nMirusios moterys:\n {mirusieji_mot}\n")

# Filtruojame tik murusius vyrus, grupuojame pagal metus, gauname mirusiųjų skaičių
mirusieji_vyr = df[(df['Rodiklis']== 'Mirusieji') & (df['Lytis']== 'Vyrai')]
mirusieji_vyr = mirusieji_vyr.groupby(['Metai'])['Reikšmė'].sum()

#Spausdiname duomenis apie vyrus
print(f"\nMirusieji vyrai:\n {mirusieji_vyr}\n")

# Mirusios moterys pagal laikotarpį linijinė diagrama
labels = mirusieji.index
plt.figure(figsize=(10, 6))
plt.plot(mirusieji_mot)
plt.plot(mirusieji_vyr)
plt.title("Mirusieji pagal lytį ir metus")
plt.xlabel('Metai')
plt.ylabel('Skaičius')
plt.legend(['Vyrai', 'Moterys'])
plt.show()




# Apskaičiuojame metinį mirčių sumažėjimą procentais kiekvienais metais
# Sukuriama linijinė diagrama kurioje matosi metiniai mirčių pokyčiai
# Naudojant numpy fuinkcijas apskaičiavome tendencijos liniją kuri nuprognozuotų ateities mirčių pokyčius
metai = np.array([2018, 2019, 2020, 2021, 2022])
mirtys = np.array([79148, 76562, 87094, 95492, 85768])
metinis_mirciu_pokytis= (mirtys[1:] - mirtys[:-1]) / mirtys[:-1] * 100

#Skaičiuojamas maximalus mirtingumas per metus
maxmirtys = np.max(mirtys)
#Skaičiuojame penkių metų vidurkį
avgmirtys = np.mean(mirtys)
#Spausdinama maximalus mirtingumas
print(f"Daugiausiai mirusiųjų per metus, pekių metų laikotarpyje: {maxmirtys}")
#Spausdinamas penkių metų vidurkis
print(f"Mirčių vidurkis per penkis metus: {avgmirtys}")

#Tendencijos ir prognozės atvaizdavimas
plt.figure(figsize=(10, 6))
plt.plot(metai[1:], metinis_mirciu_pokytis, marker='o', color='blue')
plt.xlabel('Metai')
plt.ylabel('Mirčių pokytis %')
plt.title('Metiniai mirčių pokyčiai ir prognozė')

tendencija= np.polyfit(metai[1:], metinis_mirciu_pokytis, 1)
prognoze= np.polyval(tendencija, metai[1:])

plt.plot(metai[1:], prognoze, color='red')
plt.legend(['Tendecija', 'Prognozės'])

plt.show()


# Filtruojame tik vyrus ir moteris, grupuojame apskkritis
gim_apskritys = df[(df['Lytis']=='Vyrai & moterys')]
gim_apskritys = gim_apskritys.groupby(['Administracinė teritorija', 'Rodiklis'])['Reikšmė'].sum()
print(f"\nGimusieji ir mirusieji pagal apskritis 2018-2022:\n {gim_apskritys}\n")

#Gimusiųjų ir mirusiųjų stulpelinė diagrama pagal apskritis
plt.figure(figsize=(10, 6))
gim_apskritys.plot(kind='bar', color=['blue', 'red'])
plt.title('Mirtingumas ir gimstamumas pagal apskritis 2018-2022')
plt.ylabel('Skaičius')
plt.subplots_adjust(bottom=0.4)

plt.show()


