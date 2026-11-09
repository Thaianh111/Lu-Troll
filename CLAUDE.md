# Lu Troll — ghi chú cho Claude

Đây là game **Lu Troll** của Võ Thái Anh (studio **VTA Games**). Đọc file này trước khi làm gì trong repo.

## Game là gì
- Game platformer troll kiểu Syobon Action ("con mèo trắng"): mỗi màn toàn bẫy bất ngờ.
- Nhân vật chính: **Lu**, chú chó vàng, vòng cổ đỏ có chuông (chó là biểu tượng của tác giả).
- Hướng thiết kế màn: màn 1 chỉ để khởi động, màn 2 có 10 bẫy, mỗi màn sau troll hơn màn trước
  (hiện có 5 màn: 1 Khởi động · 2 Đập máy · 3 Đổi luật · 4 Hết tin nổi · 5 Sấm sét)
- Màn 5: Lu nhặt phép **sấm sét** (biến `zapHave`, nút ⚡ `#bd`, phím X/Shift/K): lướt ngang 9 khung, trên không lướt 1 lần, xuyên `egate`, diệt quái, chớp sáng vùng tối. Câu đố: hố rộng (nhảy + lướt ở đỉnh), cổng giả `fgate`, cột thu lôi `rod` mở cửa `door`, đẩy cục phân `dball` làm bậc lên gờ, mây giông `storm` (đứng yên bị sét), cục phân lăn `dungroll`.
  (mục tiêu: người chơi tức muốn đập điện thoại nhưng vẫn muốn chơi lại).
- Quái là **bọ chét chó** (vẽ bằng code trong `drawEnemy`): loại thường, loại nhảy (`hop`), loại gai (`spiky`), loại tách 3 (`split`), Vua bọ chét (`king`, đạp 2 lần). Màn 5 có thêm **bọ hung lăn phân** (`beetle`): chết thì cục phân nằm lại thành khối đẩy được.
- Tạm thời KHÔNG đưa nội dung điện lạnh/HVAC vào game, chỉ tập trung bẫy bất ngờ.

## Kỹ thuật
- Toàn bộ game nằm trong **một file `index.html`** (HTML5 canvas + JS, không build, không thư viện ngoài).
- Nhân vật Lu: hình gốc `art/lu-goc.png` (vẽ bằng SpriteCook). Hoạt ảnh làm bằng Sorceress AutoSprite V3 từ hình gốc (đứng yên, ngó nghiêng, chạy, nhảy, chết, gảy đầu, nhấc chân tè), đã xoá nền và thu nhỏ thành 1 tấm `art/lu-anim.png`, nhúng trong `index.html` (biến `LUA`, hàm `drawDog`). Đứng yên lâu: gảy đầu → ngó nghiêng → tè (lịch trong `IDLE`). Nước tè vẽ bằng code (`drawPee`).
- Âm thanh tạo bằng WebAudio; hiệu ứng sprite từ pixelfx (MIT) đã nhúng sẵn trong file.
- Chơi chính trên điện thoại (xoay ngang), có nút cảm ứng ◀ ▶ ⤒; máy tính dùng phím mũi tên / Space.
- Host bằng GitHub Pages từ nhánh `main`, thư mục gốc.

## Quy ước
- Giao tiếp, chữ trong game và tài liệu bằng **tiếng Việt**.
- Credit/bản quyền ghi **"Võ Thái Anh"** (không dùng biệt danh). Logo studio VTA Games là chó mực đen.
- Khi thêm hiệu ứng pixel art / sprite: dùng pixelfx (https://github.com/patch-gg/pixelfx).

## Lịch sử
- Bản thử đầu tiên làm trong repo `Thaianh111/game-moi` (thư mục `prototypes/lu-troll/`), ngày 2026-11-05.
- Tách ra repo riêng `Thaianh111/Lu-Troll` ngày 2026-11-09.
