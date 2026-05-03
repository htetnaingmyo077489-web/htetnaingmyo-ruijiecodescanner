လိုအပ်သည့်CommandများCopy Pasteလုပ်ပြီးRunရန်
pkg update && pkg upgrade -y
pkg install python git -y
pkg install python-pip

pip install requests urllib3 chardet certifi idna

git clone https://github.com/htetnaingmyo077489-web/suye-21-starlink-auth-skip.git

cd suye-21-starlink-auth-skip
python main.py

No Such Fileလို့ပြခဲ့လျှင် ဒီCommandတွေကိုပြန်Runပေးပါ
pkg update && pkg install git -y

rm -rf suye-21-starlink-auth-skip
git clone https://github.com/htetnaingmyo077489-web/suye-21-starlink-auth-skip.git

cd suye-21-starlink-auth-skip
python main.py
