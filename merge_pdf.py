"""
Łączy kilka plików PDF w jeden. Wszystko dzieje się lokalnie na Twoim komputerze.

Instalacja (raz):
    pip install pypdf

TRYB PROSTY (okienka):
    Kliknij dwukrotnie plik merge_pdf.py albo wpisz:
        python merge_pdf.py
    1. Wybierz pliki PDF w okienku (Ctrl+klik, żeby zaznaczyć kilka).
    2. Potwierdź albo zmień kolejność.
    3. Wskaż, gdzie zapisać połączony plik.
    4. Zdecyduj, czy wyrównać wszystkie strony do A4.

TRYB Z TERMINALA:
    python merge_pdf.py WYJSCIE.pdf PLIK1.pdf PLIK2.pdf PLIK3.pdf [--a4]
    Pliki zostaną połączone w podanej kolejności.
    --a4 = wyrównaj wszystkie strony do formatu A4.
"""

import os
import sys
from pypdf import PdfReader, PdfWriter, PageObject, Transformation
from pypdf.generic import RectangleObject

A4_W, A4_H = 595.28, 841.89  # punkty PDF


def to_a4(page: PageObject) -> None:
    """Skaluje i centruje stronę (już dodaną do PdfWriter) na A4,
    pion lub poziom zgodnie z oryginałem. Działa z pypdf 4–7."""
    page.transfer_rotation_to_content()
    box = page.cropbox
    w, h = float(box.width), float(box.height)
    tw, th = (A4_H, A4_W) if w > h else (A4_W, A4_H)
    s = min(tw / w, th / h)
    tx = (tw - w * s) / 2 - float(box.left) * s
    ty = (th - h * s) / 2 - float(box.bottom) * s
    page.add_transformation(Transformation().scale(s).translate(tx, ty))
    a4 = RectangleObject([0, 0, tw, th])
    page.mediabox = a4
    page.cropbox = a4
    page.trimbox = a4
    page.bleedbox = a4
    page.artbox = a4


def merge(inputs: list[str], output_path: str, a4: bool = False) -> str:
    if len(inputs) < 2:
        raise ValueError("Wybierz co najmniej 2 pliki PDF.")
    writer = PdfWriter()
    total = 0
    for path in inputs:
        reader = PdfReader(path)
        for page in reader.pages:
            added = writer.add_page(page)
            if a4:
                to_a4(added)
        total += len(reader.pages)
    with open(output_path, "wb") as f:
        writer.write(f)
    names = "\n".join(f"{i}. {os.path.basename(p)}" for i, p in enumerate(inputs, 1))
    return f"Połączono {len(inputs)} plików ({total} stron):\n{names}\n\nZapisano:\n{output_path}"


def gui_mode() -> None:
    import tkinter as tk
    from tkinter import filedialog, simpledialog, messagebox

    root = tk.Tk()
    root.withdraw()

    files = list(filedialog.askopenfilenames(
        title="Wybierz pliki PDF do połączenia (Ctrl+klik = kilka)",
        filetypes=[("Pliki PDF", "*.pdf")],
    ))
    if not files:
        return
    if len(files) < 2:
        messagebox.showerror("Błąd", "Wybierz co najmniej 2 pliki PDF.")
        return

    listing = "\n".join(f"{i}. {os.path.basename(p)}" for i, p in enumerate(files, 1))
    order = simpledialog.askstring(
        "Kolejność",
        f"Wybrane pliki:\n{listing}\n\n"
        "Wpisz kolejność numerami, np. 2,1,3\n"
        "Zostaw puste = kolejność jak powyżej",
    )
    if order is None:
        return
    if order.strip():
        try:
            idx = [int(x) - 1 for x in order.split(",") if x.strip()]
            if sorted(idx) != list(range(len(files))):
                raise ValueError
            files = [files[i] for i in idx]
        except ValueError:
            messagebox.showerror("Błąd", "Podaj każdy numer dokładnie raz, np. 2,1,3")
            return

    output_path = filedialog.asksaveasfilename(
        title="Zapisz połączony PDF jako",
        defaultextension=".pdf",
        initialdir=os.path.dirname(files[0]),
        initialfile="polaczony.pdf",
        filetypes=[("Pliki PDF", "*.pdf")],
    )
    if not output_path:
        return

    a4 = messagebox.askyesno(
        "Rozmiar stron",
        "Wyrównać wszystkie strony do formatu A4?\n\n"
        "Tak = wszystkie strony tej samej wielkości\n"
        "Nie = każda strona zostaje w oryginalnym rozmiarze",
    )

    try:
        messagebox.showinfo("Gotowe", merge(files, output_path, a4))
    except Exception as e:
        messagebox.showerror("Błąd", str(e))


def main() -> None:
    if len(sys.argv) == 1:
        gui_mode()
        return
    args = sys.argv[1:]
    a4 = "--a4" in args
    args = [a for a in args if a != "--a4"]
    if len(args) < 3:
        print(__doc__)
        sys.exit(1)
    try:
        print(merge(args[1:], args[0], a4))
    except Exception as e:
        sys.exit(f"Błąd: {e}")


if __name__ == "__main__":
    main()
