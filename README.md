# Natural Language to SQL Query Translator

## Proje Hakkında

Bu proje, kullanıcıların doğal dilde yazdıkları sorguları otomatik olarak SQL sorgularına çeviren yenilikçi bir sistemdir. Geleneksel olarak, veritabanı sorguları yazmak için SQL gibi teknik bir dilin öğrenilmesi ve kullanılması gerekmektedir. Ancak, bu proje, doğal dil işleme (NLP) ve yapay zeka (AI) teknolojilerini birleştirerek bu süreci otomatikleştirir ve kullanıcıların SQL bilgisi olmadan veritabanları ile etkileşim kurmasını sağlar.

Proje, veritabanı şemalarını anlama, doğru tablo ve alanları seçme, ve sorguyu doğru şekilde oluşturma gibi karmaşık görevleri yerine getirebilecek kapasitede bir yapay zeka modeli içerir. Bu yetenek, projeyi veritabanı yönetimi ve veri analizi süreçlerinde devrim yaratabilecek bir araç haline getirir.

## Kullanım Alanları

Bu projenin sunduğu teknoloji, çeşitli alanlarda ve senaryolarda geniş bir uygulama yelpazesine sahiptir:

### 1. **Veri Analizi**
Veri analistleri, genellikle büyük miktarda veri üzerinde sorgulamalar yaparak anlamlı sonuçlar elde etmek zorundadır. Bu proje, analistlerin SQL öğrenmeden hızlı bir şekilde sorgulamalar yapabilmesine olanak tanır. Bu da analistlerin işlerini daha hızlı ve verimli yapmalarını sağlar.

### 2. **İş Zekası (BI)**
İş zekası uzmanları, raporlar oluşturmak ve stratejik kararlar almak için sürekli olarak veritabanlarına başvururlar. Bu araç, doğal dil ile yazılmış soruları SQL sorgularına çevirerek, karar vericilerin veriye dayalı kararları daha hızlı alabilmesine yardımcı olur.

### 3. **Müşteri Destek Sistemleri**
Müşteri destek ekipleri, kullanıcıların sorunlarını çözmek için sıklıkla veritabanı sorguları yapar. Bu araç, destek personelinin teknik detaylara girmeden hızlıca bilgiye ulaşmasını sağlayarak müşteri hizmetlerini geliştirir.

### 4. **Eğitim**
Bu proje, SQL öğrenmekte olan öğrenciler için bir eğitim aracı olarak da kullanılabilir. Öğrenciler, doğal dildeki sorularının SQL sorgusuna nasıl dönüştüğünü görerek SQL öğrenimini hızlandırabilir.

### 5. **Veritabanı Yönetim Sistemleri**
Bu sistem, veritabanı yöneticileri tarafından veritabanı yönetimi süreçlerini kolaylaştırmak için kullanılabilir. Yönetici, karmaşık SQL sorgularını yazmadan veritabanını yönetebilir.

## Proje Yapısı

Proje, aşağıdaki temel bileşenlerden oluşmaktadır:

### 1. Embeddings
`embeddings.py`

Bu modül, veritabanı şemalarının ve kullanıcı sorgularının vektör uzayında temsil edilmesini sağlar. Bu sayede, yapay zeka modelinin veritabanı şemasını daha iyi anlaması ve doğru tabloları seçebilmesi sağlanır.

- **Kullanılan Teknolojiler:**
  - **Sentence Transformers:** Cümleleri ve metinleri vektörlere dönüştürmek için kullanılan bir kütüphane.
  - **Pinecone:** Vektör veritabanı yönetimi için kullanılan bir araç.

### 2. Dil Modeli
`language_model.py`

Bu modül, kullanıcı tarafından girilen doğal dil sorgularını SQL sorgularına dönüştürmek için kullanılır. Model, sorguyu analiz eder, gerekli tabloları ve kolonları seçer, ardından uygun SQL sorgusunu oluşturur.

- **Kullanılan Teknolojiler:**
  - **Transformers:** Doğal dil işleme görevlerinde kullanılan güçlü bir dil modeli çerçevesi.
  - **Hugging Face:** Transformer modellerinin entegrasyonu ve yönetimi için kullanılan kütüphane.

### 3. Veri Dönüşümleri
`csv_to_sql.py`, `xlsx_to_sql.py`

Bu modüller, CSV veya Excel formatındaki veri dosyalarını SQL formatına dönüştürmek için kullanılır. Bu dönüşüm, verilerin veritabanına daha kolay entegre edilmesini sağlar.

- **Kullanılan Teknolojiler:**
  - **Pandas:** Veri işleme ve analizi için kullanılan güçlü bir kütüphane.
  - **Openpyxl:** Excel dosyalarıyla çalışmak için kullanılan bir kütüphane.

### 4. Kullanıcı Arayüzü
`run.py`

Projenin kullanıcı arayüzü, Gradio platformu üzerinden sağlanmaktadır. Gradio, kullanıcıların web tarayıcısı üzerinden kolayca etkileşime girebileceği bir arayüz sunar.

- **Kullanılan Teknolojiler:**
  - **Gradio:** Makine öğrenimi modellerini ve diğer uygulamaları hızlı bir şekilde web arayüzüne entegre etmek için kullanılan bir kütüphane.
  - **FastAPI:** Yüksek performanslı web API'leri oluşturmak için kullanılan modern bir framework.

## Teknolojiler ve Kütüphaneler

Projede kullanılan başlıca teknolojiler ve kütüphaneler şunlardır:

- **Python:** Projenin ana programlama dili.
- **Transformers (Hugging Face):** Doğal dil işleme modellerini kullanmak için.
- **Gradio:** Kullanıcı arayüzü geliştirmek için.
- **Pandas:** Veri işleme ve dönüşüm görevleri için.
- **Pinecone:** Vektör veritabanı yönetimi için.
- **FastAPI:** Web arayüzü için yüksek performanslı bir API framework.

## Dosya Yapısı

- `embeddings.py`: Veritabanı şemalarını ve kullanıcı sorgularını vektörlere dönüştürme.
- `language_model.py`: Doğal dil sorgularını SQL sorgularına çevirme.
- `csv_to_sql.py`: CSV dosyalarını SQL'e dönüştürme.
- `xlsx_to_sql.py`: Excel dosyalarını SQL'e dönüştürme.
- `run.py`: Gradio kullanıcı arayüzünü çalıştıran ana dosya.
- `requirements.txt`: Proje için gerekli Python paketlerinin listesi.

## Sonuç

Bu proje, karmaşık veritabanı sorgularını herkesin erişimine açarak, veri analizi, iş zekası, müşteri destek sistemleri gibi birçok alanda kullanım potansiyeline sahiptir. Doğal dil işleme ve yapay zeka teknolojilerini kullanarak, veritabanlarıyla etkileşim kurmayı daha sezgisel ve erişilebilir hale getirir.
