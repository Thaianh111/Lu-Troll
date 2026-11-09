# Chỉnh dự án Android do Capacitor tạo: tên app, xoay ngang, toàn màn hình, icon con Lu.
import sys, os, re
from PIL import Image
A = sys.argv[1]                      # thư mục app/android
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
main = os.path.join(A, 'app/src/main')

# 1) Xoay ngang + giữ màn hình
mf = os.path.join(main, 'AndroidManifest.xml')
s = open(mf, encoding='utf-8').read()
if 'screenOrientation' not in s:
    s = s.replace('android:name=".MainActivity"', 'android:name=".MainActivity"\n            android:screenOrientation="sensorLandscape"', 1)
open(mf, 'w', encoding='utf-8').write(s)

# 2) Tên app
sp = os.path.join(main, 'res/values/strings.xml')
s = open(sp, encoding='utf-8').read()
s = re.sub(r'(<string name="app_name">)[^<]*(</string>)', r'\1Lu Troll\2', s)
s = re.sub(r'(<string name="title_activity_main">)[^<]*(</string>)', r'\1Lu Troll\2', s)
open(sp, 'w', encoding='utf-8').write(s)

# 3) Toàn màn hình (ẩn thanh trạng thái + thanh điều hướng)
pkg_dir = os.path.join(main, 'java/vn/vtagames/lutroll')
os.makedirs(pkg_dir, exist_ok=True)
open(os.path.join(pkg_dir, 'MainActivity.java'), 'w', encoding='utf-8').write('''package vn.vtagames.lutroll;

import android.view.View;
import com.getcapacitor.BridgeActivity;

public class MainActivity extends BridgeActivity {
    @Override
    public void onWindowFocusChanged(boolean hasFocus) {
        super.onWindowFocusChanged(hasFocus);
        if (hasFocus) {
            getWindow().getDecorView().setSystemUiVisibility(
                View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY | View.SYSTEM_UI_FLAG_FULLSCREEN
                | View.SYSTEM_UI_FLAG_HIDE_NAVIGATION | View.SYSTEM_UI_FLAG_LAYOUT_STABLE
                | View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION | View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN);
        }
    }
}
''')

# 4) Icon: con Lu trên nền vàng nhạt
lu = Image.open(os.path.join(ROOT, 'art/lu-goc.png')).convert('RGBA')
lu = lu.crop(lu.getbbox())
BG = (255, 233, 168, 255)
def icon(size, safe, round_=False, bg=True):
    im = Image.new('RGBA', (size, size), BG if bg else (0, 0, 0, 0))
    s2 = int(size * safe); w, h = lu.size; k = s2 / max(w, h)
    l = lu.resize((max(1, int(w * k)), max(1, int(h * k))), Image.NEAREST if k >= 1 else Image.LANCZOS)
    im.alpha_composite(l, ((size - l.width) // 2, (size - l.height) // 2))
    if round_:
        m = Image.new('L', (size, size), 0)
        from PIL import ImageDraw
        ImageDraw.Draw(m).ellipse((0, 0, size - 1, size - 1), fill=255)
        im.putalpha(m)
    return im
for d, n in {'mdpi': 48, 'hdpi': 72, 'xhdpi': 96, 'xxhdpi': 144, 'xxxhdpi': 192}.items():
    p = os.path.join(main, f'res/mipmap-{d}')
    os.makedirs(p, exist_ok=True)
    icon(n, 0.82).save(os.path.join(p, 'ic_launcher.png'))
    icon(n, 0.78, round_=True).save(os.path.join(p, 'ic_launcher_round.png'))
    icon(int(n * 108 / 48), 0.55, bg=False).save(os.path.join(p, 'ic_launcher_foreground.png'))
bgx = os.path.join(main, 'res/values/ic_launcher_background.xml')
open(bgx, 'w', encoding='utf-8').write('<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <color name="ic_launcher_background">#FFE9A8</color>\n</resources>\n')
print('patched', A)
