Công nghệ nhận dạng ký tự quang học (OCR) hiện nay rất phát triển, ứng dụng rộng rãi trong nhiều tình huống thực tế. Framework PaddleOCR cung cấp những công cụ hiệu quả để phát hiện, nhận dạng các văn bản trong nhiều trường hợp đơn giản cũng như thách thức như văn bản cong, tỷ lệ thay đổi... với nhiều ngôn ngữ khác nhau. Dựa trên framework này luận văn huấn luyện với dữ liệu VinText và các dữ liệu được tạo ra, góp phần nâng cao độ chính xác nhận dạng Tiếng Việt.<br>
Trong quá trình huấn luyện, luận văn đã không ngừng cải tiến bộ dữ liệu huấn luyện. Thử nghiệm dữ liệu VinText ban đầu không cho kết quả tốt, nên nhiều dữ liệu khác được phát sinh, bao gồm cảnh ảnh sinh ra từ từ điển Tiếng Việt, sinh cảnh ảnh từ từ điển Tiếng Anh với các từ f, j, w, z, sinh cảnh ảnh có chữ viết hoa là tên người Việt phổ biến, sinh cảnh ảnh từ các ký tự có dấu là đặt trưng của tiếng Việt, các ký tự dễ nhầm lẫn, cảnh ảnh từ các bảng hiệu cửa hàng được download từ Google và được chú thích.<br>
Người thực hiện sử dụng mô hình DB trên dữ liệu ICDAR15 do PP-OCRv3 cung cấp làm kiến thức phát hiện văn bản với phần cài đặt tham số unclip ratio lớn để mở rộng hộp<br>
nhận dạng sau khi phát hiện nhằm lấy được các dấu của chữ để tăng độ chính xác nhận dạng.
Ở nhiệm vụ nhận dạng văn bản, luận văn thử nghiệm với bốn thuật toán khác nhau là MobileNetv3, SVTRNet, ABINet (RestNet 45), RFL (ResNet RFL). Mô hình MobileNetv3 cho kết quả tốt nhất.<br>
Với kiến thức từ mô hình phát hiện và nhận dạng cho phương pháp hai giai đoạn, kết quả nhận biết đạt được ở tập test là 76.6%.<br>
Một số kết quả từ quá trình huấn luyện:<br>
<img width="652" alt="image" src="https://github.com/user-attachments/assets/188e9628-f5f7-424e-a595-151536ae0f61" /><br>
Biểu đồ huấn luyện, đánh giá của mô hình MobileNetv3: <br>
<img width="468" alt="image" src="https://github.com/user-attachments/assets/dee0370d-c3f9-4c8a-b488-3416e9b7168e" /><br>
<img width="468" alt="image" src="https://github.com/user-attachments/assets/2ea40b21-cb74-4917-9fea-36f07c1498a2" /><br>
<img width="468" alt="image" src="https://github.com/user-attachments/assets/fbb2fcda-ad4b-4b24-adb2-d3942c93e328" /><br>
<img width="468" alt="image" src="https://github.com/user-attachments/assets/7298a24a-c515-46f2-8e55-dc520f41132b" /><br>
Kết quả nhận dạng đạt được:<br>
<img width="468" alt="image" src="https://github.com/user-attachments/assets/65368fc3-cd19-45d3-82d7-b278e93765c7" /><br>
<img width="468" alt="image" src="https://github.com/user-attachments/assets/e8adfac6-1d0c-46eb-b11c-2965738ca080" /><br>
<img width="468" alt="image" src="https://github.com/user-attachments/assets/79c009f9-32c7-40af-a301-e5c48083d7a5" /><br>
<img width="468" alt="image" src="https://github.com/user-attachments/assets/59ccacc2-d452-44cf-9906-963df8ef65f0" /><br>
<img width="468" alt="image" src="https://github.com/user-attachments/assets/939f1b69-4115-475e-8ca1-99c1ba56796c" /><br>
<img width="468" alt="image" src="https://github.com/user-attachments/assets/ef3f2f3e-e3d0-49b6-95cc-64fb9af0d99a" /><br>
<img width="468" alt="image" src="https://github.com/user-attachments/assets/22d030c7-30b2-4a7a-9f97-4f9bf7e2b072" /><br>
<img width="468" alt="image" src="https://github.com/user-attachments/assets/4642580f-b6d2-4f4b-b97b-3e9ecc2773e1" /><br>












