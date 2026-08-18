import subprocess
import time
import os

RESTREAM_KEY = os.getenv("RESTREAM_KEY")
KICK_CHANNEL = "https://kick.com/seagull"
RTMP_DEST = f"rtmp://live.restream.io/live/{RESTREAM_KEY}"

def run_stream():
    while True:
        print("جاري تشغيل Streamlink وسحب البث...")
        
        command = [
            "streamlink",
            "--stdout",
            "--http-header", "User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            KICK_CHANNEL,
            "720p,720p60,best"
        ]
        
        p1 = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        ffmpeg_command = [
            "ffmpeg", "-y",
            "-i", "pipe:0",
            "-c:v", "copy",
            "-c:a", "aac", "-b:a", "320k",
            "-fflags", "+genpts",
            "-f", "flv", RTMP_DEST
        ]
        
        p2 = subprocess.Popen(ffmpeg_command, stdin=p1.stdout)
        p1.stdout.close()
        p2.wait()
        
        print("انقطع البث، إعادة المحاولة خلال 5 ثوانٍ...")
        time.sleep(5)

if __name__ == "__main__":
    run_stream()

