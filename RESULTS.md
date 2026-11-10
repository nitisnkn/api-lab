# API lab results
## Part 0
Step 0.1, the number of pizza names: 18
Step 0.3, status code of the request without a token: 404
Step 0.4, the name of your pizza: Margherita
Step 0.12, results of the three runs without a session (optional): The Red Napoletana, A Bright Siciliana, The Scary Fungi e Olive
Step 0.16, blocks of "how many of the three tools are excluded": 0, 1, 2, 3

## Defect report
Title: Excluding all tools returns 500 instead of 400
Request: POST /api/pizza with body {"excludedTools": ["Knife", "Pizza cutter", "Scissors"]}
Expected result: Status 400 and a JSON error message explaining no pizza can be made
Actual result: Status 500 Internal Server Error with an empty body
Severity: High

## Part A: Input space partitioning for ratings

| Characteristic | Blocks | Values in the tests |
| --- | --- | --- |
| C1 Value of stars | below 1, 1 to 5 (base), above 5 | 0, 3, 6 |
| C2 Type of stars | whole number (base), decimal, text, missing | 3, 3.5, "3", no field |
| C3 Pizza | exists (base), does not exist | a new pizza, 999999999 |
| C4 Token | the user's own (base), none, wrong length | from auth, no header, token short |
## Step A4
Status codes when another user attempts to:
- Read: 404
- Change: 400
- Delete: 400
## Part B
1. **API tests vs Unit tests:** 
   - **API tests can find:** ปัญหาการเชื่อมต่อเครือข่าย (Network/Routing issues) และข้อผิดพลาดจากการทำงานร่วมกันของระบบจริง (Integration issues เช่น Database หรือ Load Balancer) ที่ Unit test แบบใช้ Stub ตรวจไม่พบ
   - **Reason for Unit tests with stubs:** ควรเขียน Unit test ด้วย เพราะทำงานได้เร็วกว่ามาก สามารถทดสอบแยกเฉพาะส่วนได้โดยไม่ต้องพึ่งพาระบบภายนอก และช่วยระบุบรรทัดของโค้ดที่ผิดพลาดได้ชัดเจนกว่า

2. **Test Isolation:**
   - **Why create a new user:** เพื่อให้แต่ละ Test เป็นอิสระจากกัน (Test Isolation) ป้องกันไม่ให้ข้อมูลของ Test หนึ่งไปกระทบผลลัพธ์ของอีก Test หนึ่ง (เช่น Test A ลบข้อมูลที่ Test B กำลังจะอ่าน)
   - **Project 2 application:** ใน Project 2 เราจะสร้างข้อมูลจำลองเฉพาะเจาะจง (เช่น สร้างร้านค้าหรือห้องพักใหม่) สำหรับแต่ละ Test เสมอ เพื่อให้รันทดสอบขนานกันได้โดยไม่แย่งข้อมูลกัน

3. **Session usage:**
   - **Why use one session:** การใช้ Session ช่วยจัดการ Cookie (เช่น Token หรือ Load Balancer cookie) ให้อัตโนมัติ และช่วยประหยัดเวลา/ทรัพยากรเพราะไม่ต้องเปิดการเชื่อมต่อ TCP ใหม่ทุกครั้ง
   - **Step 0.12 result:** หากไม่ใช้ Session, Load Balancer อาจจะส่ง Request ไปยัง Server คนละตัวที่ไม่มีข้อมูล Login ของเรา ทำให้บาง Request ล้มเหลวและเกิดปัญหา Flaky test

4. **Defect in Step 0.16:**
   - **Which block:** บล็อกที่ตัดอุปกรณ์ออกครบทั้ง 3 ชิ้น (3 tools excluded)
   - **Why 500 is worse than 400:** Status 500 (Internal Server Error) ที่ไม่มีข้อความบอกอะไรเลย ทำให้แอปพลิเคชันฝั่ง Client ไม่รู้ว่าเกิดจากสาเหตุอะไร แต่ถ้าตอบ 400 พร้อมข้อความแจ้งเตือน Client จะสามารถแสดงผลให้ผู้ใช้ทราบได้ว่าสั่งพิซซ่าไม่ได้เพราะอะไร
   - **Why keep xfail:** การติดป้าย `xfail` เอาไว้ จะช่วยเตือนความจำว่ามีบั๊กนี้อยู่ หากวันหนึ่งนักพัฒนาแก้บั๊กนี้สำเร็จ โค้ดส่วนนี้จะรันไม่ผ่าน (เพราะ strict=True) ซึ่งจะคอยเตือนให้เรากลับมาเอาป้าย xfail ออก

5. **Coverage count (Step A1):**
   - **Base choice coverage:** ใช้ 9 เคส (คำนวณจาก: 1 Base case + [2 C1 non-base] + [3 C2 non-base] + [1 C3 non-base] + [2 C4 non-base])
   - **All combinations coverage:** ใช้ 72 เคส (คำนวณจาก: 3 x 4 x 2 x 3)

6. **Status codes in Step A4:**
   - **Codes received:** Read ได้ 404, Change ได้ 400, Delete ได้ 400
   - **Expected vs Defect:** เป็น Defect ครับ เพราะปัญหาเรื่องสิทธิ์การเข้าถึงข้อมูลของคนอื่น ควรจะตอบ 403 (Forbidden) เพื่อบอกว่าไม่มีสิทธิ์ หรือ 404 (Not Found) เพื่อซ่อนข้อมูล แต่ไม่ควรตอบ 400 (Bad Request) เพราะรูปแบบคำสั่งของเราถูกต้อง ไม่ได้ผิดไวยากรณ์

7. **Fake token testing:**
   - (คุณสามารถลองรัน `curl -H "madeup.txt" https://quickpizza.grafana.com/api/ratings` เพื่อดูผลลัพธ์) 
   - **Defect explain:** หากระบบพ่นข้อมูลออกมา หรือแสดง Error ที่เปิดเผยโครงสร้างระบบมากเกินไป ถือเป็น Defect เพราะแฮกเกอร์อาจนำข้อมูลหลุดเหล่านั้นไปหาช่องโหว่เพื่อโจมตีระบบจริงต่อได้

8. **API vs Web tests:**
   - **API checks better:** การตรวจสอบโครงสร้าง JSON ที่ตอบกลับมา, ค่า HTTP Status Code ที่ถูกต้องเป๊ะๆ และความเร็วในการตอบสนอง
   - **Web checks better:** การแสดงผลบนหน้าจอ (UI), การคลิกปุ่ม, การแสดงสี/ฟอนต์ และความเข้ากันได้ของเบราว์เซอร์
```[cite: 16]