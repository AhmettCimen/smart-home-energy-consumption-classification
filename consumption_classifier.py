import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score,classification_report
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler # scaler kullandım linear regressiion çok uzun sürdüğü için
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('Smart Home Dataset.csv', low_memory=False) # büyük çaplı veriler için low_memory=False  
df = df.dropna()


df['time'] = pd.to_numeric(df['time'], errors='coerce') 
df['datetime'] = pd.to_datetime(df['time'], unit='s')
df['hour'] = df['datetime'].dt.hour


weather_columns = ['temperature', 'humidity', 'visibility', 'windSpeed', 'pressure', 'cloudCover', 'windBearing', 'dewPoint', 'precipProbability']
for col in weather_columns: 
    df[col] = pd.to_numeric(df[col], errors='coerce')




le = LabelEncoder()
df['summary_encoded'] = le.fit_transform(df['summary'].astype(str))



pivot_hour = df.pivot_table(index='hour', values='use [kW]') # burada pivotları olşturuyorum saate ,sıcaklık, nem ve rüzgara için pivot oluşturdum
pivot_hour.columns = ['hourAvg']

pivot_temp = df.pivot_table(index='temperature', values='use [kW]')
pivot_temp.columns = ['temperatureAvg'] 

pivot_humid = df.pivot_table(index='humidity', values='use [kW]')
pivot_humid.columns = ['humidityAvg'] 

pivot_wind = df.pivot_table(index='windSpeed', values='use [kW]')
pivot_wind.columns = ['windSpeedAvg'] 

df = df.merge(pivot_hour, on='hour', how='left')
df = df.merge(pivot_temp, on='temperature', how='left')
df = df.merge(pivot_humid, on='humidity', how='left')
df = df.merge(pivot_wind, on='windSpeed', how='left')


y = (df['use [kW]'] > df['use [kW]'].mean()).astype(int)

features = [
    'hour', 'summary_encoded', 
    'temperature', 'humidity', 'visibility', 'windSpeed', 
    'pressure', 'cloudCover', 'windBearing', 'dewPoint', 'precipProbability',
    'hourAvg', 'temperatureAvg', 'humidityAvg', 'windSpeedAvg' 
]

X = df[features]
X = X.fillna(0) # merge sonrası NaN oluştu onları 0la doldrdum
scaler = StandardScaler() # scaler kullanmasm da sonuç benzer çıkıyor. ama scaler yokken modellerin fitlenmesi uzuyor 
X = scaler.fit_transform(X)


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

models = {
    "Logistic Regression": LogisticRegression(max_iter=7000), 
    "KNN Classification ": KNeighborsClassifier(n_neighbors=5),
    "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42)
}


for isim, model in models.items(): # yukarıda oluşturduğum modelleri sırsasıyla fitleyip acc2 skorunu printliyor
    print(f"\n{isim} eğitiliyor...")
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    acc2=accuracy_score(y_test,y_pred)
    print(f"acc2: {acc2} \n Sonuç: %{accuracy*100:.2f}") # çok uzun basamaklar yazmasın diye .2f
    print(classification_report(y_test,y_pred)) # 
    
    




rf_model = models["Random Forest"]
feature_names = features


fi_df = pd.DataFrame({'Feature': feature_names, 'Importance': rf_model.feature_importances_}) # feature önem sırası
fi_df = fi_df.sort_values(by='Importance', ascending=False)
#fi =feature importance 

plt.figure(figsize=(12, 8)) 
sns.barplot(x='Importance', y='Feature', data=fi_df, palette='viridis', hue='Feature', legend=False)
 # normalde bu kadar palet rengi parametrelerine vb gerek yok.ama önem grafiklerinde yaygın olarak renklendirme kullanıldığnı gördüm.

plt.title('Feature Importance Scores(Özelliklerin Önem Sırası)')
plt.xlabel('Importance Score(Önem Skoru)')
plt.ylabel('Features')
plt.grid(axis='x', linestyle='--', alpha=0.7) 
plt.tight_layout() 
plt.savefig("ImportanceG.png", dpi=300, bbox_inches='tight')


plt.show()


