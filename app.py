from flask import Flask, render_template, request

app = Flask(__name__)


def caesar_cipher(text, shift, mode="encrypt"):
    """Caesar Cipher: geser huruf dengan shift tertentu."""
    if mode == "decrypt":
        shift = -shift

    result = []
    for ch in text:
        if "A" <= ch <= "Z":
            base = ord("A")
            result.append(chr((ord(ch) - base + shift) % 26 + base))
        elif "a" <= ch <= "z":
            base = ord("a")
            result.append(chr((ord(ch) - base + shift) % 26 + base))
        else:
            result.append(ch)
    return "".join(result)


def vigenere_cipher(text, key, mode="encrypt"):
    """Vigenère Cipher dengan key huruf."""
    if not key:
        raise ValueError("Key Vigenère tidak boleh kosong.")

    # bersihkan key: hanya huruf
    clean_key = "".join([c for c in key if c.isalpha()])
    if not clean_key:
        raise ValueError("Key Vigenère harus berisi huruf A–Z.")

    clean_key = clean_key.upper()
    result = []
    key_index = 0
    key_len = len(clean_key)

    for ch in text:
        if ch.isalpha():
            k = ord(clean_key[key_index % key_len]) - ord("A")
            if mode == "decrypt":
                k = -k

            if ch.isupper():
                base = ord("A")
                result.append(chr((ord(ch) - base + k) % 26 + base))
            else:
                base = ord("a")
                result.append(chr((ord(ch) - base + k) % 26 + base))

            key_index += 1
        else:
            result.append(ch)

    return "".join(result)


def rail_fence_encrypt(text, rails):
    """Rail Fence Cipher - enkripsi."""
    if rails < 2:
        raise ValueError("Rail minimal 2.")

    fence = [[] for _ in range(rails)]
    row = 0
    direction_down = True

    for ch in text:
        fence[row].append(ch)

        if rails > 1:
            if row == 0:
                direction_down = True
            elif row == rails - 1:
                direction_down = False

            row += 1 if direction_down else -1

    return "".join("".join(row_chars) for row_chars in fence)


def rail_fence_decrypt(cipher, rails):
    """Rail Fence Cipher - dekripsi."""
    if rails < 2:
        raise ValueError("Rail minimal 2.")

    length = len(cipher)
    # buat pola zigzag
    pattern = [[False] * length for _ in range(rails)]

    row = 0
    direction_down = True
    for col in range(length):
        pattern[row][col] = True

        if rails > 1:
            if row == 0:
                direction_down = True
            elif row == rails - 1:
                direction_down = False
            row += 1 if direction_down else -1

    # isi huruf cipher ke posisi pattern yang True
    fence = [[""] * length for _ in range(rails)]
    idx = 0
    for r in range(rails):
        for c in range(length):
            if pattern[r][c]:
                fence[r][c] = cipher[idx]
                idx += 1

    # baca ulang sesuai zigzag
    result = []
    row = 0
    direction_down = True
    for col in range(length):
        result.append(fence[row][col])

        if rails > 1:
            if row == 0:
                direction_down = True
            elif row == rails - 1:
                direction_down = False
            row += 1 if direction_down else -1

    return "".join(result)


def process_cipher(algorithm, mode, text, key_raw):
    if not text.strip():
        raise ValueError("Teks tidak boleh kosong.")

    algorithm = algorithm.lower()
    mode = mode.lower()

    if algorithm == "caesar":
        try:
            shift = int(key_raw)
        except ValueError:
            raise ValueError("Shift untuk Caesar harus berupa angka.")
        return caesar_cipher(text, shift, mode)

    elif algorithm == "vigenere":
        return vigenere_cipher(text, key_raw, mode)

    elif algorithm == "railfence":
        try:
            rails = int(key_raw)
        except ValueError:
            raise ValueError("Jumlah rail harus berupa angka.")
        return rail_fence_encrypt(text, rails) if mode == "encrypt" else rail_fence_decrypt(text, rails)

    else:
        raise ValueError("Algoritma tidak dikenal.")


# Util untuk penilaian soal
def normalize_answer(s: str) -> str:
    """Normalisasi jawaban: huruf saja, uppercase."""
    return "".join(ch for ch in s.upper() if ch.isalpha())


# ================== ROUTE HALAMAN UTAMA ==================
@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    error = ""
    text = ""
    key = ""
    algorithm = "caesar"
    mode = "encrypt"

    if request.method == "POST":
        algorithm = request.form.get("algorithm", "caesar")
        mode = request.form.get("mode", "encrypt")
        text = request.form.get("text", "")
        key = request.form.get("key", "")

        try:
            result = process_cipher(algorithm, mode, text, key)
        except ValueError as e:
            error = str(e)

    return render_template(
        "index.html",
        result=result,
        error=error,
        text=text,
        key=key,
        algorithm=algorithm,
        mode=mode,
    )

@app.route("/soal", methods=["GET", "POST"])
def soal():
    correct_q1 = "JHJV MJW TJVKRWP JMJUJQ VJTJWJW HJWP BJWPJC NWJT"
    correct_q2 = "AKU SUKA INDOMIE RENANG"
    correct_q3 = "KUDA TERBANG KELIHATAN BOHONGNYA"
    correct_q4 = "SEMUT RENANG IKAN MERANGKAI KATA"
    correct_q5 = "KITA SERANG RUSIA BESOK MALAM YA"

    score = None
    max_score = 5
    results = {}

    q1 = q2 = q3 = q4 = q5 = ""

    if request.method == "POST":
        q1 = request.form.get("q1", "")
        q2 = request.form.get("q2", "")
        q3 = request.form.get("q3", "")
        q4 = request.form.get("q4", "")
        q5 = request.form.get("q5", "")

        score = 0
        results = {}

        # Q1
        if normalize_answer(q1) == normalize_answer(correct_q1):
            score += 1
            results["q1"] = {"correct": True, "expected": correct_q1}
        else:
            results["q1"] = {"correct": False, "expected": correct_q1}

        # Q2
        if normalize_answer(q2) == normalize_answer(correct_q2):
            score += 1
            results["q2"] = {"correct": True, "expected": correct_q2}
        else:
            results["q2"] = {"correct": False, "expected": correct_q2}

        # Q3
        if normalize_answer(q3) == normalize_answer(correct_q3):
            score += 1
            results["q3"] = {"correct": True, "expected": correct_q3}
        else:
            results["q3"] = {"correct": False, "expected": correct_q3}

        # Q4
        if normalize_answer(q4) == normalize_answer(correct_q4):
            score += 1
            results["q4"] = {"correct": True, "expected": correct_q4}
        else:
            results["q4"] = {"correct": False, "expected": correct_q4}

        # Q5
        if normalize_answer(q5) == normalize_answer(correct_q5):
            score += 1
            results["q5"] = {"correct": True, "expected": correct_q5}
        else:
            results["q5"] = {"correct": False, "expected": correct_q5}

    return render_template(
        "soal.html",
        score=score,
        max_score=max_score,
        results=results,
        q1=q1,
        q2=q2,
        q3=q3,
        q4=q4,
        q5=q5,
    )



if __name__ == "__main__":
    app.run(debug=True)