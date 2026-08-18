import subprocess
import time
import sys

RESTREAM_KEY = "re_11725544_event1cd98b642dcb49be89dbbda911e43626"
KICK_CHANNEL = "https://kick.com/seagull"
RTMP_DEST = f"rtmp://live.restream.io/live/{RESTREAM_KEY}"

# تحديد وقت التشغيل بـ 5 ساعات و 30 دقيقة بالثانية (5.5 * 3600 = 19800 ثانية)
MAX_RUN_TIME = 19800 

def run_stream():
    start_time = time.time()
    
    while True:
        # التحقق مما إذا مرّت 5 ساعات و 30 دقيقة لإعادة التشغيل النظيف
        if time.time() - start_time > MAX_RUN_TIME:
            print("[*] اقتربنا من حدود الـ 6 ساعات، جاري إعادة تشغيل السكربت لتفادي الانقطاع...")
            sys.exit(0) # الخروج بنجاح ليقوم جيثوب أو حلقة العمل بإعادة تدويره
            
        print("جاري تشغيل البث بجودة صوت 320k وإضافة الـ GIF...")

        command = [
            "streamlink", "--stdout",
            "--http-header", "User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            KICK_CHANNEL, "720p,720p60,best"
        ]
        
        p1 = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # معادلة التموضع (أسفل المنتصف):
        # (main_w-overlay_w)/2 منتصف الشاشة أفقياً
        # main_h-overlay_h-80 في الأسفل مع ارتفاع بسيط
        # mod(t,300)<60 تظهر لمدة دقيقة كل 5 دقائق
        ffmpeg_command = [
            "ffmpeg", "-y",
            "-i", "pipe:0",
            "-ignore_loop", "0", "-i", "logo.gif",
            "-filter_complex", "[1:v]scale=250:-1[img];[0:v][img]overlay=(main_w-overlay_w)/2:main_h-overlay_h-80:enable='mod(t,300)<60'",
            "-c:v", "libx264", "-preset", "veryfast",
            "-c:a", "aac", "-b:a", "320k",
            "-f", "flv", RTMP_DEST
        ]
        
        p2 = subprocess.Popen(ffmpeg_command, stdin=p1.stdout)
        p1.stdout.close()
        
        # مراقبة البث مع فحص الوقت بانتظام
        while p2.poll() is None:
            if time.time() - start_time > MAX_RUN_TIME:
                print("[*] وقت إعادة التشغيل الذاتي وصل...")
                p1.terminate()
                p2.terminate()
                sys.exit(0)
            time.sleep(10)
            
        print("انقطع البث، إعادة المحاولة خلال 5 ثوانٍ...")
        time.sleep(5)

if __name__ == "__main__":
    run_stream()
