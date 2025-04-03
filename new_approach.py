import serial
import struct
import time

# Współczynniki konwersji RAW → mm
channel_multi = {
    1: 0.000087,  # dopasowane do 2.972 mm
    2: 0.000087,
    3: 0.00025,
    4: 0.00025,
}

def extract_frames(buffer):
    """Znajduje ramki w buforze – od 0x2A do 0x0D"""
    frames = []
    current = []
    in_frame = False

    for b in buffer:
        if b == 0x2A:  # start
            current = [b]
            in_frame = True
        elif in_frame:
            current.append(b)
            if b == 0x0D:  # koniec ramki
                frames.append(current)
                in_frame = False
    return frames

def parse_frame(frame_bytes):
    """Wyszukuje kanały i przelicza wartości"""
    results = []
    i = 0
    while i < len(frame_bytes) - 4:
        ch = frame_bytes[i]
        status = frame_bytes[i+1]
        if 1 <= ch <= 4 and (status & 0x80):  # ważna wartość
            msb = frame_bytes[i+2]
            lsb = frame_bytes[i+3]
            raw = (msb << 8) + lsb
            multi = channel_multi.get(ch, 0.00025)
            mm = round(raw * multi, 3)
            results.append((ch, raw, mm))
            i += 4
        else:
            i += 1
    return results

def main():
    port = "COM4"
    baudrate = 115200

    try:
        with serial.Serial(port, baudrate, timeout=0.2) as ser:
            print(f"📡 Połączono z {port} @ {baudrate} baud.")
            print("⏳ Oczekiwanie na dane... (przerwij Ctrl+C)\n")

            buffer = bytearray()

            while True:
                data = ser.read(256)
                if data:
                    buffer.extend(data)

                    # Jeśli bufor jest zbyt duży – przytnij
                    if len(buffer) > 1024:
                        buffer = buffer[-512:]

                    # Szukaj ramek
                    frames = extract_frames(buffer)
                    if frames:
                        latest = frames[-1]  # użyj najnowszej
                        results = parse_frame(latest)
                        if results:
                            print("📏 Odczyt:")
                            for ch, raw, mm in results:
                                if ch in [1, 2]:
                                    print(f"  Kanał {ch}: {mm} mm (surowa: {raw})")
                            print()
                        buffer.clear()

                time.sleep(0.1)

    except serial.SerialException as e:
        print(f"❌ Błąd połączenia: {e}")

if __name__ == "__main__":
    main()
