
from telethon import TelegramClient, events
from telethon.errors.rpcerrorlist import SlowModeWaitError
from telethon.sessions import StringSession
from datetime import datetime
import asyncio

def load_api_id():
    try:
        with open('api_id.txt', 'r') as file:
          api_id = file.read().strip()
    except Exception as e:
        api_id = input(">> Masukkan API ID: ")
        with open('api_id.txt', 'w') as file:
           file.write(api_id)
        print("\x1b[32m[✓] api_id.txt telah disimpan\x1b[0m\n")

    return api_id

def load_api_hash():
    try:
        with open('api_hash.txt', 'r') as file:
           api_hash = file.read().strip()
    except Exception as e:
        api_hash = input(">> Masukkan API Hash: ")
        with open('api_hash.txt', 'w') as file:
           file.write(api_hash)
        print("\x1b[32m[✓] api_hash.txt telah disimpan\x1b[0m")

    return api_hash

api_id = load_api_id()
api_hash = load_api_hash()

new_file = False

def load_pesan():
    global new_file

    msg = ""

    try:
        with open('msg.txt', 'r') as file:
            msg = file.read().strip()
        print("\x1b[32m[✓] msg.txt Loaded\x1b[0m")
    except Exception as e:
        makefile = input("> file msg.txt tidak ditemukan, ingin membuatnya? (y): ")

        if makefile:
           with open('msg.txt', 'w') as file:
              file.write(msg)
           print("\x1b[32m[✓] msg.txt telah dibuat\x1b[0m")
           new_file = True

    return msg

def update_pesan():
     msg = load_pesan()

     if new_file == False:
        with open('msg.txt', 'w') as file:
           file.write(msg)
        print("\x1b[32m[✓] msg.txt berhasil diperbarui\x1b[0m")

     return msg

errorGa = False

async def send_pesan_groups(client, group, message, count, delay):
    global errorGa

    try:
        entity = await client.get_entity(group)
        for _ in range(count * 60 * 60):
            try:
                await client.send_message(entity, message, parse_mode="md")

                now = datetime.now()
                time = now.strftime('%H:%M - %d/%m/%Y')
                print(f"\x1b[96m\x1b[1m[{time}] \x1b[92mBerhasil mengirim ke: {group}\x1b[0m")
                await asyncio.sleep(delay)
            except SlowModeWaitError as e:
                wait_time = e.seconds
                print(f"\x1b[33m\x1b[1m>> Slow mode untuk grup {group}, menunggu selama {wait_time} detik\x1b[0m")
                await asyncio.sleep(wait_time)
            except Exception as e:
                print(f"\x1b[31m\x1b[1m[x] Tidak berhasil memgirim ke {group}\n>> Dengan kesalahan: {e}\x1b[0m")
                await asyncio.sleep(60)
    except Exception as e:
        errorGa = True
        print(f"\x1b[31m\x1b[1m[x] Maaf saya tidak menemukang grup: {group}\x1b[0m")
        return

async def send_messages_concurrently(client, groups, message, count, delay):
    tasks = [send_pesan_groups(client, group, message, count, delay) for group in groups]
    await asyncio.gather(*tasks)

async def main():
    global errorGa

    print("\n\x1b[35m\x1b[1m【 𝚂𝚌𝚛𝚒𝚙𝚝 𝚖𝚊𝚍𝚎 𝚋𝚢 𝙲𝚊𝚖𝚒𝚘 𝚍𝚎 𝚂𝚘𝚕𝚟𝚘𝚒𝚍 】\n\x1b[33m【 𝚃𝚎𝚕𝚎𝚐𝚛𝚊𝚖: @𝙲𝚊𝚖𝚒𝚘𝙳𝚎𝚂𝚘𝚕𝚟𝚘𝚒𝚍 】\x1b[0m\n")

    try:
        with open('api_id.txt', 'r') as file:
           api_id = file.read().strip()
        print("\x1b[32m[✓] api_id.txt Loaded\x1b[0m")
    except Exception as e:
        api_id = input(">> Masukkan API ID: ")
        with open('api_id.txt', 'w') as file:
           file.write(api_id)
        print("\x1b[32m[✓] api_id.txt telah disimpan\x1b[0m")

    try:
        with open('api_hash.txt', 'r') as file:
           api_hash = file.read().strip()
        print("\x1b[32m[✓] api_hash.txt Loaded\x1b[0m")
    except Exception as e:
        api_hash = input(">> Masukkan API Hash: ")
        with open('api_hash.txt', 'w') as file:
           file.write(api_hash)
        print("\x1b[32m[✓] api_hash.txt telah disimpan\x1b[0m")

    client = None
    session_file = 'session.txt'

    input_orno = input("\nApakah ingin menggunakan nomor telepon baru? (y/n): ").lower()

    if input_orno == 'y':
        nomor_tele = input("\n> Masukkan nomor telepon: ")
        print("\x1b[93m> Wait Sedang mengirimkan kode OTP\x1b[0m")

        client = TelegramClient(StringSession(), api_id, api_hash)
        await client.connect()

        try:
            await client.send_code_request(nomor_tele)
            code = input(f"> Masukkan kode OTP yang dikirimkan ke \x1b[96m({nomor_tele})\x1b[0m\n> Masukkan kode: ")
            await client.sign_in(nomor_tele, code)

            with open(session_file, 'w') as f:
                f.write(client.session.save())

            print(f"\n\x1b[92m[✓] Berhasil masuk dengan nomor telepon \x1b[93m{nomor_tele}\x1b[0m")

        except Exception as e:
            print(f"\n\x1b[31m[x] Terjadi kesalahan: {e}\x1b[0m")
            return

    elif input_orno == 'n':
        try:
            client = TelegramClient(StringSession(open(session_file).read()), api_id, api_hash)
            await client.start()

            print("\n\x1b[92m[✓] Berhasil masuk dengan session sebelumnya\x1b[0m")

        except Exception as e:
            print(f"\n\x1b[31m[x] Terjadi kesalahan: {e}\x1b[0m")
            return

    else:
        print("\n\x1b[31m[x] Masukan tidak valid, silakan masukkan 'y' atau 'n'\x1b[0m")
        return

    msg = update_pesan()

    input_grups = input("\n\x1b[33m> Example: grup1, grup2, grup3, grup4, dst...\x1b[0m\n> Inputkan grup yg akan dikirim: ")
    groups = [group.strip() for group in input_grups.split(',')]

    input_durasi = input("\n\x1b[33m> Example: 10 = 10 Jam / 48 = 48 Jam atau 2 Hari\x1b[0m\n> Inputkan durasi sesi ini: ")
    while not input_durasi.isdigit():
        input_durasi = input("\n\x1b[91m[x] Harus berupa angka!\n\x1b[33m> Example: 10 = 10 Jam / 48 = 48 Jam atau 2 Hari\x1b[0m\n> Inputkan durasi sesi ini: ")

    input_jeda = input("\n\x1b[33m> Example: 30 = 30 Detik / 120 = 2 Menit (Disarankan 120detik)\x1b[0m\n> Inputkan jeda pengiriman pesan: ")
    while not input_jeda.isdigit():
        input_jeda = input("\n\x1b[91m[x] Harus berupa angka!\n\x1b[33m> Example: 30 = 30 Detik / 120 = 2 Menit (Disarankan 120detik)\x1b[0m\n> Inputkan jeda pengiriman pesan: ")

    conv = ', '.join(groups)
    print(f"\n\x1b[96m[CamioSc]\x1b[0m Pesan ini akan terkirim ke: \x1b[36m{conv}\n\x1b[96m[CamioSc]\x1b[0m Durasi: \x1b[96m{input_durasi} jam\x1b[0m, Jeda: \x1b[96m{input_jeda} detik\x1b[0m\n")

    try:
        await client.connect()
        await send_messages_concurrently(client, groups, msg, int(input_durasi), int(input_jeda))
        if errorGa == False:
            print("\n\x1b[92m[✓] Sesi ini sudah selesai\n\n\x1b[95mTerimakasih sudah menggunakan script saya\n- Regret @CamioDeSolvoid -\x1b[0m")
        else:
            print("\n\x1b[92m[✓] Sesi ini sudah selesai\n\x1b[91m>> Dengan kesalahan: grup tidak ditemukan\x1b[0m")
    except Exception as e:
        print(f"\x1b[31mTerjadi kesalahan: {e}\x1b[0m")
    finally:
        await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
