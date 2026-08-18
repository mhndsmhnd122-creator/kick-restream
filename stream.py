import subprocess
import time
import sys

RESTREAM_KEY = "re_11725544_event1f24e3174647428d86fc1329252bbf36"
KICK_CHANNEL = "https://kick.com/Peerless"
RTMP_DEST = f"rtmp://live.restream.io/live/{RESTREAM_KEY}"

MAX_RUN_TIME = 19800 

def run_stream():
    start_time = time.time()
    while True:
        if time.time() - start_time > MAX_RUN_TIME:
            sys.exit(0)
            
        print("جاري محاولة جلب رابط البث من قناة Peerless...")
        
        # استخراج رابط البث المباشر لتجاوز قيود الحماية
        url_command = [
            "streamlink", "--stream-url",
            "--http-header", "User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            KICK_CHANNEL, "720p,720p60,best"
        ]
        
        try:
            result = subprocess.run(url_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=20)
            stream_url = result.stdout.strip()
            
            if not stream_url or "error" in stream_url.lower():
                print("القناة غير متصلة (Offline) أو واجهنا حماية، إعادة المحاولة بعد 10 ثوانٍ...")
                time.sleep(10)
                continue
                
            print("تم استخراج الرابط بنجاح، جاري بدء البث إلى Restream...")
            
            # تشغيل FFmpeg مع الرابط المستخرج وتطبيق الـ GIF والصوت 320k
            ffmpeg_command = [
                "ffmpeg", "-y",
                "-i", stream_url,
                "-ignore_loop", "0", "-i", "logo.gif",
                "-filter_complex", "[1:v]scale=250:-1[img];[0:v][img]overlay=(main_w-overlay_w)/2:main_h-overlay_h-80",
                "-c:v", "libx264", "-preset", "veryfast",
                "-c:a", "aac", "-b:a", "320k",
                "-f", "flv", RTMP_DEST
            ]
            
            subprocess.run(ffmpeg_command)
            
        except Exception as e:
            print(f"حدث خطأ أثناء التنفيذ: {e}")
            
        print("إعادة المحاولة خلال 5 ثوانٍ...")
        time.sleep(5)

if __name__ == "__main__":
    run_stream()
