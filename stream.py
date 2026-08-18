import subprocess
import time
import sys

# تم تحديث المفتاح الجديد
RESTREAM_KEY = "re_11725544_event1f24e3174647428d86fc1329252bbf36"
KICK_CHANNEL = "https://kick.com/Peerless"
RTMP_DEST = f"rtmp://live.restream.io/live/{RESTREAM_KEY}"

MAX_RUN_TIME = 19800 

def run_stream():
    start_time = time.time()
    while True:
        if time.time() - start_time > MAX_RUN_TIME:
            sys.exit(0)
            
        print("جاري تشغيل البث من قناة Peerless مع ضبط الإعدادات...")
        
        command = [
            "streamlink", "--stdout",
            "--http-header", "User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            KICK_CHANNEL, "720p,720p60,best"
        ]
        
        p1 = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # الإعدادات المطلوبة: GIF أسفل المنتصف، صوت 320k
        ffmpeg_command = [
            "ffmpeg", "-y",
            "-i", "pipe:0",
            "-ignore_loop", "0", "-i", "logo.gif",
            "-filter_complex", "[1:v]scale=250:-1[img];[0:v][img]overlay=(main_w-overlay_w)/2:main_h-overlay_h-80",
            "-c:v", "libx264", "-preset", "veryfast",
            "-c:a", "aac", "-b:a", "320k",
            "-f", "flv", RTMP_DEST
        ]
        
        p2 = subprocess.Popen(ffmpeg_command, stdin=p1.stdout)
        p1.stdout.close()
        p2.wait()
        
        time.sleep(5)

if __name__ == "__main__":
    run_stream()
