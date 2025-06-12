import pandas as pd
import matplotlib.pyplot as plt

# === 1. Chargement du fichier ===
df = pd.read_csv(
    'C:/Users/Donete/Documents/Projets/доставка/doneteanalcs.csv',
    encoding='cp1251',
    sep=';'
)

# === 2. Conversion des dates ===
df['Дата заказа'] = pd.to_datetime(df['Дата заказа'], dayfirst=True)
df['Дата отправки'] = pd.to_datetime(df['Дата отправки'], dayfirst=True)
df['Дата доставки'] = pd.to_datetime(df['Дата доставки'], dayfirst=True)

# === 3. Calcul des délais ===
df['Фактическое время доставки (дни)'] = (df['Дата доставки'] - df['Дата отправки']).dt.days
df['Задержка (дни)'] = df['Фактическое время доставки (дни)'] - df['Ожидаемое время доставки (дни)']
df['Есть задержка'] = df['Задержка (дни)'] > 0

# === 4. Statistiques principales ===
pourcentage_retards = df['Есть задержка'].mean() * 100
moyenne_retard = df['Задержка (дни)'].mean()

print(f" Процент заказов с задержкой: {pourcentage_retards:.2f}%")
print(f" Средняя задержка (в днях): {moyenne_retard:.2f}")

# === 5. Analyse par transporteur ===
retards_par_transport = df.groupby('Транспортная компания')['Задержка (дни)'].mean().sort_values(ascending=False)
print("\n Средняя задержка по транспортной компании:")
print(retards_par_transport)

# === 6. Analyse par ville de destination ===
retards_par_ville = df.groupby('Город назначения')['Есть задержка'].sum().sort_values(ascending=False)
print("\n Количество задержек по городу назначения:")
print(retards_par_ville)

# === 7. Visualisation ===
# Histogramme des retards
plt.figure(figsize=(8, 5))
df['Задержка (дни)'].hist(bins=15, color='skyblue', edgecolor='black')
plt.title("Распределение задержек доставки (в днях)")
plt.xlabel("Задержка (дни)")
plt.ylabel("Количество заказов")
plt.grid(True)
plt.tight_layout()
plt.savefig("д1.png")
plt.show()

# Camembert : répartition des livraisons en retard
plt.figure(figsize=(5, 5))
df['Есть задержка'].value_counts().plot.pie(
    labels=['Вовремя', 'С задержкой'],
    autopct='%1.1f%%',
    colors=['lightgreen', 'salmon'],
    startangle=90
)
plt.title("Доля заказов с задержкой")
plt.ylabel("")
plt.tight_layout()
plt.savefig("д2.png")
plt.show()
