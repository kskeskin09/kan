import streamlit as st
import pdfplumber
import re

# --- 1. VERİ YAPISI ---
TAHLIL_AYARLARI = {
    "BA#": {
        "grup": "Hemogram (Tam Kan Sayımı)",
        "bilgi": "Bağışıklık sisteminin alerji ve iltihap süreçlerinde rol oynayan en nadir beyaz kan hücreleridir. Vücudun dış uyarılara tepki vermesi veya içsel inflamasyon durumlarında sayıları değişir.",
        "mesajlar": {
            "Düşük": "Bazofil sayısının düşük olması klinik bir önem taşımaz ve genellikle bir sağlık sorunu işareti olarak kabul edilmez.",
            "Normal": "Bazofil seviyeniz normal; bağışıklık sisteminizin alerji yönetimi dengeli çalışmaktadır.",
            "Yüksek": "Bazofil sayınız yüksek; bu durum aktif bir alerjik sürece veya vücuttaki bir hassasiyete işaret edebilir."
        }
    },
    "BASO#": {
        "grup": "Hemogram (Tam Kan Sayımı)",
        "bilgi": "Bağışıklık sisteminin alerji ve iltihap süreçlerinde rol oynayan en nadir beyaz kan hücreleridir. Vücudun dış uyarılara tepki vermesi veya içsel inflamasyon durumlarında sayıları değişir.",
        "mesajlar": {
            "Düşük": "Bazofil sayısının düşük olması klinik bir önem taşımaz ve genellikle bir sağlık sorunu işareti olarak kabul edilmez.",
            "Normal": "Bazofil seviyeniz normal; bağışıklık sisteminizin alerji yönetimi dengeli çalışmaktadır.",
            "Yüksek": "Bazofil sayınız yüksek; bu durum aktif bir alerjik sürece veya vücuttaki bir hassasiyete işaret edebilir."
        }
    },
    "BA": {
        "grup": "Hemogram (Tam Kan Sayımı)",
        "bilgi": "Bağışıklık sisteminin alerji ve iltihap süreçlerinde rol oynayan en nadir beyaz kan hücreleridir. Vücudun dış uyarılara tepki vermesi veya içsel inflamasyon durumlarında sayıları değişir.",
        "mesajlar": {
            "Düşük": "Bazofil sayısının düşük olması klinik bir önem taşımaz ve genellikle bir sağlık sorunu işareti olarak kabul edilmez.",
            "Normal": "Bazofil seviyeniz normal; bağışıklık sisteminizin alerji yönetimi dengeli çalışmaktadır.",
            "Yüksek": "Bazofil sayınız yüksek; bu durum aktif bir alerjik sürece veya vücuttaki bir hassasiyete işaret edebilir."
        }
    },
    "BA%": {
        "grup": "Hemogram (Tam Kan Sayımı)",
        "bilgi": "Toplam beyaz kan hücreleri (akyuvarlar) içindeki bazofil oranını ifade eder, vücudun alerjik tepkileri ve kronik iltihaplanma süreçleriyle ilişkilidir. Vücudun dış uyarılara verdiği tepki veya savunma sisteminin uyarılma düzeyine göre değişir.",
        "mesajlar": {
            "Düşük": "Bazofil oranının düşük olması genellikle klinik olarak tek başına bir anlam taşımaz; ancak şiddetli stres, steroid kullanımı veya akut enfeksiyon süreçlerinde görülebilir.",
            "Normal": "Bazofil oranınız normal; bağışıklık sisteminizin alerji ve savunma dengesi ideal düzeydedir.",
            "Yüksek": "Bazofil oranınız yüksek; bu durum vücutta aktif bir alerjik sürece veya bir hassasiyete işaret edebilir."
        }
    },
    "BASO%": {
        "grup": "Hemogram (Tam Kan Sayımı)",
        "bilgi": "Toplam beyaz kan hücreleri (akyuvarlar) içindeki bazofil oranını ifade eder, vücudun alerjik tepkileri ve kronik iltihaplanma süreçleriyle ilişkilidir. Vücudun dış uyarılara verdiği tepki veya savunma sisteminin uyarılma düzeyine göre değişir.",
        "mesajlar": {
            "Düşük": "Bazofil oranının düşük olması genellikle klinik olarak tek başına bir anlam taşımaz; ancak şiddetli stres, steroid kullanımı veya akut enfeksiyon süreçlerinde görülebilir.",
            "Normal": "Bazofil oranınız normal; bağışıklık sisteminizin alerji ve savunma dengesi ideal düzeydedir.",
            "Yüksek": "Bazofil oranınız yüksek; bu durum vücutta aktif bir alerjik sürece veya bir hassasiyete işaret edebilir."
        }
    },
    "EO#": {
        "grup": "Hemogram (Tam Kan Sayımı)",
        "bilgi": "Bağışıklık sisteminin alerjik reaksiyonlar ve parazitlerle mücadele eden beyaz kan hücreleridir. Vücudun yabancı uyarılara karşı savunma geliştirdiği veya hassasiyet oluştuğu durumlarda sayıları değişir.",
        "mesajlar": {
            "Düşük": "Eozinofil sayısının düşük olması klinik olarak anlamlı değildir ve genellikle bir sağlık sorunu işareti olarak kabul edilmez.",
            "Normal": "Eozinofil seviyeniz normal; bağışıklık sisteminizin alerji ve savunma dengesi yerindedir.",
            "Yüksek": "Eozinofil sayınız yüksek; bu durum aktif bir alerjik sürece, vücutta bir hassasiyete veya yabancı maddelere karşı savunma tepkisine işaret edebilir."
        }
    },
    "EOS#": {
        "grup": "Hemogram (Tam Kan Sayımı)",
        "bilgi": "Bağışıklık sisteminin alerjik reaksiyonlar ve parazitlerle mücadele eden beyaz kan hücreleridir. Vücudun yabancı uyarılara karşı savunma geliştirdiği veya hassasiyet oluştuğu durumlarda sayıları değişir.",
        "mesajlar": {
            "Düşük": "Eozinofil sayısının düşük olması klinik olarak anlamlı değildir ve genellikle bir sağlık sorunu işareti olarak kabul edilmez.",
            "Normal": "Eozinofil seviyeniz normal; bağışıklık sisteminizin alerji ve savunma dengesi yerindedir.",
            "Yüksek": "Eozinofil sayınız yüksek; bu durum aktif bir alerjik sürece, vücutta bir hassasiyete veya yabancı maddelere karşı savunma tepkisine işaret edebilir."
        }
    },
    "EO%": {
        "grup": "Hemogram (Tam Kan Sayımı)",
        "bilgi": "Toplam beyaz kan hücreleri (akyuvarlar) içindeki eozinofil oranını ifade eder; vücudun alerjik tepkileri ve parazitlere karşı savunmasıyla ilişkilidir. Vücudun yabancı uyarılara verdiği tepki veya savunma sisteminin uyarılma düzeyine göre değişir.",
        "mesajlar": {
            "Düşük": "Eozinofil oranının düşük olması klinik olarak anlamlı değildir ve genellikle bir sağlık sorunu işareti olarak kabul edilmez.",
            "Normal": "Eozinofil oranınız normal; bağışıklık sisteminizin alerji ve savunma dengesi ideal düzeydedir.",
            "Yüksek": "Eozinofil oranınız yüksek; bu durum vücutta aktif bir alerjik sürece, yabancı bir uyarana veya savunma tepkisine işaret edebilir."
        }
    },
    "EOS%": {
        "grup": "Hemogram (Tam Kan Sayımı)",
        "bilgi": "Toplam beyaz kan hücreleri (akyuvarlar) içindeki eozinofil oranını ifade eder; vücudun alerjik tepkileri ve parazitlere karşı savunmasıyla ilişkilidir. Vücudun yabancı uyarılara verdiği tepki veya savunma sisteminin uyarılma düzeyine göre değişir.",
        "mesajlar": {
            "Düşük": "Eozinofil oranının düşük olması klinik olarak anlamlı değildir ve genellikle bir sağlık sorunu işareti olarak kabul edilmez.",
            "Normal": "Eozinofil oranınız normal; bağışıklık sisteminizin alerji ve savunma dengesi ideal düzeydedir.",
            "Yüksek": "Eozinofil oranınız yüksek; bu durum vücutta aktif bir alerjik sürece, yabancı bir uyarana veya savunma tepkisine işaret edebilir."
        }
    },
    "HCT": {
        "grup": "Hemogram (Tam Kan Sayımı)",
        "bilgi": "Kanın hacimsel olarak alyuvar oranını gösteren bir değerdir; vücudun oksijen taşıma kapasitesi ve sıvı dengesiyle ilişkilidir. Sıvı kaybı veya alyuvar üretimindeki değişimlere bağlı olarak seviyesi değişir.",
        "mesajlar": {
            "Düşük": "Hematokrit oranınız düşük; bu durum kanın oksijen taşıma kapasitesinin azaldığına veya vücuttaki sıvı miktarının arttığına işaret edebilir.",
            "Normal": "Hematokrit oranınız normal; kan bileşenleriniz ve sıvı dengeniz ideal uyum içerisindedir.",
            "Yüksek": "Hematokrit oranınız yüksek; bu durum vücudun sıvı kaybetmiş olmasına veya oksijen ihtiyacını karşılamak için hücre üretiminin artmasına işaret edebilir."
        }
    },
    "Hematokrit": {
        "grup": "Hemogram (Tam Kan Sayımı)",
        "bilgi": "Kanın hacimsel olarak alyuvar oranını gösteren bir değerdir; vücudun oksijen taşıma kapasitesi ve sıvı dengesiyle ilişkilidir. Sıvı kaybı veya alyuvar üretimindeki değişimlere bağlı olarak seviyesi değişir.",
        "mesajlar": {
            "Düşük": "Hematokrit oranınız düşük; bu durum kanın oksijen taşıma kapasitesinin azaldığına veya vücuttaki sıvı miktarının arttığına işaret edebilir.",
            "Normal": "Hematokrit oranınız normal; kan bileşenleriniz ve sıvı dengeniz ideal uyum içerisindedir.",
            "Yüksek": "Hematokrit oranınız yüksek; bu durum vücudun sıvı kaybetmiş olmasına veya oksijen ihtiyacını karşılamak için hücre üretiminin artmasına işaret edebilir."
        }
    },
    "HGB": {
        "grup": "Hemogram (Tam Kan Sayımı)",
        "bilgi": "Alyuvarlarda bulunan ve dokulara oksijen taşıyan proteindir; vücudun enerji seviyesiyle ilişkilidir. Kan üretimi, demir dengesi veya oksijen ihtiyacındaki değişimlere göre seviyesi değişir.",
        "mesajlar": {
            "Düşük": "Hemoglobin değeriniz düşük; bu durum vücudun oksijen taşıma kapasitesinin azaldığına ve enerji üretiminin yavaşladığına işaret edebilir.",
            "Normal": "Hemoglobin seviyeniz normal; dokularınıza yeterli düzeyde oksijen taşınmakta ve kan üretiminiz dengeli ilerlemektedir.",
            "Yüksek": "Hemoglobin değeriniz yüksek; bu durum vücudun sıvı kaybetmiş olmasına veya oksijen ihtiyacını karşılamak için hücre üretimini artırmasına işaret edebilir."
        }
    },
    "Hgb miktarı": {
        "grup": "Hemogram (Tam Kan Sayımı)",
        "bilgi": "Alyuvarlarda bulunan ve dokulara oksijen taşıyan proteindir; vücudun enerji seviyesiyle ilişkilidir. Kan üretimi, demir dengesi veya oksijen ihtiyacındaki değişimlere göre seviyesi değişir.",
        "mesajlar": {
            "Düşük": "Hemoglobin değeriniz düşük; bu durum vücudun oksijen taşıma kapasitesinin azaldığına ve enerji üretiminin yavaşladığına işaret edebilir.",
            "Normal": "Hemoglobin seviyeniz normal; dokularınıza yeterli düzeyde oksijen taşınmakta ve kan üretiminiz dengeli ilerlemektedir.",
            "Yüksek": "Hemoglobin değeriniz yüksek; bu durum vücudun sıvı kaybetmiş olmasına veya oksijen ihtiyacını karşılamak için hücre üretimini artırmasına işaret edebilir."
        }
    },
    "IG#": {
        "grup": "Hemogram (Tam Kan Sayımı)",
        "bilgi": "Kemik iliğinde üretilen ancak henüz tam olgunlaşmamış beyaz kan hücrelerinin sayısıdır; vücudun acil savunma ihtiyacıyla ilişkilidir. Genellikle aktif bir enfeksiyon veya vücudun yoğun bir uyaranla karşılaştığı durumlarda sayıları değişir.",
        "mesajlar": {
            "Düşük": "İmmatür granülosit sayınız referans değerin altında; bu durum genellikle vücudun acil bir hücre üretimine ihtiyaç duymadığını gösterse de, bağışıklık sistemi kapasitesindeki genel bir düşüklükle de ilişkili olabilir.",
            "Normal": "İmmatür granülosit sayınız normal; kemik iliğinizdeki hücre üretimi ve savunma sisteminiz dengeli bir seyir izlemektedir.",
            "Yüksek": "İmmatür granülosit sayınız yüksek; bu durum vücudun aktif bir enfeksiyonla mücadele ettiğine veya savunma sisteminin uyarıldığına işaret edebilir."
        }
    },
    "IG%": {
        "grup": "Hemogram (Tam Kan Sayımı)",
        "bilgi": "Olgunlaşmamış hücrelerin beyaz kan hücrelerine oranıdır. Enfeksiyon veya stres durumlarında değişebilir.",
        "mesajlar": {
            "Düşük": "İmmatür granülosit oranınız referans değerin altında; bu durum genellikle vücudun acil bir hücre üretimine ihtiyaç duymadığını gösterse de, bağışıklık sistemi kapasitesindeki genel bir düşüklükle de ilişkili olabilir.",
            "Normal": "İmmatür granülosit oranınız normal; kemik iliği üretimi ve savunma sisteminiz dengeli bir dağılım sergilemektedir.",
            "Yüksek": "İmmatür granülosit oranınız yüksek; bu durum vücudun aktif bir enfeksiyonla mücadele ettiğine veya savunma sisteminin uyarıldığına işaret edebilir."
        }
    },
    "LY#": {
        "grup": "Hemogram (Tam Kan Sayımı)",
        "bilgi": "Virüslere karşı savaşan ve bağışıklık hafızasını oluşturan temel akyuvar hücresidir. Enfeksiyonlara verilen yanıtlar veya savunma sisteminin uyarılma düzeyine göre sayısı değişir.",
        "mesajlar": {
            "Düşük": "Lenfosit sayınız düşük; bu durum bağışıklık sisteminin kapasitesinde bir azalmaya veya vücudun savunma mekanizmalarının baskılandığı bir sürece işaret edebilir.",
            "Normal": "Lenfosit seviyeniz normal; bağışıklık sisteminiz yabancı uyarılara karşı dengeli ve yeterli bir savunma potansiyeline sahiptir.",
            "Yüksek": "Lenfosit sayınız yüksek; bu durum vücudun aktif bir savunma halinde olduğuna veya bağışıklık sisteminin uyarıldığına işaret edebilir."
        }
    },
    "LYM#": {
        "grup": "Hemogram (Tam Kan Sayımı)",
        "bilgi": "Virüslere karşı savaşan ve bağışıklık hafızasını oluşturan temel akyuvar hücresidir. Enfeksiyonlara verilen yanıtlar veya savunma sisteminin uyarılma düzeyine göre sayısı değişir.",
        "mesajlar": {
            "Düşük": "Lenfosit sayınız düşük; bu durum bağışıklık sisteminin kapasitesinde bir azalmaya veya vücudun savunma mekanizmalarının baskılandığı bir sürece işaret edebilir.",
            "Normal": "Lenfosit seviyeniz normal; bağışıklık sisteminiz yabancı uyarılara karşı dengeli ve yeterli bir savunma potansiyeline sahiptir.",
            "Yüksek": "Lenfosit sayınız yüksek; bu durum vücudun aktif bir savunma halinde olduğuna veya bağışıklık sisteminin uyarıldığına işaret edebilir."
        }
    },
    "LY%": {
        "grup": "Hemogram (Tam Kan Sayımı)",
        "bilgi": "Toplam akyuvarlar içindeki lenfosit oranını ifade eder. Vücudun virüslere karşı savunması ve bağışıklık hafızasıyla ilişkilidir; enfeksiyonlara verilen yanıtlar veya savunma sisteminin uyarılma düzeyine göre değişir.",
        "mesajlar": {
            "Düşük": "Lenfosit oranınız düşük; bu durum bağışıklık sisteminin kapasitesinde bir azalmaya veya vücudun savunma mekanizmalarının baskılandığı bir sürece işaret edebilir.",
            "Normal": "Lenfosit oranınız normal; bağışıklık sisteminiz yabancı uyarılara karşı dengeli ve yeterli bir savunma potansiyeline sahiptir.",
            "Yüksek": "Lenfosit oranınız yüksek; bu durum vücudun aktif bir savunma halinde olduğuna veya bağışıklık sisteminin uyarıldığına işaret edebilir."
        }
    },
    "LYM%": {
        "grup": "Hemogram (Tam Kan Sayımı)",
        "bilgi": "Toplam akyuvarlar içindeki lenfosit oranını ifade eder. Vücudun virüslere karşı savunması ve bağışıklık hafızasıyla ilişkilidir; enfeksiyonlara verilen yanıtlar veya savunma sisteminin uyarılma düzeyine göre değişir.",
        "mesajlar": {
            "Düşük": "Lenfosit oranınız düşük; bu durum bağışıklık sisteminin kapasitesinde bir azalmaya veya vücudun savunma mekanizmalarının baskılandığı bir sürece işaret edebilir.",
            "Normal": "Lenfosit oranınız normal; bağışıklık sisteminiz yabancı uyarılara karşı dengeli ve yeterli bir savunma potansiyeline sahiptir.",
            "Yüksek": "Lenfosit oranınız yüksek; bu durum vücudun aktif bir savunma halinde olduğuna veya bağışıklık sisteminin uyarıldığına işaret edebilir."
        }
    },
    "MCH": {
        "grup": "Hemogram (Tam Kan Sayımı)",
        "bilgi": "Tek bir alyuvar hücresinin içerdiği ortalama hemoglobin miktarını ifade eder. Alyuvarların oksijen taşıma kapasitesi ve demir dengesiyle doğrudan ilişkilidir; kan üretimi ve vitamin düzeylerine göre seviyesi değişir.",
        "mesajlar": {
            "Düşük": "Hücre başına düşen hemoglobin miktarınız düşük; bu durum vücutta demir eksikliğine veya alyuvarların oksijen taşıma verimliliğinin azaldığına işaret edebilir.",
            "Normal": "Hücre başına düşen hemoglobin miktarınız normal; alyuvarlarınızın içeriği ve oksijen taşıma potansiyeli ideal düzeydedir.",
            "Yüksek": "Hücre başına düşen hemoglobin miktarınız yüksek; bu durum vitamin eksikliklerine veya alyuvarların yapısal değişimlerine bağlı olarak gelişen bir sürece işaret edebilir."
        }
    },
    "MCHC": {
        "grup": "Hemogram (Tam Kan Sayımı)",
        "bilgi": "Belirli bir hacimdeki alyuvarın içindeki hemoglobin yoğunluğunu ifade eder. Alyuvarların oksijen taşıma verimliliği ve demir dengesiyle ilişkilidir; kan üretimi ve hücre yapısına göre seviyesi değişir.",
        "mesajlar": {
            "Düşük": "Hücrelerinizdeki hemoglobin yoğunluğu düşük; bu durum vücutta demir eksikliğine veya alyuvarların oksijen taşıma kapasitesinin azaldığına işaret edebilir.",
            "Normal": "Hücrelerinizdeki hemoglobin yoğunluğu normal; alyuvarlarınızın içindeki hemoglobin yoğunluğu ve oksijen taşıma verimliliği ideal düzeydedir.",
            "Yüksek": "Hücrelerinizdeki hemoglobin yoğunluğu yüksek; bu durum alyuvarların yapısal değişimlerine veya vücudun sıvı kaybına bağlı olarak gelişen bir sürece işaret edebilir."
        }
    },
    "MCV": {
        "grup": "Hemogram (Tam Kan Sayımı)",
        "bilgi": "Tek bir kırmızı kan hücresinin (alyuvar) ortalama büyüklüğünü ifade eder. Alyuvarların gelişim süreci ve vitamin-mineral dengesiyle ilişkilidir; kan üretimi ve hücre yapısına göre seviyesi değişir.",
        "mesajlar": {
            "Düşük": "Alyuvarlarınız normalden küçük; bu durum vücutta demir eksikliğine veya alyuvar üretimindeki yapısal değişimlere işaret edebilir.",
            "Normal": "Alyuvarlarınızın boyutu normal; alyuvarlarınızın büyüklüğü ve oksijen taşıma potansiyeli ideal düzeydedir.",
            "Yüksek": "Alyuvarlarınız normalden büyük; bu durum bazı vitamin eksikliklerine veya alyuvarların gelişim sürecindeki değişimlere işaret edebilir."
        }
    },
    "MO#": {
        "grup": "Hemogram (Tam Kan Sayımı)",
        "bilgi": "Vücuttaki atıkları ve mikropları temizleyen çöpçü akyuvar hücresidir. Enfeksiyonlar, doku onarımı veya savunma sistemi yanıtlarına göre sayısı değişir.",
        "mesajlar": {
            "Düşük": "Monosit sayınız düşük; bu durum bağışıklık sisteminin baskılanmasına veya savunma kapasitesindeki geçici bir azalmaya işaret edebilir.",
            "Normal": "Monosit seviyeniz normal; bağışıklık sisteminiz temizleme ve savunma görevini dengeli bir şekilde sürdürmektedir.",
            "Yüksek": "Monosit sayınız yüksek; bu durum vücudun aktif bir enfeksiyonla mücadele ettiğine veya doku onarımı sürecinde olduğuna işaret edebilir."
        }
    },
    "MONO#": {
        "grup": "Hemogram (Tam Kan Sayımı)",
        "bilgi": "Vücuttaki atıkları ve mikropları temizleyen çöpçü akyuvar hücresidir. Enfeksiyonlar, doku onarımı veya savunma sistemi yanıtlarına göre sayısı değişir.",
        "mesajlar": {
            "Düşük": "Monosit sayınız düşük; bu durum bağışıklık sisteminin baskılanmasına veya savunma kapasitesindeki geçici bir azalmaya işaret edebilir.",
            "Normal": "Monosit seviyeniz normal; bağışıklık sisteminiz temizleme ve savunma görevini dengeli bir şekilde sürdürmektedir.",
            "Yüksek": "Monosit sayınız yüksek; bu durum vücudun aktif bir enfeksiyonla mücadele ettiğine veya doku onarımı sürecinde olduğuna işaret edebilir."
        }
    },
    "MO%": {
        "grup": "Hemogram (Tam Kan Sayımı)",
        "bilgi": "Toplam akyuvarlar içindeki monosit oranını ifade eden temizlikçi hücre değeridir. Vücuttaki kronik süreçler veya doku onarımı ihtiyacına göre bu oran değişir.",
        "mesajlar": {
            "Düşük": "Monosit oranınız düşük; bu durum bağışıklık sisteminin genel bir baskılanmasına veya savunma kapasitesindeki geçici bir azalmaya işaret edebilir.",
            "Normal": "Monosit oranınız normal; bağışıklık sisteminiz atıkları temizleme ve savunma görevini dengeli bir şekilde sürdürmektedir.",
            "Yüksek": "Monosit oranınız yüksek; bu durum vücudun aktif bir enfeksiyonla mücadele ettiğine veya doku onarımı sürecinde olduğuna işaret edebilir."
        }
    },
    "MONO%": {
        "grup": "Hemogram (Tam Kan Sayımı)",
        "bilgi": "Toplam akyuvarlar içindeki monosit oranını ifade eden temizlikçi hücre değeridir. Vücuttaki kronik süreçler veya doku onarımı ihtiyacına göre bu oran değişir.",
        "mesajlar": {
            "Düşük": "Monosit oranınız düşük; bu durum bağışıklık sisteminin genel bir baskılanmasına veya savunma kapasitesindeki geçici bir azalmaya işaret edebilir.",
            "Normal": "Monosit oranınız normal; bağışıklık sisteminiz atıkları temizleme ve savunma görevini dengeli bir şekilde sürdürmektedir.",
            "Yüksek": "Monosit oranınız yüksek; bu durum vücudun aktif bir enfeksiyonla mücadele ettiğine veya doku onarımı sürecinde olduğuna işaret edebilir."
        }
    },
    "MPV": {
        "grup": "Hemogram (Tam Kan Sayımı)",
        "bilgi": "Kanın pıhtılaşmasını sağlayan trombositlerin ortalama büyüklüğünü ifade eder. Kemik iliğindeki üretim hızı ve trombositlerin ömrü ile doğrudan ilişkilidir.",
        "mesajlar": {
            "Düşük": "Trombosit hacminiz düşük; bu durum pıhtılaşma hücrelerinin üretim hızında bir yavaşlamaya veya bağışıklık sisteminin bu hücreleri etkilediği bir sürece işaret edebilir.",
            "Normal": "Trombosit hacminiz normal; trombosit üretiminiz ve pıhtılaşma hücrelerinizin büyüklüğü ideal dengededir.",
            "Yüksek": "Trombosit hacminiz yüksek; bu durum vücudun aktif olarak yeni ve büyük pıhtılaşma hücreleri ürettiğine veya savunma sisteminin uyarıldığına işaret edebilir."
        }
    },
    "NE#": {
        "grup": "Hemogram (Tam Kan Sayımı)",
        "bilgi": "Bakterilerle savaşan temel savunma hücresidir. Enfeksiyonlara veya vücuttaki hasara göre sayısı değişir.",
        "mesajlar": {
            "Düşük": "Nötrofil sayınız düşük; bu durum bağışıklık sisteminin baskılanmasına veya enfeksiyonlara karşı savunma kapasitesinin azaldığına işaret edebilir.",
            "Normal": "Nötrofil seviyeniz normal; bağışıklık sisteminiz bakteriyel tehditlere karşı dengeli ve yeterli bir savunma potansiyeline sahiptir.",
            "Yüksek": "Nötrofil sayınız yüksek; bu durum vücudun aktif bir bakteriyel enfeksiyonla mücadele ettiğine veya iltihabi bir sürece işaret edebilir."
        }
    },
    "NE": {
        "grup": "Hemogram (Tam Kan Sayımı)",
        "bilgi": "Bakterilerle savaşan temel savunma hücresidir. Enfeksiyonlara veya vücuttaki hasara göre sayısı değişir.",
        "mesajlar": {
            "Düşük": "Nötrofil sayınız düşük; bu durum bağışıklık sisteminin baskılanmasına veya enfeksiyonlara karşı savunma kapasitesinin azaldığına işaret edebilir.",
            "Normal": "Nötrofil seviyeniz normal; bağışıklık sisteminiz bakteriyel tehditlere karşı dengeli ve yeterli bir savunma potansiyeline sahiptir.",
            "Yüksek": "Nötrofil sayınız yüksek; bu durum vücudun aktif bir bakteriyel enfeksiyonla mücadele ettiğine veya iltihabi bir sürece işaret edebilir."
        }
    },
    "NE%": {
        "grup": "Hemogram (Tam Kan Sayımı)",
        "bilgi": "Toplam akyuvarlar içindeki nötrofil oranını ifade eden temel savunma hücresi değeridir. Bakteriyel enfeksiyonlara veya vücuttaki hasara göre bu oran değişir.",
        "mesajlar": {
            "Düşük": "Nötrofil oranınız düşük; bu durum bağışıklık sisteminin baskılanmasına veya vücudun enfeksiyonlara karşı savunma kapasitesinin azaldığına işaret edebilir.",
            "Normal": "Nötrofil oranınız normal; bağışıklık sisteminiz bakteriyel tehditlere karşı dengeli ve yeterli bir savunma potansiyeline sahiptir.",
            "Yüksek": "Nötrofil oranınız yüksek; bu durum vücudun aktif bir bakteriyel enfeksiyonla mücadele ettiğine veya iltihabi bir sürece işaret edebilir."
        }
    },
    "NRBC#": {
        "grup": "Hemogram (Tam Kan Sayımı)",
        "bilgi": "Normalde kanda bulunmaması gereken çekirdekli genç alyuvar hücresidir. Kan üretiminin aşırı zorlandığı veya vücudun oksijensiz kaldığı durumlarda kana karışır.",
        "mesajlar": {
            "Düşük": "Çekirdekli genç alyuvar hücresi sayınız düşük; bu genellikle sağlıklı bir durum olsa da, referans altındaki seviyeler kemik iliğinin yeni alyuvar üretme kapasitesindeki bir yetersizliğe veya üretim sürecinin baskılandığına işaret edebilir.",
            "Normal": "Çekirdekli genç alyuvar hücresi sayınız normal; kan üretim sisteminiz dengeli çalışmaktadır.",
            "Yüksek": "Çekirdekli genç alyuvar hücresi sayınız yüksek; bu durum vücudun ciddi bir oksijen ihtiyacı duyduğuna veya kan üretiminin zorlandığına işaret edebilir."
        }
    },
    "NRBC%": {
        "grup": "Hemogram (Tam Kan Sayımı)",
        "bilgi": "Toplam akyuvarlar içindeki çekirdekli genç alyuvar oranını ifade eder. Normal şartlarda kanda bu hücrelerin görülmemesi beklenir; kan üretimindeki zorlanmaya göre bu oran değişir.",
        "mesajlar": {
            "Düşük": "Çekirdekli genç alyuvar hücresi oranınız düşük; bu genellikle sağlıklı kabul edilse de, referans altındaki seviyeler kemik iliğinin üretim kapasitesindeki bir yetersizliğe veya baskılanmaya işaret edebilir.",
            "Normal": "Çekirdekli genç alyuvar hücresi oranınız normal; kan üretim sisteminiz dengeli çalışmaktadır ve kana erken hücre salınımı gerçekleşmemektedir.",
            "Yüksek": "Çekirdekli genç alyuvar hücresi oranınız yüksek; bu durum vücudun ciddi bir oksijen ihtiyacı duyduğuna veya kan üretiminin aşırı zorlandığına işaret edebilir."
        }
    },
    "PCT": {
        "grup": "Hemogram (Tam Kan Sayımı)",
        "bilgi": "Kandaki toplam trombosit (pıhtılaşma hücresi) hacminin oransal değeridir. Pıhtılaşma dengesini ve enfeksiyon durumunu gösterir.",
        "mesajlar": {
            "Düşük": "Kanınızdaki toplam trombosit hacminin oransal değeri düşük; bu durum pıhtılaşma hücrelerinin azaldığına veya vücudun bu hücreleri hızla tükettiğine işaret edebilir.",
            "Normal": "Kanınızdaki toplam trombosit hacminin oransal değeri normal; pıhtılaşma sisteminiz ve PCT dengeniz ideal düzeydedir.",
            "Yüksek": "Kanınızdaki toplam trombosit hacminin oransal değeri yüksek; bu durum vücutta ciddi bir bakteriyel enfeksiyona veya pıhtılaşma sisteminin aşırı uyarıldığına işaret edebilir."
        }
    },
    "PDW": {
        "grup": "Hemogram (Tam Kan Sayımı)",
        "bilgi": "Trombositlerin (pıhtılaşma hücreleri) boyut farklılığını gösterir. Üretim hızı ve hücre yaşlanmasıyla ilişkilidir.",
        "mesajlar": {
            "Düşük": "Trombositleriniz arasındaki boyut farklılığı düşük; trombositleriniz benzer boyutlardadır, pıhtılaşma sisteminizin dengeli bir seyir izlediğine işaret edebilir.",
            "Normal": "Trombositleriniz arasındaki boyut farklılığı normal; trombosit boyut dağılımınız ideal dengededir.",
            "Yüksek": "Trombositleriniz arasındaki boyut farklılığı yüksek; trombosit boyutlarınız birbirinden çok farklıdır, pıhtılaşma sisteminin aşırı uyarıldığına işaret edebilir."
        }
    },
    "PLCR": {
        "grup": "Hemogram (Tam Kan Sayımı)",
        "bilgi": "Kandaki toplam trombositler arasındaki büyük hacimli (genç) hücrelerin oranını gösterir. Kemik iliğinin trombosit üretim hızını yansıtır.",
        "mesajlar": {
            "Düşük": "Kanınızdaki toplam trombositler arasındaki büyük hacimli (genç) hücrelerin oranı düşük; bu durum kemik iliğinde trombosit üretiminin yavaşladığına veya hücrelerin yaşlandığına işaret edebilir.",
            "Normal": "Kanınızdaki toplam trombositler arasındaki büyük hacimli (genç) hücrelerin oranı normal; trombosit üretim hızınız ve hücre gelişiminiz ideal dengededir.",
            "Yüksek": "Kanınızdaki toplam trombositler arasındaki büyük hacimli (genç) hücrelerin oranı yüksek; bu durum vücudun yoğun şekilde yeni ve büyük trombositler ürettiğine veya pıhtılaşma sisteminin uyarıldığına işaret edebilir."
        }
    },
    "P-LCR": {
        "grup": "Hemogram (Tam Kan Sayımı)",
        "bilgi": "Kandaki toplam trombositler arasındaki büyük hacimli (genç) hücrelerin oranını gösterir. Kemik iliğinin trombosit üretim hızını yansıtır.",
        "mesajlar": {
            "Düşük": "Kanınızdaki toplam trombositler arasındaki büyük hacimli (genç) hücrelerin oranı düşük; bu durum kemik iliğinde trombosit üretiminin yavaşladığına veya hücrelerin yaşlandığına işaret edebilir.",
            "Normal": "Kanınızdaki toplam trombositler arasındaki büyük hacimli (genç) hücrelerin oranı normal; trombosit üretim hızınız ve hücre gelişiminiz ideal dengededir.",
            "Yüksek": "Kanınızdaki toplam trombositler arasındaki büyük hacimli (genç) hücrelerin oranı yüksek; bu durum vücudun yoğun şekilde yeni ve büyük trombositler ürettiğine veya pıhtılaşma sisteminin uyarıldığına işaret edebilir."
        }
    },
    "PLT": {
        "grup": "Hemogram (Tam Kan Sayımı)",
        "bilgi": "Kanın pıhtılaşmasını sağlayan hücrelerdir. Yaralanma anında kanamayı durdurmak için görev yaparlar.",
        "mesajlar": {
            "Düşük": "Kanın pıhtılaşmasını sağlayan hücre miktarınız düşük; bu durum kanın pıhtılaşma hızının yavaşladığına ve kanama eğiliminin arttığına işaret edebilir.",
            "Normal": "Kanın pıhtılaşmasını sağlayan hücre miktarınız düşük normal; pıhtılaşma sisteminiz ve trombosit miktarınız ideal dengededir.",
            "Yüksek": "Kanın pıhtılaşmasını sağlayan hücre miktarınız düşük yüksek; bu durum vücudun pıhtılaşmaya meyilli olduğuna veya kemik iliğinin aşırı üretim yaptığına işaret edebilir."
        }
    },
    "RBC": {
        "grup": "Hemogram (Tam Kan Sayımı)",
        "bilgi": "Dokulara oksijen taşıyan kırmızı kan hücreleridir. Vücudun oksijen seviyesi ve kemik iliği sağlığıyla ilişkilidir.",
        "mesajlar": {
            "Düşük": "Dokulara oksijen taşıyan kırmızı kan hücrelerinizin sayısı düşük; bu durum kansızlığa (anemi) veya dokulara yeterli oksijen taşınamadığına işaret edebilir.",
            "Normal": "Dokulara oksijen taşıyan kırmızı kan hücrelerinizin sayısı normal; vücudunuzdaki oksijen taşıma kapasitesi ideal dengededir.",
            "Yüksek": "Dokulara oksijen taşıyan kırmızı kan hücrelerinizin sayısı yüksek; bu durum vücudun oksijen ihtiyacının arttığına veya sıvı kaybı yaşadığınıza işaret edebilir."
        }
    },
    "RDW-CV": {
        "grup": "Hemogram (Tam Kan Sayımı)",
        "bilgi": "Alyuvarların (kırmızı kan hücreleri) boyutları arasındaki farkı yüzde olarak gösterir. Hücrelerin ne kadar düzenli veya düzensiz yapıda olduğunu belirler.",
        "mesajlar": {
            "Düşük": "Alyuvarlarınızın (kırmızı kan hücreleri) boyutları arasındaki fark düşük; bu durum alyuvarlarınızın boyut olarak birbirine çok benzer (tek tip) olduğuna ve kan üretiminin stabil seyrettiğine işaret edebilir.",
            "Normal": "Alyuvarlarınızın (kırmızı kan hücreleri) boyutları arasındaki fark normal; alyuvar boyut dağılımınız ideal dengededir.",
            "Yüksek": "Alyuvarlarınızın (kırmızı kan hücreleri) boyutları arasındaki fark yüksek; bu durum alyuvar boyutları arasında büyük farklar olduğuna ve çeşitli kansızlık (anemi) türlerine işaret edebilir."
        }
    },
    "RDW CV": {
        "grup": "Hemogram (Tam Kan Sayımı)",
        "bilgi": "Alyuvarların (kırmızı kan hücreleri) boyutları arasındaki farkı yüzde olarak gösterir. Hücrelerin ne kadar düzenli veya düzensiz yapıda olduğunu belirler.",
        "mesajlar": {
            "Düşük": "Alyuvarlarınızın (kırmızı kan hücreleri) boyutları arasındaki fark düşük; bu durum alyuvarlarınızın boyut olarak birbirine çok benzer (tek tip) olduğuna ve kan üretiminin stabil seyrettiğine işaret edebilir.",
            "Normal": "Alyuvarlarınızın (kırmızı kan hücreleri) boyutları arasındaki fark normal; alyuvar boyut dağılımınız ideal dengededir.",
            "Yüksek": "Alyuvarlarınızın (kırmızı kan hücreleri) boyutları arasındaki fark yüksek; bu durum alyuvar boyutları arasında büyük farklar olduğuna ve çeşitli kansızlık (anemi) türlerine işaret edebilir."
        }
    },
    "RDW-SD": {
        "grup": "Hemogram (Tam Kan Sayımı)",
        "bilgi": "Alyuvarların (kırmızı kan hücreleri) boyut farkını doğrudan hacim olarak ölçer. Hücrelerin ne kadar düzensiz boyutta olduğunu gösteren hassas bir değerdir.",
        "mesajlar": {
            "Düşük": "Alyuvarlarınızın (kırmızı kan hücreleri) boyut farkı düşük; bu durum alyuvarlarınızın boyut olarak birbirine çok benzer (tek tip) olduğuna ve kan üretiminin stabil seyrettiğine işaret edebilir.",
            "Normal": "Alyuvarlarınızın (kırmızı kan hücreleri) boyut farkı normal; alyuvar boyut dağılımınız ideal dengededir.",
            "Yüksek": "Alyuvarlarınızın (kırmızı kan hücreleri) boyut farkı yüksek; bu durum alyuvar boyutları arasında belirgin farklar olduğuna ve çeşitli kansızlık (anemi) türlerine işaret edebilir."
        }
    },
    "RDW SD": {
        "grup": "Hemogram (Tam Kan Sayımı)",
        "bilgi": "Alyuvarların (kırmızı kan hücreleri) boyut farkını doğrudan hacim olarak ölçer. Hücrelerin ne kadar düzensiz boyutta olduğunu gösteren hassas bir değerdir.",
        "mesajlar": {
            "Düşük": "Alyuvarlarınızın (kırmızı kan hücreleri) boyut farkı düşük; bu durum alyuvarlarınızın boyut olarak birbirine çok benzer (tek tip) olduğuna ve kan üretiminin stabil seyrettiğine işaret edebilir.",
            "Normal": "Alyuvarlarınızın (kırmızı kan hücreleri) boyut farkı normal; alyuvar boyut dağılımınız ideal dengededir.",
            "Yüksek": "Alyuvarlarınızın (kırmızı kan hücreleri) boyut farkı yüksek; bu durum alyuvar boyutları arasında belirgin farklar olduğuna ve çeşitli kansızlık (anemi) türlerine işaret edebilir."
        }
    },
    "WBC": {
        "grup": "Hemogram (Tam Kan Sayımı)",
        "bilgi": "Vücudun savunma mekanizmasını oluşturan beyaz kan hücreleridir. Bağışıklık sisteminin enfeksiyonlara, iltihaba ve yabancı maddelere karşı verdiği yanıtı yansıtır.",
        "mesajlar": {
            "Düşük": "Vücudun savunma mekanizmasını oluşturan beyaz kan hücrelerinizin sayısı düşük; bu durum bağışıklık sisteminin zayıfladığına, vücudun enfeksiyonlara karşı savunmasız kaldığına veya kemik iliği baskılanmasına işaret edebilir.",
            "Normal": "Vücudun savunma mekanizmasını oluşturan beyaz kan hücrelerinizin sayısı seviyeniz normal; bağışıklık sisteminiz ve vücut savunmanız ideal dengededir.",
            "Yüksek": "Vücudun savunma mekanizmasını oluşturan beyaz kan hücrelerinizin sayısı yüksek; bu durum vücudun aktif bir enfeksiyonla, iltihabi bir süreçle veya fiziksel bir stresle mücadele ettiğine işaret edebilir."
        }
    },
    "Total IgE": {
        "grup": "Hemogram (Tam Kan Sayımı)",
        "bilgi": "Bağışıklık sistemi tarafından üretilen bir antikordur. Özellikle alerjik reaksiyonlar ve parazit enfeksiyonlarına karşı vücudun verdiği yanıtı gösterir.",
        "mesajlar": {
            "Düşük": "Total IgE düşük; bu durum bağışıklık sisteminin bazı alerjenlere karşı tepkisiz olduğuna veya nadiren bazı bağışıklık yetmezliklerine işaret edebilir.",
            "Normal": "Total IgE seviyeniz normal; vücudunuzun alerjik hassasiyeti ve parazitlere karşı savunma dengesi ideal düzeydedir.",
            "Yüksek": "Total IgE yüksek; bu durum vücudun bir alerjenle etkileşimde olduğuna, aktif bir alerjik sürece (astım, egzama vb.) veya parazit enfeksiyonuna işaret edebilir."
        }
    }
}

# --- 2. KOMBİNASYON KURALLARI ---
KOMBINASYON_KURALLARI = [
    {
        "ad": "Bakteriyel Enfeksiyon Eğiliimi",
        "kosullar": {"WBC": "Yüksek", "NE#": "Yüksek", "NE": "Yüksek", "NE%": "Yüksek", "LY#": "Düşük", "LYM#": "Düşük", "LY%": "Düşük","LYM%": "Düşük", "IG#": "Yüksek", "IG%": "Yüksek"},
        "tam_uyum": "🚨 Kan tablonuzdaki bulgular birbiriyle uyumlu olup, vücudunuzda bakteriyel bir enfeksiyon tablosuna işaret etmektedir. Tanının netleşmesi ve uygun tedavi protokolünün belirlenmesi için bir İç Hastalıkları (Dahiliye) veya Enfeksiyon Hastalıkları uzmanına başvurmanız faydalı olacaktır.",
        "kismi_uyum": "⚠️ Bazı kan değerlerinizdeki hafif sapmalar, başlangıç aşamasında veya seyri düşük bir bakteriyel enfeksiyon olasılığını akla getirmektedir. Bu bulguların klinik bir anlam taşıyıp taşımadığının netleşmesi için bir İç Hastalıkları (Dahiliye) veya Enfeksiyon Hastalıkları uzmanınına başvurmanız önerilir."
    },
    {
        "ad": "Viral Enfeksiyon Eğiliimi",
        "kosullar": {"WBC": "Düşük", "LY#": "Yüksek", "LYM#": "Yüksek", "LY%": "Yüksek", "LYM%": "Yüksek", "NE#": "Düşük", "NE": "Düşük", "NE%": "Düşük"},
        "tam_uyum": "🚨 Kan tablonuzdaki verilerin tamamı birbiriyle örtüşmektedir. Bu tablo, vücudunuzda viral bir enfeksiyon olasılığının oldukça yüksek olduğuna işaret etmektedir. Durumun netleşmesi ve vücut direncinizin takibi için vakit kaybetmeden bir İç Hastalıkları (Dahiliye) veya Enfeksiyon Hastalıkları uzmanına başvurmanız faydalı olacaktır.",
        "kismi_uyum": "⚠️ Bazı değerlerinizde dengesizlik görülmektedir. Bu bulgular başlangıç aşamasında bir enfeksiyona işaret ediyor olabilir. Vücudunuzun bir viral enfeksiyonla mücadele ediyor olabileceği ihtimalini göz önünde bulundurarak, belirtilerinizin takibi ve kesin teşhis için en kısa sürede bir İç Hastalıkları (Dahiliye) veya Enfeksiyon Hastalıkları uzmanına başvurmanız önerilir."
    },
    {
        "ad": "Alerjik Reaksiyon Eğilimi",
        "kosullar": {"EO#": "Yüksek", "EOS#": "Yüksek", "EO%": "Yüksek", "EOS%": "Yüksek", "BA#": "Yüksek", "BASO#": "Yüksek", "BA": "Yüksek", "BA%": "Yüksek", "BASO%": "Yüksek", "Total IgE": "Yüksek", "Total IgE": "Yüksek"},
        "tam_uyum": "🚨 Kan tablonuzdaki verilerin tamamı birbiriyle örtüşmektedir. Bu tablo, vücudunuzda alerjik bir reaksiyon veya aşırı duyarlılık olasılığının oldukça yüksek olduğuna işaret etmektedir. Reaksiyonun kaynağının belirlenmesi ve uygun tedavi için vakit kaybetmeden bir İç Hastalıkları (Dahiliye) veya Enfeksiyon Hastalıkları uzmanına başvurmanız faydalı olacaktır.",
        "kismi_uyum": "⚠️ Bazı değerlerinizde dengesizlik görülmektedir. Bu bulgular, vücudunuzun bir alerjene tepki verdiği veya alerjik bir durum eğilimi içerisinde olduğu şeklinde yorumlanabilir. Belirtilerinizin takibi ve kesin teşhis için en kısa sürede bir İç Hastalıkları (Dahiliye) veya Enfeksiyon Hastalıkları uzmanına başvurmanız önerilir."
    },
    {
        "ad": "Fiziksel Veya Psikolojik Stres Eğilimi",
        "kosullar": {"NE#": "Yüksek", "NE": "Yüksek", "NE%": "Yüksek", "LY#": "Düşük", "LYM#": "Düşük", "LY%": "Düşük", "LYM%": "Düşük", "WBC": "Yüksek"},
        "tam_uyum": "🚨 Kan tablonuzdaki verilerin tamamı birbiriyle örtüşmektedir. Bu tablo, vücudunuzun yüksek düzeyde fiziksel veya psikolojik bir stres altında olma olasılığının oldukça yüksek olduğuna işaret etmektedir. Bu durumun vücudunuzdaki etkilerini yönetmek ve altta yatan nedeni belirlemek için vakit kaybetmeden bir İç Hastalıkları (Dahiliye) veya Psikoloji uzmanına başvurmanız faydalı olacaktır.",
        "kismi_uyum": "⚠️ Bazı değerlerinizde dengesizlik görülmektedir. Bu bulgular, vücudunuzun bir stres faktörüyle mücadele ettiği veya fiziksel/psikolojik bir stres eğilimi içerisinde olduğu şeklinde yorumlanabilir. Durumun takibi ve kesin değerlendirme için en kısa sürede bir İç Hastalıkları (Dahiliye) veya Psikoloji uzmanına başvurmanız önerilir."
    },
    {
        "ad": "Kansızlık (Anemi) Eğilimi",
        "kosullar": {"HGB": "Düşük", "HCT": "Düşük", "Hematokrit": "Düşük", "RBC": "Düşük", "MCH": "Düşük", "MCHC": "Düşük", "MCV": "Düşük", "RDW-CV": "Yüksek"},
        "tam_uyum": "🚨 Kan tablonuzdaki verilerin tamamı birbiriyle örtüşmektedir. Bu tablo, vücudunuzda kansızlık (anemi) olasılığının oldukça yüksek olduğuna işaret etmektedir. Kansızlığın tipinin belirlenmesi ve gerekli desteğin planlanması için vakit kaybetmeden bir İç Hastalıkları (Dahiliye) veya Hematoloji uzmanına başvurmanız faydalı olacaktır.",
        "kismi_uyum": "⚠️ Bazı değerlerinizde dengesizlik görülmektedir. Bu bulgular, vücudunuzun kan üretiminde bir aksama olduğu veya kansızlık (anemi) eğilimi içerisinde olduğu şeklinde yorumlanabilir. Belirtilerinizin takibi ve kesin teşhis için en kısa sürede bir İç Hastalıkları (Dahiliye) veya Hematoloji uzmanına başvurmanız önerilir."
    },
    {
        "ad": "Demir Eksikliği Eğilimi",
        "kosullar": {"HGB": "Düşük", "MCV": "Düşük", "MCH": "Düşük", "RDW-CV": "Yüksek", "RDW CV": "Yüksek", "RDW-SD": "Yüksek", "RDW SD": "Yüksek", "MCHC": "Düşük"},
        "tam_uyum": "🚨 Kan tablonuzdaki verilerin tamamı birbiriyle örtüşmektedir. Bu tablo, vücudunuzda demir eksikliğine bağlı bir kansızlık olasılığının oldukça yüksek olduğuna işaret etmektedir. Eksikliğin derecesinin belirlenmesi ve uygun takviye planı için vakit kaybetmeden bir İç Hastalıkları (Dahiliye) veya Hematoloji uzmanına başvurmanız faydalı olacaktır.",
        "kismi_uyum": "⚠️ Bazı değerlerinizde dengesizlik görülmektedir. Bu bulgular, vücudunuzdaki demir depolarının azaldığı veya demir eksikliği eğilimi içerisinde olduğu şeklinde yorumlanabilir. Durumun netleşmesi için en kısa sürede bir İç Hastalıkları (Dahiliye) veya Hematoloji uzmanına başvurmanız önerilir."
    },
    {
        "ad": "B12 veya Folat (B9) Eksikliği Eğilimi",
        "kosullar": {"HGB": "Düşük", "MCV": "Yüksek", "RDW-SD": "Yüksek", "RDW SD": "Yüksek", "RDW-CV": "Yüksek", "RDW CV": "Yüksek", "MCH": "Yüksek"},
        "tam_uyum": "🚨 Kan tablonuzdaki verilerin tamamı birbiriyle örtüşmektedir. Bu tablo, vücudunuzda B12 vitamini veya Folat eksikliğine bağlı bir kansızlık olasılığının oldukça yüksek olduğuna işaret etmektedir. Sinir sistemi ve kan yapımı üzerindeki etkilerin önlenmesi için vakit kaybetmeden bir İç Hastalıkları (Dahiliye), Hematoloji veya Nöroloji uzmanına başvurmanız faydalı olacaktır.",
        "kismi_uyum": "⚠️ Bazı değerlerinizde dengesizlik görülmektedir. Bu bulgular, vücudunuzdaki vitamin depolarının yetersizliği veya vitamin eksikliği eğilimi içerisinde olduğu şeklinde yorumlanabilir. Kesin teşhis ve takviye planı için en kısa sürede bir İç Hastalıkları (Dahiliye), Hematoloji veya Nöroloji uzmanına başvurmanız önerilir."
    },
    {
        "ad": "Vücutta Sıvı Eksikliği (Dehidrasyon) Eğilimi",
        "kosullar": {"HGB": "Yüksek", "HCT": "Yüksek", "Hematokrit": "Yüksek", "RBC": "Yüksek"},
        "tam_uyum": "🚨 Kan tablonuzdaki verilerin tamamı birbiriyle örtüşmektedir. Bu tablo, vücudunuzda sıvı eksikliği (dehidratasyon) olasılığının oldukça yüksek olduğuna işaret etmektedir. Yetersiz sıvı alımı veya aşırı sıvı kaybı organ fonksiyonlarını etkileyebileceği için vakit kaybetmeden bir İç Hastalıkları (Dahiliye) uzmanına başvurmanız faydalı olacaktır.",
        "kismi_uyum": "⚠️ Bazı değerlerinizde yükselme görülmektedir. Bu bulgular, vücudunuzun yeterince hidre olmadığı veya sıvı eksikliği eğilimi içerisinde olduğu şeklinde yorumlanabilir. Günlük sıvı tüketiminizi gözden geçirmeniz ve durumun netleşmesi için en kısa sürede bir İç Hastalıkları (Dahiliye) uzmanına başvurmanız önerilir."
    },
    {
        "ad": "Pıhtılaşma Hücrelerinde Artış (Trombositoz) Eğilimi",
        "kosullar": {"PLT": "Yüksek", "PCT": "Yüksek", "MPV": "Yüksek", "PDW": "Yüksek", "PLCR": "Yüksek", "P-LCR": "Yüksek"},
        "tam_uyum": "🚨 Kan tablonuzdaki verilerin tamamı birbiriyle örtüşmektedir. Bu tablo, kanınızdaki pıhtılaşma hücrelerinin sayısında ve hücre hacmindeki artış olasılığının oldukça yüksek olduğuna işaret etmektedir. Bu durum kanın damar içindeki akışkanlığını ve pıhtılaşma riskini etkileyebileceği için vakit kaybetmeden bir İç Hastalıkları (Dahiliye) veya Hematoloji uzmanına başvurmanız faydalı olacaktır.",
        "kismi_uyum": "⚠️ Bazı değerlerinizde yükselme görülmektedir. Bu bulgular, vücudunuzun bir inflamasyona veya farklı bir uyarıya tepki olarak pıhtılaşma hücresi artış eğilimi gösterdiği şeklinde yorumlanabilir. Kesin teşhis ve takip için en kısa sürede bir İç Hastalıkları (Dahiliye) veya Hematoloji uzmanına başvurmanız önerilir."
    },
    {
        "ad": "Kan Pulu (Pıhtılaşma Hücresi) Eksikliği (Trombositopeni) Eğilimi",
        "kosullar": {"PLT": "Düşük", "PCT": "Düşük", "MPV": "Yüksek", "PDW": "Yüksek", "PLCR": "Yüksek", "P-LCR": "Yüksek"},
        "tam_uyum": "🚨 Kan tablonuzdaki verilerin tamamı birbiriyle örtüşmektedir. Bu tablo, kanınızdaki pıhtılaşma hücrelerinin sayısında belirgin bir azalma olasılığının oldukça yüksek olduğuna işaret etmektedir. Vücudun yeni hücre üretmeye çalıştığı ancak mevcut hücrelerin hızla tüketildiği bu tablo, kanama riskini artırabileceği için vakit kaybetmeden bir İç Hastalıkları (Dahiliye) veya Hematoloji uzmanına başvurmanız faydalı olacaktır.",
        "kismi_uyum": "⚠️ Bazı değerlerinizde dengesizlik görülmektedir. Bu bulgular, pıhtılaşma hücrelerinizin ömrünün kısaldığı veya bir pıhtılaşma hücresi eksikliği eğilimi içerisinde olduğunuz şeklinde yorumlanabilir. Durumun kontrol altına alınması için en kısa sürede bir İç Hastalıkları (Dahiliye) veya Hematoloji uzmanına başvurmanız önerilir."
    },
    {
        "ad": "Kan Hücresi Üretiminde Genel Azalma (Kemik İliği Baskılanması) Eğilimi",
        "kosullar": {"WBC": "Düşük", "RBC": "Düşük", "PLT": "Düşük", "HGB": "Düşük", "HCT": "Düşük", "Hematokrit": "Düşük", "PCT": "Düşük"},
        "tam_uyum": "🚨 Kan tablonuzdaki tüm ana hücre gruplarında (savunma, oksijen taşıma ve pıhtılaşma) bir düşüş görülmektedir. Bu tablo, vücudunuzda kan hücresi üretiminde genel bir azalma olasılığının oldukça yüksek olduğuna işaret etmektedir. Bağışıklık sistemi, enerji seviyesi ve pıhtılaşma dengesini doğrudan etkileyen bu durumun nedeninin (vitamin eksikliği, ilaç etkisi veya kemik iliği durumu) tespiti için vakit kaybetmeden bir Hematoloji veya İç Hastalıkları (Dahiliye) uzmanına başvurmanız şiddetle önerilir ve faydalı olacaktır..",
        "kismi_uyum": "⚠️ Kan hücrelerinizin birden fazla grubunda dengesizlik görülmektedir. Bu bulgular, vücudunuzun yeterli kan hücresi üretmekte zorlandığı veya bir üretim azalması eğilimi içerisinde olduğu şeklinde yorumlanabilir. Durumun ciddiyet kazanmaması için en kısa sürede bir Hematoloji veya İç Hastalıkları (Dahiliye) uzmanına başvurmanız önerilir."
    }
]

# --- 3. FONKSİYONLAR ---
def analiz_et(deger, ref_alt, ref_ust, param_adi):
    ayar = TAHLIL_AYARLARI.get(param_adi)
    if deger < ref_alt: durum = "Düşük"
    elif deger > ref_ust: durum = "Yüksek"
    else: durum = "Normal"
    return durum, ayar["mesajlar"].get(durum, durum), ayar.get("bilgi", "")

def pdf_oku(file):
    sonuclar = []
    with pdfplumber.open(file) as pdf:
        full_text = ""
        for page in pdf.pages:
            full_text += (page.extract_text() or "") + "\n"
        full_text = re.sub(r'[ \t]+', ' ', full_text)
        
        for p_key in TAHLIL_AYARLARI.keys():
            p_pattern = re.escape(p_key)
            pattern = rf"{p_pattern}[^0-9,.]*([\d\.,]+).*?([\d\.,]+)\s*-\s*([\d\.,]+)"
            match = re.search(pattern, full_text, re.IGNORECASE | re.DOTALL)
            if match:
                try:
                    raw_res = match.group(1).replace(',', '.')
                    raw_low = match.group(2).replace(',', '.')
                    raw_high = match.group(3).replace(',', '.')
                    sonuc_val = float(raw_res)
                    ref_min = float(raw_low)
                    ref_max = float(raw_high)
                    durum, mesaj, bilgi = analiz_et(sonuc_val, ref_min, ref_max, p_key)
                    sonuclar.append({
                        "ad": p_key, 
                        "sonuc": sonuc_val, 
                        "ref": f"{ref_min} - {ref_max}",
                        "durum": durum, 
                        "mesaj": mesaj, 
                        "bilgi": bilgi,
                        "grup": TAHLIL_AYARLARI[p_key]["grup"]
                    })
                except (ValueError, IndexError):
                    continue
    return sonuclar

# --- 4. ARAYÜZ (STREAMLIT) ---
st.set_page_config(page_title="SAnaliz Tahlil Analiz Sistemi", layout="wide")
st.title("SAnaliz Akıllı Tahlil Okuma ve Analiz Sistemi")

yuklenen_dosya = st.file_uploader("e-Nabız veya e-Devlet'ten aldığınız tahlil PDF'ini yükleyin", type=["pdf"])

if yuklenen_dosya:
    with st.spinner('Veriler analiz ediliyor...'):
        veriler = pdf_oku(yuklenen_dosya)
        
    if veriler:
        st.subheader("📊 Analiz Sonuçları")
        gruplar = list(dict.fromkeys([v['grup'] for v in veriler]))
        durum_sozlugu = {v['ad']: v['durum'] for v in veriler}

        for grup in gruplar:
            st.markdown(f"### {grup}")
            col_header = st.columns([1.5, 1, 1.5, 1.2, 4])
            col_header[0].write("**Parametre**")
            col_header[1].write("**Sonuç**")
            col_header[2].write("**Referans**")
            col_header[3].write("**Durum**")
            col_header[4].write("**Analiz Mesajı**")
            st.divider()
            
            for v in veriler:
                if v['grup'] == grup:
                    c1, c2, c3, c4, c5 = st.columns([1.5, 1, 1.5, 1.2, 4])
                    
                    # Hizalama için dikey boşluk miktarı
                    v_align = "padding-top:16px;"
                    
                    with c1:
                        # Bilgi balonunu (help) geri getirdik
                        # Boş bir div ile üstten boşluk verip altına normal markdown basıyoruz
                        st.markdown(f"<div style='padding-top:12px;'></div>", unsafe_allow_html=True)
                        st.markdown(f"**{v['ad']}**", help=v['bilgi'])
                        
                    with c2: 
                        st.markdown(f"<div style='{v_align}'>{v['sonuc']}</div>", unsafe_allow_html=True)
                    with c3: 
                        st.markdown(f"<div style='{v_align}'>{v['ref']}</div>", unsafe_allow_html=True)
                    with c4:
                        if v['durum'] == "Düşük": 
                            st.markdown(f"<div style='{v_align} color:#ff4b4b;'>📉 Düşük</div>", unsafe_allow_html=True)
                        elif v['durum'] == "Yüksek": 
                            st.markdown(f"<div style='{v_align} color:#ff4b4b;'>📈 Yüksek</div>", unsafe_allow_html=True)
                        else: 
                            st.markdown(f"<div style='{v_align} color:#09ab3b;'>✅ Normal</div>", unsafe_allow_html=True)
                    
                    with c5: 
                        st.info(v['mesaj'])

            st.write("")

        # --- RİSK ANALİZİ ---
        st.write("---")
        st.subheader("Toplu Risk Analizi")
        herhangi_bir_kombinasyon_var_mi = False
        for kural in KOMBINASYON_KURALLARI:
            eslesenler = [p for p, d in kural["kosullar"].items() if durum_sozlugu.get(p) == d]
            toplam = len(kural["kosullar"])
            if len(eslesenler) == toplam:
                st.error(f"🔴 **{kural['ad']}**: {kural['tam_uyum']}")
                herhangi_bir_kombinasyon_var_mi = True
            elif len(eslesenler) / toplam >= 0.5:
                st.warning(f"🟡 **{kural['ad']} (Kısmi Uyum)**: {kural['kismi_uyum']} (Riskli Parametreler: {', '.join(eslesenler)})")
                herhangi_bir_kombinasyon_var_mi = True
        
        if not herhangi_bir_kombinasyon_var_mi:
            st.success("Belirli bir riskli kombinasyon saptanmadı. Oldukça sağlıklı görünüyorsunuz.")
    else:
        st.warning("PDF içerisinde tanımladığınız parametrelerle eşleşen bir veri bulunamadı. Lütfen e-Nabız veya e-Devlet'ten aldığınız tahlil PDF'ini yükleyin ve verilerin doğru şekilde tanımlandığından emin olun.")