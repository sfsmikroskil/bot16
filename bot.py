import asyncio
from playwright.async_api import async_playwright
import pytesseract
import random as r
import json
import state
from data16 import contacts
from PIL import Image

def updateIndex(new_index):
    """Fungsi untuk memperbarui nilai CURRENT_INDEX di file state.py"""
    with open('state.py', 'w') as f:
        f.write(f"last_index = {new_index}\n")
    with open("state.py", "r") as f:
        print("Isi state:", f.read())

def getHP():
    hpAwalan = ["0852", "0822", "0853", "0857", "0813", "0822", "0823"]
    n1 = r.randint(1, 9999)
    n1 = f"{n1:04d}"
    n2 = r.randint(1, 9999)
    n2 = f"{n2:04d}"
    noHP = hpAwalan[r.randint(0,6)] + n1 + n2
    return noHP

async def main(nama, email, c):
    async with async_playwright() as p:
        noHP = getHP()
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 720, 'height': 1280})

        # 1. Buka halaman website
        #print("Membuka halaman website...")
        await page.goto("https://virtual-expo.lkpp.go.id/visitor/register")
        
        # 2. Mengisi Form
        #print("Mengisi formulir...")
        await page.wait_for_timeout(2000)
        await page.fill("#profile_name", nama)
        await page.fill("#profile_email", email)
        await page.fill("#profile_company_name", "Kementerian Imigrasi dan Pemasyarakatan")
        await page.fill("#profile_occupation", "Ditjen Imigrasi dan Pemasyarakatan")
        await page.fill("#profile_phone_number", noHP)
        await page.fill("#profile_password", "Admin123")
        await page.fill("#profile_password_confirmation", "Admin123")
        await page.check("input.form-check-input")
        
        await page.wait_for_timeout(1000)
        await page.screenshot(path=f"{c}_regis.png")
        # Simpan index
        updateIndex(c+1)
        #with open("./state.json", "w", encoding="utf-8") as f:
        #    print(f"Tulis ke {c+1}")
        #    json.dump({"last_index": c + 1}, f)
        # 3. Regis
        #print("Mengeklik tombol submit...")
        await page.click("button[type='submit']")
        await asyncio.sleep(3) # Tunggu elemen/canvas termuat sempurna
        
        await page.mouse.click(360, 1008)
        await page.wait_for_timeout(2000)
        await page.screenshot(path=f"{c}lewati.png")

        # 4. Lewati Video
        #print("Lewati Selesai")
        #Close banner
        await page.mouse.click(593, 530)
        await page.wait_for_timeout(2000)
        #print("Close banner selesai")

        # 5. Klik cookies
        await page.mouse.click(620, 1236)
        await page.wait_for_timeout(3000)

        # 6. Masukk Hall
        await page.mouse.click(277, 654)
        await page.wait_for_timeout(2000)
        #print("Masuk Hall selesai")
        

        # 7. Filter booth
        await page.mouse.click(420, 30)
        await page.wait_for_timeout(1000)
        
        await page.keyboard.type("UKPBJ KEMENTERIAN IM")
        await page.wait_for_timeout(1000)
        await page.keyboard.press("Enter")
        await page.wait_for_timeout(2000)
        await page.screenshot(path=f"{c}_1.png")

        #8. Whatsapp
        await page.mouse.click(370, 770)
        await page.wait_for_timeout(2000)

        #Live chat
        await page.mouse.click(360, 669)
        await page.wait_for_timeout(2000)
        await page.screenshot(path=f"{c}_2.png")

        print(f"Akun : ({c}) {nama} | Selesai")
        await browser.close()

if __name__ == "__main__":
    jumlah = 2
    last_index = 0
    4
    # Baca state    
    #try:
        #with open("state.json", "r", encoding="utf-8") as f:
        #    state = json.load(f)
        #    last_index = state.get("last_index", 0)
        #last_index = state.last_index
    #except:
        #last_index = 0
    #mulaiDari = last_index
    mulaiDari=0
    print("Mulai...")
    for i in range (mulaiDari, mulaiDari+jumlah):
        contact = contacts[i]        
        nama = contact["nama"]
        email = contact["email"]
        c = i
        #print(f"Proses: {nama} ({email})")
        asyncio.run(main(nama, email, c))
    print("Selesai")
