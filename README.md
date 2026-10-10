# Dev Tribhoomi POS

Point of sale, stock, bakery and satu production, and built-in accounting for
**Dev Tribhoomi Khadhye Udhyog**, Kathmandu. One computer, one register, works without internet.
Modelled on QuickBooks Point of Sale Pro 2013, which it replaces.

Version 0.2.0

## Install on the shop computer (Windows 10 or 11)

1. Install **Python 3.12** from <https://www.python.org/downloads/windows/>.
   On the first install screen tick **"Add python.exe to PATH"**.
2. Unzip this folder somewhere permanent, for example `C:\DevTribhoomiPOS`.
3. Double-click **`install_windows.bat`**. It needs internet once, for a few minutes.
4. Two shortcuts appear on the desktop:
   - **Dev Tribhoomi POS**: the real shop. The first start asks for the shop details and creates the owner login.
   - **Dev Tribhoomi POS - Practice**: a separate practice company with two weeks of sample sales, for training.
     Login `owner` / `practice` (PIN 9999), cashier Ramesh PIN 1111, baker Gopal PIN 2222.

`run_devpos.bat` and `run_practice.bat` do the same as the shortcuts.

**No Python on the till?** On any Windows PC with this folder installed, run `build_exe.bat`. It makes
`dist\DevTribhoomiPOS\DevTribhoomiPOS.exe`; copy that whole folder to the till and run the exe.

## Where the data lives

`%LOCALAPPDATA%\DevTribhoomiPOS\` (the practice company is in `DevTribhoomiPOS-Practice\`):

| Path | What |
|---|---|
| `devpos.db` | The database (SQLite) |
| `backups\` | Automatic backups (Z-Out, app close); set a second folder on USB or Google Drive in Settings |
| `reports\` | Excel workbooks written by the Report builder agent |
| `online_orders\inbox` | Drop online orders here (JSON or CSV); see Help, section 5 |

To move to a new computer: install, then *Settings > Backups & reports > Restore a backup*.

## What is in it

- **Register:** scan, search or quick buttons with Nepali names; sell by weight from a scale; weighed-pack
  barcodes; hold/recall; split payments (cash, Fonepay, eSewa, Khalti, card, bank, udhaaro, store credit);
  returns and cancellations as credit notes; Tax Invoice or Abbreviated Tax Invoice in English, Nepali or both.
- **End of day:** shifts with opening float, X-Out, Z-Out with denomination count and over/short, payouts,
  cash drops, no-sale log.
- **Items and lists:** spreadsheet-style editing of every list (items, categories, customers, suppliers and farmers,
  employees, units, tax codes, payment methods, reasons); on-hand counts editable in the grid as logged count
  corrections; bulk price changes with preview and history; price tags and barcode labels; Excel import/export.
- **Stock:** receiving, purchase orders from low stock, farm purchases, waste, physical counts, opening stock,
  batches with best-before dates, supplier payments.
- **Production:** recipes, production batches that consume ingredients and cost each finished unit.
- **Orders:** advance orders with deposits; online orders imported from an inbox folder.
- **Reports:** 40+ reports incl. VAT sales and purchase registers, VAT return summary, IRD materialized view,
  audit trail, P&L, balance sheet, trial balance, general ledger; date presets in Bikram Sambat months and the
  Nepali fiscal year; export to formatted Excel.
- **Accounting:** double-entry ledger posted automatically by every document; expenses, transfers, journals.
- **Agents:** transaction supervisor, reorder, expiry, margin, inventory sanity, VAT due, report builder,
  day summary, online orders, backup, integrity, CBMS sync. Optional AI assistant (needs an Anthropic API key).
- **IRD Electronic Billing Procedure:** fiscal-year bill numbers, no edit or delete of issued bills, "Copy of
  Original (n)" reprints, credit notes with reasons, hash-chained audit trail, materialized view, CBMS queue.

The full manual is inside the app: **Help** (or press F1). It is also `devpos/docs/user_guide.md`.

## Before going live

- Ask the tax office (IRD) whether this software needs registering before issuing VAT bills, and confirm the
  abbreviated-invoice limit and the VAT status of each product (satu blends, wheat-flour items, bread).
- Enter real items or import them from Excel (Items > More > Import from Excel > Download template).
- Run a few days in the practice company, then a few days side by side with QuickBooks POS until totals match.

## For developers

```
python -m venv .venv && .venv\Scripts\activate      # or source .venv/bin/activate
pip install -r requirements-dev.txt
python -m pytest -q                                   # 40 tests
python launcher.py --practice
```

Layout: `devpos/core` (database, ledger, sales, stock, tax, agents; no Qt), `devpos/ui` (PySide6 screens),
`devpos/hardware` (drawer, scale, pole display), `tests/`.
