# Lu Troll — Tài liệu thiết kế game (GDD)

Một game của **VTA Games** · © Võ Thái Anh
Cập nhật: 2026-11-10 · Người viết: Minh (Game Designer)
Phạm vi tài liệu: mô tả đúng game **hiện tại** trong `index.html` (10 màn), đánh giá và đề xuất cải tiến.

---

## 1. Tổng quan

| Mục | Nội dung |
| --- | --- |
| Thể loại | Platformer cuộn ngang 2D kiểu "troll" (bẫy bất ngờ, chết là học) |
| Nền tảng | Trình duyệt (GitHub Pages) + APK Android (Capacitor). Chơi chính trên điện thoại xoay ngang; máy tính dùng bàn phím |
| Người chơi mục tiêu | Người Việt chơi điện thoại, thích game hài, chơi ngắn, thích quay lại khoe "tui chết bao nhiêu lần" |
| Nhân vật | **Lu** – chú chó vàng, vòng cổ đỏ có chuông |
| Phe địch | Bọ chét chó (nhiều loại), bọ hung lăn phân, quạ, đồ vật đội lốt (bụi cỏ, xương rồng, người tuyết, bộ giáp, thảm…), trùm **Vua Bọ Chét** |
| Core fantasy | "Tui biết game đang lừa tui, và lần sau tui sẽ không bị lừa nữa." Người chơi **tức nhưng cười**, và muốn chơi lại ngay |
| Giọng điệu | Chọc quê thân thiện, tiếng Việt đời thường, đậm chất miền Tây/Nam Bộ ("dữ thần", "chi trời", "lẹ") |

### Vòng lặp chơi
- **30 giây:** chạy, nhảy, thấy thứ gì đó "an toàn" → bị troll → cảnh chết chậm + câu chọc quê → bấm nhảy chơi lại liền từ đầu màn/điểm lưu.
- **5 phút:** học thuộc từng bẫy của một đoạn, qua điểm lưu 🚩, bị một bẫy "kiểu mới" ở nửa sau, cuối cùng đuổi kịp cờ đích (cờ biết bỏ chạy).
- **Cả phiên:** mở khóa lần lượt 10 màn trên bản đồ, mỗi màn thêm một luật/chủ đề mới (đổi luật → phép sấm sét → điện có hạn → phong cảnh riêng → boss). Kết thúc: bảng "Phá đảo" ghi tổng số lần chết và xương nhặt được.

---

## 2. Cơ chế

### 2.1. Di chuyển (số liệu thực trong code)
| Thông số | Giá trị | Ghi chú |
| --- | --- | --- |
| Khung hình logic | 800 × 450 | |
| Trọng lực `GR` | 0.6 /khung | rơi tối đa 14 |
| Tốc độ chạy `SPD` | 4 px/khung | giày tốc độ ×2.1 |
| Lực nhảy `JMP` | 12.2 | cao tối đa ≈ 124 px; nhả nút sớm → nhảy thấp (cắt vy về −4) |
| Lò xo / mây hồng | vy −20 / −17 | |
| Băng, bùn | trượt có quán tính, tối đa 6.5 | |
| Không có | coyote time, bộ đệm nhảy (jump buffer) | xem mục đánh giá |

### 2.2. Phép sấm sét ⚡ (màn 5–10)
- Phải **nhặt cục ⚡** (`power`) trong màn mới mở nút kỹ năng (trước đó nút hiện 🔒). Mất màn là phải nhặt lại; chết trong màn thì giữ phép.
- Lướt ngang 9 khung với tốc độ 20 (≈180 px), hồi chiêu 30 khung; trên không chỉ lướt được 1 lần.
- Lướt xuyên cổng điện `egate`, diệt quái, chớp sáng vùng tối, kích cột thu lôi `rod` (mở cửa/cầu vồng).
- Troll cố định: **lần đầu tiên** dùng phép trong phiên chơi thì lướt ngược.
- Màn 6–10 có **điện có hạn** `nrgMax` (3, màn 10 là 4): cầu sét `orbs` +1, mây vàng `charge` sạc đầy; cầu sét giả (`evil`) hút điện.

### 2.3. Kẻ địch
| Loại | Hành vi | Cách diệt |
| --- | --- | --- |
| Bọ chét thường | đi qua lại | đạp |
| Bọ nhảy `hop` | nhảy xa | đạp |
| Bọ gai `spiky` | đạp là chết | lướt ⚡ / né |
| Bọ tách `split` | đạp ra 3 con nhỏ | đạp từng con |
| Vua bọ chét `king` | đạp 2 lần | đạp |
| Bọ hung `beetle` | lăn phân; chết để lại cục phân đẩy được (làm bậc) | đạp/lướt |
| Quạ `bird` / quạ trộm `thief` | bay nhấp nhô; quạ trộm cướp phép ⚡ | đạp để lấy lại phép |
| Tượng `statue` (xác ướp, người tuyết, bộ giáp) | đứng yên giả trang trí, đến gần thì rượt | né / lướt |
| **BOSS Vua Bọ Chét** (màn 10) | 3 máu, có thời gian bất tử sau mỗi đòn | đạp hoặc lướt ⚡; chết thì mở cửa `boss` |

### 2.4. Bẫy (thư viện chung)
- **Khối & đất:** khối ? ra quái/nấm đảo nút/giày tốc độ/gương/xương; khối tàng hình; đất giả; đất giả kích hoạt theo nhóm; cầu tàng hình; đất lún khi đứng yên; gạch rớt; bùn, băng trơn.
- **Từ trên rơi xuống:** đá rớt, khối đè `crusher`, thanh gai, dừa/cột băng/đèn chùm/mặt trời `drop` (`lead` = rớt sớm bao nhiêu), biển báo sập `signdrop`, chữ tên màn rớt `titledrop`.
- **Bay tới:** tên lửa sau lưng / phía trước, cá lóc phóng lên, ong rượt, súng lửa.
- **Đổi luật:** nấm đảo trái-phải, cờ lưu giả đổi nút nhảy với nút phải, lật gương màn hình, lộn ngược trọng lực, vùng tối.
- **Troll giao diện (meta):** cờ đích bỏ chạy, đích giả `fakewin`, phá đảo giả `fakeend`, cờ lưu giả `fakecp`, TẠM DỪNG giả, QUA MÀN giả, màn hình CHẾT giả, nút ▶ CHƠI THÔI bỏ chạy 2 lần ở màn hình tiêu đề.
- **Đồ "vô hại" biết cắn:** mây cắn, bụi cỏ/xương rồng/đống tuyết/thảm `chomp`, tim +1 mạng là bom, xương giả hóa bọ chét, ốc đảo ảo ảnh.

### 2.5. Chết và chơi lại
- Không có hệ thống mạng: **chơi lại vô hạn**. Mỗi màn có **1 điểm lưu** (`cp`), qua là hiện "🚩 Đã lưu chỗ".
- Cảnh chết chậm: khựng ~0,6 giây, zoom rung vào mặt Lu → bay lên → rớt từ từ. Bảng "Gâu! Chết rồi 😵" + câu chọc quê theo nguyên nhân (≈ 80 câu trong `MSG`) + "Màn này chết N lần · tổng M". Sau ~1,7 giây bấm nhảy để chơi lại, tự hồi sinh sau ~3,8 giây.
- Nhạc tụt giọng khi bị troll.

### 2.6. Tiến độ, điểm số, code thử
- Bản đồ chọn màn `#lvsel`: 10 thẻ, qua màn N mở màn N+1; lưu `localStorage` `lutroll_prog = {u, c}`. Màn đã qua có dấu ✓.
- Điểm: 💀 tổng số lần chết, 🦴 số xương. Xương **chỉ để đếm**, chưa dùng vào việc gì.
- Phá đảo: bảng tổng kết "chết N lần · 🦴 M", chết ≤ 15 lần thì khen. Thông số này **không được lưu**.
- Nút 🔑: nhập code `T.a` để mở chế độ thử (chọn thẳng màn bất kỳ, bản đồ mở hết).

---

## 3. Điều khiển

| | Điện thoại (xoay ngang) | Máy tính |
| --- | --- | --- |
| Chạy | Cần điều khiển nổi nửa trái (chạm đâu hiện ở đó, kéo trái/phải) | ← → |
| Nhảy | Nút nhảy to bên phải `#bj`, hoặc đẩy cần lên | Space / ↑ |
| Lướt ⚡ | Nút ⚡ `#bd` (vòng hồi chiêu, số điện; 🔒 khi chưa nhặt) | X / Shift / K |
| Khác | 🗺️ bản đồ, 🔑 code, 🔊 tắt tiếng | |

---

## 4. Màn chơi

| # | Tên | Dài (px) | Chủ đề / luật mới | Bẫy & điểm nhấn chính |
| --- | --- | --- | --- | --- |
| 1 | Khởi động | 4000 | dạy chạy-nhảy, "đừng tin gì cả" | khối ? ra bọ chét, khối tàng hình, đất giả, đá rớt, mây cắn, gai mọc, cờ đích bỏ chạy |
| 2 | Đập máy | 4400 | 10 bẫy liên tiếp | bảng "an toàn" xạo, nấm đảo nút, khối đè giữa bãi xương, bọ gai, lò xo bắn lên thanh gai, cá lóc, gạch rớt, tên lửa sau lưng, đích giả, đích thật bỏ chạy |
| 3 | Đổi luật | 5400 | luật chơi bị thay | gương lật màn hình, trần lộn ngược trọng lực, bùn trơn, cờ lưu giả đổi nút, hố giả (đi bộ qua được, nhảy thì gai), vùng tối, ong rượt, bọ tách 3, phá đảo giả |
| 4 | Hết tin nổi | 5700 | tổng hợp + bọ chét đủ loại | cầu tàng hình + khối tàng hình ngay mép, giày tốc độ, đất lún khi "nghỉ chân", tên lửa phía trước, 3 khối đè, Vua bọ chét (tách), ong rượt trong bóng tối, đích giả |
| 5 | Sấm sét | 6400 | nhận phép ⚡ (không giới hạn điện) | cổng điện, mây giông (đứng yên bị sét), hố rộng nhảy+lướt, cổng giả bằng đá, cột thu lôi mở cửa, bọ hung → đẩy phân làm bậc, phân lăn, vùng tối cần lướt cho sáng, cờ lưu giả |
| 6 | Trên trời | 7000 | **điện có hạn 3** | mây một chiều/biến mất/nhún/trôi, gió ngược + gió giật, quạ trộm phép, sét theo nhịp, mây vàng sạc, cầu vồng giả (thật mở bằng cột thu lôi), bầy quạ, gương lật |
| 7 | Miền Tây | 6200 | phong cảnh sông nước | dừa rớt, lục bình chìm, khúc gỗ cá sấu (⚡ nằm trên nó), bụi cỏ cắn, biển "Chợ nổi Cái Răng" sập, cầu khỉ gãy, tim bom, TẠM DỪNG giả, ghe đưa đò, chữ tên màn rớt, cầu sét giả, QUA MÀN giả |
| 8 | Sa mạc | 6400 | **nắng nóng**: phải núp bóng râm | cát lún, xương rồng ôm, ốc đảo ảo ảnh, lốc xoáy cuốn lên lấy ⚡, bóng râm giả, kim tự tháp tối + xác ướp, đá lăn, cửa mở bằng cột thu lôi, **mặt trời rớt**, màn hình CHẾT giả |
| 9 | Núi tuyết | 6400 | băng trơn, bão tuyết | cột băng rớt (sớm/muộn xen kẽ), đất giả, lửa sưởi đốt đuôi (⚡ trên lửa), đống tuyết há miệng, tuyết lở, người tuyết rượt, gió giật, tim bom, cờ lưu giả, biển sập |
| 10 | Lâu đài | 7300 | **BOSS**, điện 4 | thảm biết cắn, đèn chùm rớt, súng lửa, gạch rớt trên dung nham lấy ⚡, 2 khối đè + tim bom, bộ giáp sống dậy, đá trôi, cửa cột thu lôi, phòng boss khóa cửa, Vua Bọ Chét 3 máu, "Thoát rồi!!!" → đích giả + chữ rớt + thảm cắn |

Thời gian chạy thẳng không chết: ~17 giây (màn 1) đến ~30 giây (màn 10). Thực tế mỗi màn mất 3–15 phút tùy số lần chết.

---

## 5. Cân bằng (hiện trạng)
- Đường cong độ khó đi lên đều 1→4, nhảy bậc ở 5 (thêm phép), 6 (điện có hạn + nền mây, rớt là chết), sau đó 7–10 giữ mức cao, thay chủ đề.
- Độ dài màn tăng 4000 → 7300 px nhưng **vẫn chỉ 1 điểm lưu/màn**, nên nửa sau màn 6–10 phải chạy lại rất xa.
- Bẫy "lead" (rớt sớm) xen kẽ sớm/muộn để người chơi không học một nhịp duy nhất (tốt).

## 6. Nghệ thuật & Âm thanh (định hướng hiện tại)
- **Hình:** Lu là sprite hoạt ảnh (đứng, ngó, chạy, nhảy, chết, gảy đầu, tè) từ hình gốc `art/lu-goc.png`; hào quang sấm sét khi có ⚡. Quái, bẫy, phong cảnh vẽ bằng code (khối màu, phong cách đồ chơi). Màn 7–10 có nền riêng (`drawThemeBG`) và đáy là nước/cát/vực/dung nham. Hiệu ứng bụi, khói, "!", tia lửa từ pixelfx. Chữ có emoji.
- **Màn mở đầu:** splash VTA Games (chó mực đen) → banner LU TROLL lắc lư → bản đồ.
- **Âm thanh:** toàn bộ WebAudio. Nhạc nền "Lu Lu Gâu Gâu" (kazoo, tuba um-pa, tiếng sủa, còi trượt, kèn xe đạp, khúc lén lút gõ mõ), nhanh dần theo màn, tụt giọng khi bị troll. Hiệu ứng: nhảy, đạp, xương, lò xo, lướt ⚡, giai điệu chọc quê, kèn "oa oa" khi chết, fanfare qua màn.

## 7. Phạm vi MVP
Đã đạt: 10 màn chơi được từ đầu đến cuối, có boss, bản đồ, lưu tiến độ, chạy web + APK. Các mục dưới đây là bản 1.1 trở đi.

---

## 8. Đánh giá

### Điểm mạnh
1. **Thư viện bẫy rất phong phú và có "vị" riêng**: không chỉ đất giả/khối rơi kiểu kinh điển mà còn troll giao diện (TẠM DỪNG giả, CHẾT giả, QUA MÀN giả, chữ tên màn rớt) – đây là chất "đúng thể loại" mạnh nhất.
2. **Bẫy "đồ vô hại" theo chủ đề** (dừa, biển Chợ nổi Cái Răng, mặt trời rớt, thảm "chùi chân") vừa troll vừa kể chuyện, rất bản địa, dễ nhớ, dễ khoe.
3. **Phản hồi khi chết xuất sắc**: cảnh chết chậm + ~80 câu chọc quê theo đúng nguyên nhân → người chơi cười thay vì cáu.
4. **Mỗi màn thêm một luật mới** (đổi luật, ⚡, điện có hạn, nắng nóng, băng, boss) → nhịp khám phá tốt, không lặp.
5. Chơi lại tức thì, không mất mạng, không màn hình chờ dài.

### Điểm yếu
1. **Chạy lại quá xa ở màn dài (lớn nhất).** Màn 6–10 dài 6200–7300 px, chỉ 1 điểm lưu (màn 10 ở 4540, sau phòng boss mới tới đích). Thể loại troll sống nhờ "chết–thử lại trong 3 giây"; phải chạy lại 30–60 giây qua các bẫy đã thuộc khiến cảm giác chuyển từ "tức cười" sang "chán", nhất là trên điện thoại. Cờ lưu giả (`fakecp`) ở màn 3, 5, 9 làm điều này nặng hơn.
2. **Một số bẫy không công bằng ở lần chơi đầu và cả lần sau.** Chuẩn "tức nhưng muốn chơi lại" là: lần 1 bị lừa, lần 2 **thấy được** cách né. Một vài bẫy hiện chưa có dấu hiệu nhận biết hoặc khó né ngay cả khi biết: cột băng/dừa `lead` sớm (rớt trước khi tới), tim bom (giống tim thật hoàn toàn), cầu sét giả (giống thật), bóng râm giả trong vùng nắng gắt, troll "lần đầu lướt ngược" xảy ra đúng lúc người chơi cần lướt qua hố/cổng. Thêm việc **không có coyote time / jump buffer** nên trên cảm ứng có cảm giác "tui bấm rồi mà!" – người chơi sẽ đổ lỗi cho điều khiển, không phải cho bẫy, và đó là kiểu tức muốn bỏ game.
3. **Ít lý do chơi lại sau khi phá đảo.** Xương không dùng vào việc gì, không lưu số lần chết/kỷ lục từng màn, không có thử thách thêm, không có gì để khoe ngoài trí nhớ. Thể loại này rất hợp với chia sẻ ("tui chết 87 lần ở màn 4") nhưng game chưa khai thác.
4. **Nhịp độ trong màn**: nửa đầu màn 1–4 dày bẫy, nhưng màn 7–10 có đoạn đất bằng dài không có gì (ví dụ 3000–3900 màn 9, 6040–7200 màn 10 chỉ còn 2 quái), lúc chạy lại càng thấy dài.
5. **Mobile**: không có nút tạm dừng thật (chỉ có TẠM DỪNG giả làm troll), không rung khi chết, hướng dẫn điều khiển cho người mới gần như không có ngoài biển báo. Nút ⚡ xuất hiện giữa màn có thể làm người chơi bấm nhầm.
6. **Độ dài nội dung**: ~1–2 giờ cho người chơi trung bình; không có chế độ thêm hay màn bí mật – thể loại thường có "màn ẩn", ống/cửa bí mật, đường tắt.
7. Câu chọc quê chỉ 1 câu/nguyên nhân → chết 10 lần cùng chỗ là đọc lại 10 lần cùng câu, hết buồn cười.

---

## 9. Đề xuất cải tiến (xếp theo ưu tiên)

| # | Cải tiến | Lý do | Ai làm | Độ lớn |
| --- | --- | --- | --- | --- |
| 1 | **Thêm điểm lưu**: mỗi màn ≥ 2 điểm lưu thật (màn 6–10: 3 điểm, cách nhau ~2000 px), giữ cờ lưu giả nhưng đặt **ngay trước** một cờ thật | Sửa điểm yếu lớn nhất; giữ nhịp chết–thử lại ≤ 15 giây | programmer | nhỏ |
| 2 | **Coyote time 6 khung + jump buffer 6 khung** (bấm nhảy hơi sớm trước khi chạm đất vẫn nhảy) | Người chơi tức vì bẫy, không phải vì điều khiển; rất quan trọng trên cảm ứng | programmer | nhỏ |
| 3 | **Câu chọc quê xoay vòng + theo số lần chết**: mỗi nguyên nhân 2–3 câu; chết ≥ 5 lần cùng chỗ thì câu đổi giọng gợi ý ("Lần thứ 5 rồi đó… thử đi bộ thay vì nhảy coi 🤭") | Giữ tiếng cười, đồng thời là gợi ý mềm cho bẫy khó → công bằng hơn | designer viết câu, programmer gắn | nhỏ |
| 4 | **"Dấu hiệu sau khi bị lừa"**: lần 2 trở đi bẫy để lại dấu nhỏ (tim bom có ngòi lấp ló, cầu sét giả đổi màu nhẹ, dừa/cột băng rung trước khi rớt, xương giả có mắt) | Đúng chuẩn "lần 1 bị lừa, lần 2 né được" → tức nhưng muốn chơi lại | programmer + artist | vừa |
| 5 | **Lưu kỷ lục từng màn trên bản đồ**: số lần chết ít nhất, thời gian tốt nhất, xương nhặt/tổng; thẻ màn hiện 1–3 huy hiệu (qua màn · nhặt hết xương · chết ≤ 3 lần) | Tạo lý do chơi lại; biến xương thành mục tiêu | programmer + artist (icon huy hiệu) | vừa |
| 6 | **Nút tạm dừng thật + rung khi chết** (`navigator.vibrate` 80 ms) và màn hình hướng dẫn điều khiển 1 lần ở màn 1 | Trải nghiệm mobile cơ bản; tạm dừng thật còn làm troll TẠM DỪNG giả buồn cười hơn vì người chơi đã quen nút thật | programmer | nhỏ |
| 7 | **Thẻ khoe "Giấy chứng tử"** sau khi qua màn/phá đảo: ảnh Lu xỉu + "Chết 47 lần ở Màn 4 – Hết tin nổi" + chết nhiều nhất vì bẫy gì, nút lưu ảnh/chia sẻ | Thể loại troll lan truyền nhờ khoe; tận dụng sẵn số đếm chết | programmer + artist | vừa |
| 8 | **Bỏ troll "lần đầu lướt ngược" khỏi thời điểm nguy hiểm**: chỉ kích hoạt khi Lu đang đứng trên đất an toàn ở biển "Bấm ⚡ lướt qua cổng điện" (màn 5) | Hiện có thể làm người chơi rớt hố ngay lần đầu dùng phép → cảm giác bị lừa vô lý | programmer | nhỏ |
| 9 | **Lấp đoạn trống màn 7–10** bằng 1–2 bẫy "thở" (vui, không chết: chim ỉa lên đầu, biển báo đổi chữ, Lu tè trúng hố giả lộ ra) | Nhịp độ đều hơn, giảm cảm giác chạy lại nhàm | designer + programmer | vừa |
| 10 | **Âm thanh "báo trước" cho bẫy rơi** (tiếng rắc rắc của dừa/cột băng, tiếng cót két đèn chùm) và giọng sủa khác nhau theo nguyên nhân chết | Cho người chơi kênh thứ hai để học bẫy; tăng chất hài | sound | nhỏ |
| 11 | **Chế độ "Lu Ngược" (Hard)** mở sau khi phá đảo: chơi lại 10 màn với bẫy **đảo vị trí** (đất thật thành giả, giả thành thật, cờ đích đứng yên nhưng cờ lưu bỏ chạy…) | Tái sử dụng nội dung có sẵn, phạt người chơi "học thuộc" → cực hợp thể loại; nhân đôi thời lượng | designer + programmer | lớn |
| 12 | **Màn mới "Màn 11 – Phòng khám thú y"** (màn bí mật mở bằng cách nhặt hết xương 10 màn): kim tiêm bay, bàn cân bật lò xo, máy sấy lông thổi gió, vòng cổ loa che màn hình, chú mèo "y tá" dẫn đường giả; kết thúc bằng Lu được tắm sạch bọ chét (ending thật) | Nội dung mới có lý do câu chuyện (bọ chét → đi thú y), làm xương có giá trị, là phần thưởng cho người chơi giỏi | designer + programmer + artist + sound | lớn |

**Đề xuất làm trước (đợt 1, nhanh và thấy hiệu quả ngay):** #1, #2, #3, #6, #8 – đều nhỏ, có thể làm cùng một đợt, giải quyết thẳng điểm yếu 1, 2 và mobile.
**Đợt 2:** #4, #5, #7, #10. **Đợt 3 (nội dung mới):** #12 trước rồi #11 (màn mới dễ kiểm soát phạm vi hơn chế độ đảo bẫy cho cả 10 màn).

### Tiêu chí "xong là gì" (đợt 1)
- **#1 Điểm lưu:** mỗi màn có ≥ 2 cờ lưu thật (màn 6–10 có 3); chết sau cờ thì hồi sinh tại cờ đó; người kiểm thử đo: từ chỗ hồi sinh tới bẫy kế tiếp ≤ 15 giây đi bộ ở mọi màn. Cờ lưu giả vẫn hoạt động như cũ.
- **#2 Coyote/buffer:** rời mép đất ≤ 6 khung (0,1 giây) vẫn nhảy được; bấm nhảy ≤ 6 khung trước khi chạm đất thì nhảy ngay khi chạm. Không ảnh hưởng nhảy trên mây, lò xo, trọng lực ngược. Hố giả màn 3 vẫn giết người chơi nếu nhảy.
- **#3 Câu chọc quê:** mỗi nguyên nhân có ≥ 2 câu, không lặp liên tiếp; từ lần chết thứ 5 cùng nguyên nhân trong một màn hiện câu gợi ý (một câu gợi ý cho mỗi bẫy khó: tim bom, cầu sét giả, bóng râm giả, dừa/cột băng sớm, cờ lưu giả, cổng giả, hố giả, cầu khỉ gãy).
- **#6 Mobile:** nút ⏸ thật dừng mọi chuyển động và nhạc, có "Tiếp tục / Bản đồ"; điện thoại rung ngắn khi chết (tắt được cùng nút 🔊); màn 1 hiện hướng dẫn điều khiển 1 lần đầu tiên (lưu localStorage).
- **#8 Lướt ngược:** troll lướt ngược chỉ xảy ra khi Lu đang đứng trên đất; không bao giờ xảy ra trên không hay khi phía trước là hố.

---

## 10. Câu hỏi còn mở (cần anh trả lời)
1. Anh muốn giữ "chỉ 1 điểm lưu" như một phần độ khó, hay đồng ý thêm điểm lưu (đề xuất #1)?
2. Xương có nên thành "tiền" (mua mũ/vòng cổ cho Lu) hay chỉ là huy hiệu/mở màn bí mật? Em đề xuất **huy hiệu + mở màn bí mật** cho gọn phạm vi.
3. Có muốn thêm tính năng chia sẻ ảnh (cần xin quyền lưu ảnh trong APK) không?
4. Ưu tiên nội dung mới: màn bí mật (#12) hay chế độ "Lu Ngược" (#11)?
