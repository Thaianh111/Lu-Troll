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
- **Màn chọn màn** `#lvsel` (hàm `openMap`, nút 🗺️ `#map` trong game): 10 thẻ có icon riêng (`LVICON`), qua màn N mới mở màn N+1 (`clearLevel`, lưu localStorage `lutroll_prog` = {u: màn mở cao nhất, c: các màn đã qua}). Bấm CHƠI THÔI / thắng game → về bản đồ.
- **Cảnh chết chậm**: khựng ~0,6 giây + zoom rung vô mặt Lu, rồi bay lên và rớt từ từ (trọng lực 0.2), bảng "Chết rồi" hiện sau ~1,2 giây; sau ~1,7 giây bấm nhảy để chơi lại liền.
- **Nút 🔑 nhập code** (góc trên phải): code `T.a` mở chế độ thử, chọn thẳng màn bất kỳ (bản đồ cũng mở hết).
- **Màn giới thiệu studio** `#vtaSplash` (logo chó mực VTA Games, chép y từ game Nông Trại) rồi **banner tiêu đề** `#ttl` (Lu nhún nhảy, chữ LU TROLL lắc lư, nút ▶ CHƠI THÔI! bỏ chạy 2 lần mới cho bấm). Ảnh banner: `art/banner.png`, `art/vta-splash.png`.
- **Nhạc nền "Lu Lu Gâu Gâu"** sáng tác bằng WebAudio (`BARS`, `SONG`, `bgmStep`): kèn kazoo, tuba um-pa, tiếng chó sủa gâu gâu, còi trượt, kèn xe đạp, khúc lén lút gõ mõ; bản nghe thử `art/nhac/Lu-Lu-Gau-Gau.mp3`. Màn sau nhanh dần; bị troll thì cả bài tụt giọng.
- Âm thanh tạo bằng WebAudio; hiệu ứng sprite từ pixelfx (MIT) đã nhúng sẵn trong file.
- Chơi chính trên điện thoại (xoay ngang). Điều khiển **kiểu MOBA**: cần điều khiển nổi bên trái (`#joyz`/`#joy`, chạm chỗ nào nửa trái thì cần hiện ở đó; kéo trái/phải để chạy, đẩy lên để nhảy), bên phải nút nhảy to `#bj` + nút kỹ năng ⚡ `#bd` (vòng hồi chiêu, số điện; hiện 🔒 khi màn có ⚡ mà chưa nhặt). Máy tính: phím mũi tên / Space / X.
- Màn 5–10 đều phải **nhặt cục ⚡** (`power`) mới dùng được kỹ năng lướt; ⚡ đặt ở chỗ phải giải đố (6 trên mây xám biến mất, 7 trên khúc gỗ cá sấu, 8 trên cao phải nhờ lốc xoáy cuốn lên, 9 trên đống lửa, 10 trên dung nham giữa gạch rớt).
- **Điểm lưu (đợt 1)**: mỗi màn khai báo `cps:[x,…]` (1–5: 2–3 cờ, 6–10: 3 cờ; cờ lưu giả `fakecp` màn 3/5/9 nằm ngay trước một cờ thật). Chạm cờ khi đang đứng trên đất → `cpX`, `cpZap` (đã có ⚡). Hồi sinh: `build()` gọi `cpReplay(cpX)` — cột thu lôi phía sau coi như đã kích (cửa/cầu vồng mở), `doorclose` phía sau đóng lại, bẫy kích theo mốc (`trig`, chữ rớt, màn hình giả) phía sau bỏ, quái phía sau bỏ (boss phía sau = đã hạ, mở cửa `boss`), quái gần chỗ hồi sinh đứng im 90 khung (`e.hold`). Cờ thật đã lưu vẽ màu xanh lá. `lvReset()` khi vào màn mới.
- **Coyote + bộ đệm nhảy**: hằng `COYOTE`/`JBUF` (6 khung), biến `P.coy`/`P.jb` trong `update()`. Coyote chỉ dùng khi `P.vy*gd>=0` (không chồng lên lò xo/mây hồng/lốc xoáy); lộn trọng lực thì xóa cả hai.
- **Câu chọc quê**: `MSG` (câu gốc) + `MSGX` (câu thêm) xoay vòng bằng `pickMsg`; `deathSpot` đếm chết cùng kiểu trong bán kính 260px (`DSPOT`), từ lần 5 hiện gợi ý `HINT[...]` (dính cầu sét giả/cổng giả gần đây thì dùng `L.trollK`). Đá lăn màn 8 đổi nguyên nhân thành `boulder`.
- **Tạm dừng thật**: nút ⏸ `#pause` (hàng nút góc trên phải, khác hẳn chữ to "⏸ TẠM DỪNG" của bẫy `fakepause` — cố ý giữ troll), phím Esc/P, tự dừng khi ẩn app; `setPause(on,'menu'|'tut')`, `paused` bỏ qua `update()` và suspend AudioContext. Bảng `#pbox`: Tiếp tục / Về bản đồ / Âm thanh + rung. **Rung** `buzz()` khi chết (và chết giả), tắt cùng nút 🔊 (`setMuted`). **Hướng dẫn lần đầu** `#tut` khi vào màn 1, lưu khóa riêng `lutroll_tut` (không đụng `lutroll_prog`).
- **Troll lướt ngược**: chỉ xảy ra khi `zapTrollSafe()` đúng (đứng trên đất thật, ±210px đều có đất, không quái gần, không gió/mây giông/sét/súng lửa, không vùng tối); không đủ thì hoãn.
- Host bằng GitHub Pages từ nhánh `main`, thư mục gốc.
- **APK Android**: GitHub Actions (`.github/workflows/apk.yml`) tự đóng gói bằng Capacitor mỗi khi `index.html`/`art/` đổi, đăng lên Releases tag `apk` (file `Lu-Troll.apk`). `android-build/patch.py` chỉnh xoay ngang, toàn màn hình, icon Lu; `android-build/debug.keystore` cố định để cài đè bản mới không phải gỡ.

## Quy ước
- Giao tiếp, chữ trong game và tài liệu bằng **tiếng Việt**.
- Credit/bản quyền ghi **"Võ Thái Anh"** (không dùng biệt danh). Logo studio VTA Games là chó mực đen.
- Khi thêm hiệu ứng pixel art / sprite: dùng pixelfx (https://github.com/patch-gg/pixelfx).

## Lịch sử
- Bản thử đầu tiên làm trong repo `Thaianh111/game-moi` (thư mục `prototypes/lu-troll/`), ngày 2026-11-05.
- Tách ra repo riêng `Thaianh111/Lu-Troll` ngày 2026-11-09.
