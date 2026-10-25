# MUSE-AI — Theme cho Knulli / Batocera

Theme do Muse thiết kế: nền mực sâu với quầng sáng hổ phách và teal, tên hệ
máy khổng lồ có phát sáng và bóng phản chiếu 3D, video game trong khung bo
tròn có bóng đổ và vệt sáng, metadata xếp chip rõ ràng, font đẹp và rõ.

## Điểm nhấn

- **Màn system:** tên hệ máy cực lớn (Tektur), phát sáng hổ phách, phản
  chiếu phía dưới, nền aurora mực + sao tia.
- **Màn detailed:** video/boxart khung bo tròn + bóng đổ + vệt sáng chéo,
  danh sách chọn gradient hổ phách, watermark tên hệ máy mờ khổng lồ.
- **Màn grid:** ô game phóng to khi chọn, tên game chạy chữ ở thanh trên.
- **Màn splash:** thanh tiến trình hổ phách, nhãn nạp bằng font đủ dấu.
- **Font đủ tiếng Việt trọn vẹn:** Tektur (tiêu đề) + Inter (nội dung),
  cả hai đều đủ khối ký tự ghép sẵn 1EA0–1EF9 — không vỡ font.
- **Âm thanh:** tiếng tick nhẹ khi gạt dpad.

## Cài đặt

Chép toàn bộ thư mục này vào `/userdata/themes/MUSE-AI` trên máy, rồi vào
EmulationStation → UI Settings → Theme Set → chọn MUSE-AI.

## Font

- Tektur, Inter — SIL Open Font License 1.1 (xem file OFL trong `fonts/`).

## Phiên bản

- v0.1.1: định nghĩa carousel hệ thống đúng chuẩn (hết dải xám mặc định
  của ES); màn system mỗi hệ có ảnh chìm riêng (16 hệ: fbneo, nes, psx,
  psp, snes, gba, gbc, gb, c64, ports, megadrive, nds, pcengine, atari2600,
  dreamcast, n64); thanh trạng thái trên mọi màn hình: giờ, % pin + icon
  pin, icon mạng. Lưu ý: ES không có phần tử theme hiển thị ngày tháng,
  và không đọc được trạng thái dịch vụ SSH/Tailscale nên theme không thể
  hiện 2 biểu tượng đó — xem trạng thái dịch vụ trong menu Knulli.
- v0.1.0: system, basic, detailed, grid, menu, help, splash.
