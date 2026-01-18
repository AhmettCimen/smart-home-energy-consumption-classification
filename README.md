# Akıllı Ev Enerji Tüketimi Tahmini Projesi

Bu proje amaç akıllı ev verilerini , hava durumunu ve bazı diğer ortam verilerini (Sıcaklık, Nem) kullanarak evin enerji tüketiminin ortalamanın üzerinde olup olmadığını tahmin etmektir.Geliştirilen projede 3 farklı makine öğrenmesi modeli kullanılmıştır.



# Veri Seti ve Ön Hazırlık

Projede Smart Home Dataset.csv veri seti kullanılmıştır. 
İlk adımda veri setindeki eksik değerler temizlenmiştir.                     
![1](Results/1.png)                 
Zaman bilgisi saniye cinsinden (Unix timestamp) olduğu için okunabilir tarih formatına çevrildi ve bu tarihten saat bilgisi (hour) ayrı bir özellik olarak çıkarılmıştır.                            
![2](Results/2.png)                

Bu işlem sayesinde model, günün hangi saatinde enerji tüketiminin arttığını veya azaldığını öğrenebilir hale gelmiştir.

Hava durumu ile ilgili sıcaklık, nem, rüzgar hızı gibi sütunlar da sayısal formata dönüştürüldü.
![3](Results/3.png)


#burada biraz pivotlardan ve nasıl yapıldığından bahsedicem


# Veri Analizi Grafikleri

Enerji tüketiminin farklı koşullara göre nasıl değiştiğini görmek için çeşitli grafikler oluşturulmuştur.

### Saate Göre Enerji Tüketimi
![saate enerjş](Results/Change_by_Hour.png) 

### Neme Göre Enerji Tüketimi
![nem enerji](Results/Change_by_Humidity.png)

### Sıcaklığa Göre Enerji Tüketimi
![sıcaklık eneri](Results/Change_by_Temperature.png)


# Hedef Değişken ve Ölçeklendirme

Tahmin edilmek istenen değer enerji tüketimidir. Bu problem sınıflandırmaya çevrilmiştir:

- Tüketim ortalamanın üzerindeyse: 1  
- Tüketim ortalamanın altındaysa: 0  

Özellikler arasında sayısal fark çok olduğu için StandardScaler kullandım. 
Not: Herhangi bir ölçceklendirme kullanmadan denediğimde Train kısmı çok uzun sürüyordu özellikle Logistic Regression modelinde. O yüzden StandartScaler kullandım.


# Modellerin Eğitimi ve Sonuçlar

Veriyi %80 eğitim, %20 test olacak şekilde ayırdım. 
3 Farklı modelde sonuçları inceledim

- Lojistik Regresyon  
- KNN (K-Nearest Neighbors)  
- Random Forest  

### Logistic Regression Sonuçları
![Logistic Regression Results](Results/Logistic_Results.png)
Logistic Regression diğer modellere göre daha uzun sürmesine rağmen en başarısız model oldu.

### KNN Sonuçları
![KNN Results](Results/KNN_Results.png)

### Random Forest Sonuçları
![Random Forest Results](Results/RandomForest_Results.png)


# Feature'ların Önem Sırası

Enerji tüketimini tahmin ederken hangi özelliklerin daha etkili olduğu analiz edilmiştir. Özellikle pivot tablolar ile eklenen ortalama tüketim özelliklerinin (hourAvg, temperatureAvg vb.) model üzerinde önemli bir etkisi olduğu görülmüştür.

![özellik önem](Results/ImportanceG.png)


## Genel Değerlendirme

- Random Forest modeli %85'in üzerinde sonuç alarak en başarılı sonucu vermiştir
- Baseline oluşturarak elde edilen referans noktaları, tüketimi (düşük, yüksek)sınıflandırmada yardımcı oldu
- Saat ve hava durumu bilgileri enerji tüketimini ciddi şekilde etkilemektedir
- Pivot tabloları, sade verisetindeki karmaşıklıktan kurtarıp veriyi gruplandırmada çok işlevsel bi araç oldu.


