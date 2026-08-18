import subprocess
import time
import sys

RESTREAM_KEY = "re_11725544_event1cd98b642dcb49be89dbbda911e43626"
KICK_CHANNEL = "https://kick.com/seagull"
RTMP_DEST = f"rtmp://live.restream.io/live/{RESTREAM_KEY}"

MAX_RUN_TIME = 19800 

def run_stream():
    start_time = time.time()
    while True:
        if time.time() - start_time > MAX_RUN_TIME:
            sys.exit(0)
            
        command = ["streamlink", "--stdout", "--http-header", "User-Agent=Mozilla/5.0", KICK_CHANNEL, "720p,720p60,best"]
        p1 = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # إضافة فلتر النص "Peerless" فوق الـ GIF
        # drawtext يضع النص باللون الأبيض وحجم 30
        ffmpeg_command = [
            "ffmpeg", "-y",
            "-i", "pipe:0",
            "-ignore_loop", "0", "-i", "logo.gif",
            "-filter_complex", 
            "[1:v]scale=250:-1[img];"
            "[0:v][img]overlay=(main_w-overlay_w)/2:main_h-overlay_h-120[bg];"
            "[bg]drawtext=text='Peerless':x=(main_w-text_w)/2:y=main_h-80:fontsize=30:fontcolor=white:shadowcolor=black:shadowx=2:shadowy=2",
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
