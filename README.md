ผู้ใช้:

1. <code>/join</code> - เข้าร่วมเป็นสมาชิก
2. <code>/credit</code> - ตรวจสอบเครดิตปัจจุบันของคุณ
3. <code>/user</code> - ตรวจสอบ User ID ของคุณ
4. <code>/withdraw [จำนวนเงิน]</code> - สร้างคำขอถอนเครดิต เช่น /withdraw 50
5. <code>/withdrawhistory</code> - ดูประวัติการถอนของคุณ

ผู้ดูแลระบบ (Admin):

1. <code>/increase [User ID] [จำนวนเงิน]</code> - เพิ่มเครดิตให้ผู้ใช้ เช่น /increase USER_ID 50
2. <code>/decrease [User ID] [จำนวนเงิน]</code> - ลดเครดิตของผู้ใช้ เช่น /decrease USER_ID 50
3. <code>/withdrawlist</code> - แสดงรายการคำขอถอนที่กำลังรอดำเนินการ
4. <code>/approve [Request ID]</code> - อนุมัติคำขอถอนเครดิต เช่น /approve REQUEST_ID
5. <code>/reject [Request ID]</code> - ปฏิเสธคำขอถอนเครดิต เช่น /reject REQUEST_ID
