# Báo cáo kiểm thử đợt 1 (Hà – Game Tester)

Nhánh `dot-1-cai-tien`, file `index.html`. Ngày 2026-11-10.
Không sửa code game. Em đã soát toàn bộ `git diff index.html`, đọc thêm vùng code liên quan (update, trap, cpReplay, 10 hàm lvN), và chạy thật bằng Chrome headless (Chrome có sẵn trên máy). Cách chạy: sao chép `index.html` sang thư mục tạm, chèn thêm một thẻ `<script>` gọi thẳng `build()`, `update()`, `die()`, `setPause()`... rồi đọc kết quả. Không đụng file gốc. Có chụp ảnh màn hình bảng chết, bảng tạm dừng, bảng hướng dẫn.

Chú thích: [ĐÃ CHẠY] = tái hiện/đo được. [ĐỌC CODE] = chỉ nghi ngờ từ đọc code.

## Kết luận nhanh

Đợt 1 ĐẠT: không có lỗi nghiêm trọng, không có lỗi cú pháp, không có biến chưa khai báo, không có ngoại lệ khi chạy. Còn 2 lỗi vừa và 5 lỗi nhẹ (liệt kê dưới đây), nên sửa lỗi V1 trước khi đóng gói APK.

## Kiểm tra cú pháp và chạy thật

- Chrome nạp trang không có `error` nào. Toàn bộ script chạy tới `build()` cuối file.
- Biến mới `cpZap, DSPOT, MSGI` (khai báo dòng 979), `deathMsg/deathHint/spotN` (dòng 999), `paused` (dòng 202): đều khai báo trước lần dùng đầu tiên lúc chạy, không dính TDZ.
- Mọi nguyên nhân chết mà `die()`/`hint()` có thể gửi đều có trong `MSG` và `HINT`; mọi khóa `MSGX` đều có trong `MSG`. Gọi `pickMsg` 4 lần cho từng nguyên nhân: 0 lần lặp liền nhau.

## Danh sách lỗi

### Nghiêm trọng
Không có.

### Vừa

**V1. Nhấp nhanh nút nhảy trước khi chạm đất chỉ cho cú nhảy lùn.** [ĐỌC CODE + đo một phần]
- Vị trí: `update()`, dòng 1115–1118 (bộ đệm nhảy rồi tới dòng cắt `if(!kj&&P.vy*gd<-4&&!P.spr)P.vy=-4*gd`).
- Cách tái hiện: đang rơi, nhấp nút nhảy ngắn (2–4 khung) khoảng 3–4 khung trước khi chạm đất, thả tay trước lúc chạm. Lúc chạm, bộ đệm kích nhảy nhưng `kj` đã bằng 0 nên cú nhảy bị cắt `vy` về -4 ngay khung đó.
- Mong đợi: bấm sớm vẫn nhảy ra một cú nhảy bình thường (ít nhất cao bằng cú nhấp nhẹ).
- Thực tế: đo được nhấp 2 khung ngay trên đất thì lên cao khoảng 34 px (full giữ nút khoảng 124 px). Cú buffer + đã thả tay tính từ code còn thấp hơn (khoảng 10 px, chưa đo được chính xác). Đây đúng là tình huống bộ đệm sinh ra để cứu (cảm ứng, nhấp vội), nên người chơi sẽ thấy "bấm rồi mà Lu chỉ nhúc nhích".
- Gợi ý cho programmer: khi cú nhảy do bộ đệm, đặt cờ "đã bấm" tới hết N khung (hoặc bỏ qua bước cắt `vy` trong khung nhảy và vài khung đầu).

**V2. Cờ màn 4 (x=4110) hồi sinh ngay trước vùng tối, quái tới nhanh.** [ĐÃ CHẠY]
- Vị trí: `lv4()` dòng 737 (`cps:[2760,4110]`, `dark:{a:4150,b:4650}`), `cpReplay()` dòng 977 (`e.hold=90`).
- Cách tái hiện: chọn màn 4 bằng T.a, đặt `cpX=4110`, `build()`, đứng yên: chết sau khoảng 197 khung (chỉ khoảng 107 khung sau khi hết hold 90 khung) vì bọ nhảy ở x=4300 và 4480. Lu hồi sinh cách vùng tối 40 px, quái ở 190 px và 370 px, người chơi không thấy quái trong tối.
- Các cờ programmer nghi ngờ khác, kết quả đo khi đứng yên: màn 9 cờ 5330 sống 177 khung (chết do bọ nhảy), màn 7 cờ 2450 sống 163 khung (chết do bọ gai x≈2550), màn 6 cờ 5330 và màn 5 cờ 5450 sống hết 600 khung. Màn 7 cờ 2450 là cờ cũ (trước đợt 1 đã là 2450 và đã có hai quái đó) nên không phải lỗi mới; có hold nên còn dễ hơn trước. Màn 9 cờ 5330: chấp nhận được.
- Đề xuất cho designer (chưa chắc là lỗi, cần quyết): kéo dài hold lên khoảng 150 khung cho quái trong 500 px, hoặc dịch bọ ở 4300 về khoảng 4400, hoặc cho vùng tối sáng nhẹ vài giây đầu.

### Nhẹ

**N1. Bộ đệm nhảy thực tế là 5 khung, không phải 6.** [ĐÃ CHẠY]
- Vị trí: `update()` dòng 1115–1117 (`P.jb=JBUF` rồi `else if(P.jb>0)P.jb--` trong cùng khung).
- Tái hiện: thả Lu từ y=300 xuống đất màn 1 (chạm đất ở khung 15), bấm ở khung 10 (6 khung trước): không nhảy; bấm ở khung 11 (5 khung trước): nhảy. Coyote tương tự (còn khoảng 5 khung sau khi rời mép).
- GDD #2 ghi "≤ 6 khung": lệch 1 khung, người chơi gần như không nhận ra. Sửa cho đúng: đặt `P.jb=JBUF+1` hoặc giảm `jb` sau bước kiểm tra.

**N2. Tắt bảng hướng dẫn bằng phím Space làm Lu nhảy vọt ra.** [ĐỌC CODE]
- Vị trí: handler phím dòng 325 (Space gán `K.j=1`, lặp phím) và handler mới trong IIFE dòng ~113 (`tutDone` gọi `setPause(false)` chỉ xóa `K` một lần).
- Tái hiện: màn 1 lần đầu trên máy tính, giữ Space khoảng nửa giây để bấm "Hiểu rồi". Phím lặp (key repeat) đặt lại `K.j=1` ngay sau khi tiếp tục, Lu nhảy một cái. Không nguy hiểm (đầu màn 1).

**N3. Nút ⏸ vẫn hiện ở màn "Qua màn" / "Phá đảo" nhưng bấm không có tác dụng.** [ĐỌC CODE + chạy `setPause`]
- Vị trí: CSS dòng 11 (chỉ ẩn khi `inmap`/`intitle`), `setPause` dòng 374 (`state` khác `play`/`dead` thì `return`).
- Đã chạy: `state='clear'` rồi `setPause(true,'menu')` cho `paused=false`. Phím Esc/P cũng im lặng. Hợp lý nhưng nút có vẻ hỏng; nên ẩn nút hoặc cho phép dừng ở `clear`.

**N4. Bảng "Chết rồi" có thêm dòng gợi ý khá chật.** [ĐÃ CHẠY, có ảnh]
- Vị trí: `centerBox()` dòng 1865–1872: khung cố định cao 170 px, dòng phụ ở y+70 sát dòng gợi ý (khoảng cách chỉ vài px), nhưng vẫn đọc được trên màn 900×500. Chưa thử trên điện thoại thật; nếu máy nhỏ chữ thu về cỡ 12 px thì khó đọc.
- Gợi ý: khi có 3 dòng thì cao khung thêm 30 px hoặc dịch khung lên 15 px.

**N5. Gợi ý có thể trỏ nhầm sang cầu sét giả/cổng giả khi chết vì thứ khác.** [ĐỌC CODE + chạy ép]
- Vị trí: `die()` dòng ~1002 (`hk=(L.trollK&&frame-L.evilT<600)?L.trollK:c`).
- Tái hiện: màn 5, chạm cổng giả (hoặc ăn cầu sét giả ở màn 6–10) rồi chết do bọ chét trong vòng 10 giây, ở chỗ đã chết cùng nguyên nhân ≥ 5 lần: hiện câu gợi ý của cổng giả/cầu sét giả thay vì của bọ chét. Ép thử bằng harness: ra câu "cầu sét giả hút điện". Trong chơi thật hiếm gặp (cần đủ cả hai điều kiện).

**N6. Đếm "lần thứ 5" tính theo (nguyên nhân + vị trí ±260 px), chặt hơn GDD.** [ĐỌC CODE]
- Vị trí: `deathSpot()` dòng 635. GDD #3 ghi "cùng nguyên nhân trong một màn". Hiện: hố rơi mà đang bị `rev/fast/swap/mirror/dark/zapfall` đổi nguyên nhân, mỗi loại đếm riêng; chết rải rác dọc một đoạn dài có thể không bao giờ chạm 5. Đây là thiết kế hợp lý (gợi ý gắn với chỗ), chỉ ghi lại để designer/anh chốt. Đã chạy: chết `pit` 7 lần cùng chỗ thì từ lần 5 hiện gợi ý, lần 1–4 không.

**Phát hiện thêm (không phải lỗi):** `cpZap` hiện gần như thừa vì `zapHave` giữ nguyên qua các lần chết (chỉ reset ở `lvReset()`); `cpReplay` dòng 966 dư nhưng vô hại.

## Kết quả soát từng nghi vấn anh yêu cầu

| Nghi vấn | Kết quả |
| --- | --- |
| Biến chưa khai báo | Không có (chạy thật, không lỗi) |
| Trạng thái không reset khi chết / đổi màn / chọn màn / T.a | Ổn. `lvReset()` dùng ở 4 chỗ (chọn màn, T.a, `nextLevel`, thẻ màn). `build()` đặt `P.coy/jb`, `L.evilT/trollK` lại. Thắng game về bản đồ rồi chọn màn cũng qua `lvReset()`. `DSPOT`, `cpX`, `cpZap`, `zapHave`, `lvDeaths` reset đúng. `MSGI` không reset (cố ý, chỉ ảnh hưởng thứ tự câu) |
| cpReplay làm kẹt câu đố | Không kẹt. [ĐÃ CHẠY] Màn 5 cờ 3150: cửa d1 đóng (đúng như vừa qua `doorclose`), cột thu lôi `on`, bọ hung 3330 còn sống (vẫn có cục phân để kê lên gờ). Màn 6 cờ 3160: cầu vồng thật `on`. Màn 8 cờ 4850: cửa kim tự tháp mở. Màn 10 cờ 4540: cửa g10 và arena mở, boss còn đủ; cờ 5560: boss bị bỏ, cửa boss mở, cửa arena đóng. Cờ ⚡: `cpZap` + `zapHave` bền. Nrg (màn 6–10) luôn đầy lúc hồi sinh (như cũ). Cả 26 cờ: hồi sinh đứng trên đất liền, không rơi hố, đứng yên 150 khung không chết, không ngoại lệ |
| Coyote cho nhảy kép / khi chết / khi tạm dừng | Không. [ĐÃ CHẠY] Bấm nhảy lần hai giữa không trung không nhảy (`vy` chỉ đổi theo trọng lực). Nhảy sau mép 9 khung không nhảy được. `die()` đổi `state` nên `update()` thoát sớm, `P.jb/coy` được `build()` xóa. `update()` bị bỏ khi `paused` |
| Lò xo / mây hồng / lốc xoáy / lộn trọng lực | [ĐỌC CODE] Điều kiện `P.vy*gd>=0` chặn; nhặt xương lộn trọng lực xóa `coy/jb`. Chưa chạy thật 4 cơ chế này |
| Tạm dừng giao với fakepause / fakedeath / fakeclear | Không đụng nhau: bẫy giả vẽ chữ trên canvas, nút thật là DOM riêng. Vừa chạy: dừng ở `dead` được và tiếp tục đúng; `clear`/`map`/`title` không dừng (xem N3) |
| Tạm dừng giao với cảnh chết chậm / bảng chọn màn | Dừng giữa cảnh chết: `deadT` đứng yên [ĐÃ CHẠY]. "Về bản đồ" từ bảng dừng: `paused` về false, bản đồ mở [ĐÃ CHẠY]. `openMap` tự gỡ dừng |
| Esc/P khi gõ ô nhập code | Đúng: handler thoát khi `e.target.tagName==='INPUT'` (dòng 113). [ĐỌC CODE] |
| `visibilitychange` | [ĐÃ CHẠY] Ẩn app khi `play` thì tạm dừng; khi `dead` thì không (đúng ý, cảnh chết tự qua) |
| Âm thanh bật lại sai | Không thấy. `initAudio` chỉ `resume` khi không dừng; `setPause(false)` mới `resume`. Nút 🔊 trong lúc dừng đổi đúng cờ `muted` + nhãn. Rung `buzz` theo `muted`. [ĐỌC CODE] |
| `lutroll_prog` ghi sai | Không. Đợt này không đụng `saveProg/clearLevel`. Hướng dẫn dùng khóa riêng `lutroll_tut`; [ĐÃ CHẠY] xóa khóa rồi `maybeTut` thì hiện, `tutDone` ghi "1" |
| Bẫy theo mốc phía sau cờ | Đặt `done` khi `trig<cx`; mọi bẫy `trig` (rock, rocket, rocketF, bees, dungroll) kiểm `t.done` nên khớp. `fakepause/fakeclear/fakedeath` đặt `t.t=999` khớp điều kiện bẫy. Đã chạy: màn 4 cờ 4110 có `rocketF.done=true` |

## Đối chiếu tiêu chí "xong" đợt 1 (GDD mục 9)

| # | Tiêu chí | Kết quả |
| --- | --- | --- |
| 1 | Mỗi màn ≥ 2 cờ thật, màn 6–10 có 3; hồi sinh tại cờ; ≤ 15 giây tới bẫy kế; cờ giả như cũ | ĐẠT. Số cờ: M1 2, M2 2, M3 3, M4 2, M5 3, M6–10 mỗi màn 3. Cờ giả ngay trước cờ thật: M3 (2600 → 2700), M5 (5380 → 5450), M9 (5250 → 5330). Khoảng cách lớn nhất giữa hai cờ: M10 2650 → 4540 = 1890 px, khoảng 7,9 giây ở 4 px/khung, còn thừa xa 15 giây. Cờ chỉ lưu khi đứng trên đất và không lộn trọng lực. Cờ lưu thật đổi xanh lá |
| 2 | Coyote/buffer 6 khung; không ảnh hưởng mây, lò xo, trọng lực ngược; hố giả M3 vẫn giết | ĐẠT KÈM LỆCH NHẸ. Thực tế 5 khung (N1); cú nhảy buffer lùn (V1). Hố giả M3 (`jumpspike`) dựa vào `!P.on`, nhảy trong 5 khung đệm vẫn bị gai: [ĐỌC CODE], chưa chạy |
| 3 | Mỗi nguyên nhân ≥ 2 câu, không lặp liền; từ lần 5 có gợi ý, đủ 8 bẫy khó | ĐẠT. Gợi ý có đủ: tim bom (`heart`), cầu sét giả (`evilorb`), bóng râm giả (`heat`), dừa/cột băng (`coco/icicle`), cờ lưu giả (`swap`), cổng giả (`fgate`), hố giả (`jumpspike`), cầu khỉ (`monkey`). Đá lăn M8 đổi sang `boulder`, có câu. Đã chạy: 7 lần chết cùng chỗ cho 7 câu (xoay vòng 3 câu), gợi ý bắt đầu lần 5 |
| 6 | Nút ⏸ thật dừng chuyển động và nhạc; Tiếp tục / Bản đồ; rung khi chết, tắt cùng 🔊; màn 1 có hướng dẫn 1 lần | ĐẠT. Bảng dừng và bảng hướng dẫn hiển thị đúng (có ảnh). Hướng dẫn chỉ hiện khi vào màn 1 từ bản đồ (vào bằng code T.a thì bỏ qua, chấp nhận được). Rung `buzz(90)` khi chết và chết giả |
| 8 | Lướt ngược chỉ khi đứng trên đất, không khi phía trước là hố | ĐẠT. `zapTrollSafe` đòi: đứng trên đất thật, không trượt, không lộn trọng lực, đất liền ±210 px hai bên, không quái trong 280 px, không gió/mây giông/sét/súng lửa, không vùng tối. Đã chạy trên M5: 47 trên 307 vị trí đủ điều kiện, trong đó có đoạn x≈330–720 (sau khi nhặt ⚡, trước mây giông) nên troll vẫn xảy ra ở chỗ dự định. M6: chỉ 8/337 vị trí, tức nếu bỏ lỡ ở M5 thì M6 gần như không còn troll; vô hại |

## Cảm giác chơi (cho game-designer)

- Hồi sinh ở cờ làm nhịp chơi lại ngắn hơn rõ rệt (mọi đoạn giữa hai cờ dưới 8 giây đi bộ). Đồng thời cờ giả đặt ngay trước cờ thật làm cờ giả đau hơn và công bằng hơn (vì người chơi biết còn một cờ thật).
- Màn 4 cờ 4110: đoạn dễ chết nhất của đợt 1 (vùng tối + 2 bọ nhảy + 1,5 giây yên tĩnh giả). Cân nhắc dời quái hoặc cho sáng nhẹ 3 giây đầu.
- Bảng "chết lần thứ 5 + gợi ý" nên hiện đi kèm màu khác (vàng/xanh) để người chơi nhận ra đó là gợi ý chứ không phải chọc quê.
- Quái đứng im 1,5 giây sau hồi sinh: người chơi sẽ không nhận ra vì không có dấu hiệu. Có thể làm quái nhấp nháy xám trong lúc hold để biết "đang cho thở".

## Chưa kiểm tra được

- Chạy trên điện thoại thật: cảm ứng, rung (`navigator.vibrate`), joystick khi mở/đóng bảng dừng, kích thước chữ bảng chết ở màn nhỏ.
- Khi `visibilitychange` trên Android WebView (APK): chỉ chạy được mô phỏng sự kiện.
- Lò xo, mây hồng, lốc xoáy với coyote ở runtime (chỉ đọc code).
