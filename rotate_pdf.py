"""
Obraca wybrane strony pliku PDF i zapisuje wynik jako nowy plik.
Wszystko dzieje się lokalnie na Twoim komputerze.

Instalacja (raz):
    pip install pypdf

TRYB PROSTY (okienka):
    Kliknij dwukrotnie plik rotate_pdf.py albo wpisz:
        python rotate_pdf.py
    1. Wybierz PDF w okienku.
    2. Wpisz kąt obrotu (90 = w prawo, -90 = w lewo, 180).
    3. Wpisz strony (np. 1 albo 1,3-5) lub zostaw puste = wszystkie.
    Wynik zapisze się obok oryginału z dopiskiem "_obrocony".

TRYB Z TERMINALA:
    python rotate_pdf.py WEJSCIE.pdf WYJSCIE.pdf KAT [STRONY]
    np. python rotate_pdf.py dyplom.pdf dyplom_ok.pdf 90 1,3-5
"""

import os
import sys
from pypdf import PdfReader, PdfWriter


def parse_pages(spec: str, total: int) -> set[int]:
    """Zamienia np. '1,3-5' na zbiór indeksów stron (od 0)."""
    pages = set()
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            start, end = part.split("-", 1)
            pages.update(range(int(start) - 1, int(end)))
        else:
            pages.add(int(part) - 1)
    invalid = [p + 1 for p in pages if p < 0 or p >= total]
    if invalid:
        raise ValueError(f"Plik ma {total} stron, a podano: {invalid}")
    return pages


def rotate(input_path: str, output_path: str, angle: int, pages_spec: str = "") -> str:
    if angle % 90 != 0:
        raise ValueError("Kąt musi być wielokrotnością 90 (np. 90, 180, 270, -90).")
    reader = PdfReader(input_path)
    total = len(reader.pages)
    pages = parse_pages(pages_spec, total) if pages_spec.strip() else set(range(total))

    writer = PdfWriter()
    for i, page in enumerate(reader.pages):
        added = writer.add_page(page)
        if i in pages:
            added.rotate(angle)
    with open(output_path, "wb") as f:
        writer.write(f)

    nums = ", ".join(str(p + 1) for p in sorted(pages))
    return f"Obrócono strony [{nums}] o {angle}°.\nZapisano:\n{output_path}"


def gui_mode() -> None:
    import tkinter as tk
    from tkinter import filedialog, simpledialog, messagebox

    root = tk.Tk()
    root.withdraw()

    input_path = filedialog.askopenfilename(
        title="Wybierz plik PDF do obrócenia",
        filetypes=[("Pliki PDF", "*.pdf")],
    )
    if not input_path:
        return

    angle = simpledialog.askinteger(
        "Kąt obrotu",
        "O ile stopni obrócić?\n90 = w prawo, -90 = w lewo, 180 = do góry nogami",
        initialvalue=90,
    )
    if angle is None:
        return

    pages_spec = simpledialog.askstring(
        "Strony",
        "Które strony obrócić? (np. 1 albo 1,3-5)\nZostaw puste = wszystkie strony",
    ) or ""

    base, ext = os.path.splitext(input_path)
    output_path = f"{base}_obrocony{ext}"

    try:
        msg = rotate(input_path, output_path, angle, pages_spec)
        messagebox.showinfo("Gotowe", msg)
    except Exception as e:
        messagebox.showerror("Błąd", str(e))


def main() -> None:
    if len(sys.argv) == 1:
        gui_mode()
        return
    if len(sys.argv) not in (4, 5):
        print(__doc__)
        sys.exit(1)
    try:
        print(rotate(sys.argv[1], sys.argv[2], int(sys.argv[3]),
                     sys.argv[4] if len(sys.argv) == 5 else ""))
    except Exception as e:
        sys.exit(f"Błąd: {e}")


if __name__ == "__main__":
    main()
