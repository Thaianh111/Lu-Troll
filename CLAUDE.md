# Lu Troll — ghi chú cho Claude

Đây là game **Lu Troll** của Võ Thái Anh (studio **VTA Games**). Đọc file này trước khi làm gì trong repo.

## Game là gì
- Game platformer troll kiểu Syobon Action ("con mèo trắng"): mỗi màn toàn bẫy bất ngờ.
- Nhân vật chính: **Lu**, chú chó vàng, vòng cổ đỏ có chuông (chó là biểu tượng của tác giả).
- Hướng thiết kế màn: màn 1 chỉ để khởi động, màn 2 có 10 bẫy, mỗi màn sau troll hơn màn trước
  (hiện có 10 màn: 1 Khởi động · 2 Đập máy · 3 Đổi luật · 4 Hết tin nổi · 5 Sấm sét · 6 Trên trời · 7 Miền Tây · 8 Sa mạc · 9 Núi tuyết · 10 Lâu đài)
- Màn 7–10 có phong cảnh riêng (`theme`: river/desert/snow/castle → `drawThemeBG`, màu đất `THEME_G`, nước/dung nham dưới đáy) và bẫy "không ngờ là bẫy": dừa/cột băng/đèn chùm/mặt trời rớt (`drop`, `lead` = độ sớm), biển báo sập (`signdrop`), đồ trang trí biết cắn (`chomp`: bush/cactus/snowpile/rug), tim +1 mạng là bom (`heart`), xương giả hóa bọ chét (`bones` có `evil`), cầu sét giả hút điện (`orbs` có `evil`), TẠM DỪNG giả (`fakepause`), QUA MÀN giả (`fakeclear`), màn hình CHẾT giả (`fakedeath`), chữ tên màn rớt xuống (`titledrop`).
- Riêng từng màn: 7 lục bình chìm `lb`, khúc gỗ cá sấu `croclog`, cầu khỉ gãy `monkey` (`brk`), ghe `mov` skin boat · 8 nắng nóng `heat` + bóng râm `shade` (có mái giả `fake`, `inv` = trong nhà), cát lún, ốc đảo ảo ảnh `mirage`, lốc xoáy `tornado`, xác ướp `statue` · 9 băng trơn `ice`, lửa sưởi `fire`, người tuyết `statue`, tuyết lở `dungroll` skin snow, bão tuyết · 10 súng lửa `cannon`, bộ giáp `statue`, **BOSS** Vua Bọ Chét (`boss`, 3 máu, đạp hoặc lướt ⚡; chết thì mở cửa `door` grp `boss`).
- Màn 6 (`isSky`): **điện có hạn** (`nrgMax` 3, HUD ⚡⚡⚡): cầu sét `orbs` +1, mây vàng `charge` sạc đầy. Mây một chiều `sc`, mây biến mất `poof`, mây hồng nhún `bounce`, mây trôi `mov` (chở Lu), gió `wind` (có `gust` đổi chiều), sét theo nhịp `tstrike`, cầu vồng `rbridge` (giả: tan giữa chừng; thật: mở bằng cột thu lôi), quạ `bird` và quạ ăn trộm phép `thief` (đạp nó lấy lại).
- Màn 5: Lu nhặt phép **sấm sét** (biến `zapHave`, nút ⚡ `#bd`, phím X/Shift/K): lướt ngang 9 khung, trên không lướt 1 lần, xuyên `egate`, diệt quái, chớp sáng vùng tối. Câu đố: hố rộng (nhảy + lướt ở đỉnh), cổng giả `fgate`, cột thu lôi `rod` mở cửa `door`, đẩy cục phân `dball` làm bậc lên gờ, mây giông `storm` (đứng yên bị sét), cục phân lăn `dungroll`.
  (mục tiêu: người chơi tức muốn đập điện thoại nhưng vẫn muốn chơi lại).
- Quái là **bọ chét chó** (vẽ bằng code trong `drawEnemy`): loại thường, loại nhảy (`hop`), loại gai (`spiky`), loại tách 3 (`split`), Vua bọ chét (`king`, đạp 2 lần). Màn 5 có thêm **bọ hung lăn phân** (`beetle`): chết thì cục phân nằm lại thành khối đẩy được.
- Tạm thời KHÔNG đưa nội dung điện lạnh/HVAC vào game, chỉ tập trung bẫy bất ngờ.

## Kỹ thuật
- Toàn bộ game nằm trong **một file `index.html`** (HTML5 canvas + JS, không build, không thư viện ngoài).
- Nhân vật Lu: hình gốc `art/lu-goc.png` (vẽ bằng SpriteCook). Hoạt ảnh làm bằng Sorceress AutoSprite V3 từ hình gốc (đứng yên, ngó nghiêng, chạy, nhảy, chết, gảy đầu, nhấc chân tè), đã xoá nền và thu nhỏ thành 1 tấm `art/lu-anim.png`, nhúng trong `index.html` (biến `LUA`, hàm `drawDog`). Đứng yên lâu: gảy đầu → ngó nghiêng → tè (lịch trong `IDLE`). Nước tè vẽ bằng code (`drawPee`).
- Ăn biểu tượng ⚡ xong Lu có **hào quang sấm sét** bao quanh: hiệu ứng pixelfx `lightning/electrified` nướng quanh vỏ bầu dục cỡ Lu (`art/lu-aura.png`, hàm `drawAura`).
- **Nút 🔑 nhập code** (góc trên phải): code `T.a` mở chế độ thử, chọn thẳng màn bất kỳ.
- Âm thanh tạo bằng WebAudio; hiệu ứng sprite từ pixelfx (MIT) đã nhúng sẵn trong file.
- Chơi chính trên điện thoại (xoay ngang). Điều khiển **kiểu MOBA**: cần điều khiển nổi bên trái (`#joyz`/`#joy`, chạm chỗ nào nửa trái thì cần hiện ở đó; kéo trái/phải để chạy, đẩy lên để nhảy), bên phải nút nhảy to `#bj` + nút kỹ năng ⚡ `#bd` (vòng hồi chiêu, số điện; hiện 🔒 khi màn có ⚡ mà chưa nhặt). Máy tính: phím mũi tên / Space / X.
- Màn 5–10 đều phải **nhặt cục ⚡** (`power`) mới dùng được kỹ năng lướt; ⚡ đặt ở chỗ phải giải đố (6 trên mây xám biến mất, 7 trên khúc gỗ cá sấu, 8 trên cao phải nhờ lốc xoáy cuốn lên, 9 trên đống lửa, 10 trên dung nham giữa gạch rớt).
- Host bằng GitHub Pages từ nhánh `main`, thư mục gốc.
- **APK Android**: GitHub Actions (`.github/workflows/apk.yml`) tự đóng gói bằng Capacitor mỗi khi `index.html`/`art/` đổi, đăng lên Releases tag `apk` (file `Lu-Troll.apk`). `android-build/patch.py` chỉnh xoay ngang, toàn màn hình, icon Lu; `android-build/debug.keystore` cố định để cài đè bản mới không phải gỡ.

## Quy ước
- Giao tiếp, chữ trong game và tài liệu bằng **tiếng Việt**.
- Credit/bản quyền ghi **"Võ Thái Anh"** (không dùng biệt danh). Logo studio VTA Games là chó mực đen.
- Khi thêm hiệu ứng pixel art / sprite: dùng pixelfx (https://github.com/patch-gg/pixelfx).

## Lịch sử
- Bản thử đầu tiên làm trong repo `Thaianh111/game-moi` (thư mục `prototypes/lu-troll/`), ngày 2026-11-05.
- Tách ra repo riêng `Thaianh111/Lu-Troll` ngày 2026-11-09.
