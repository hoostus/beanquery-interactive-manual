import marimo

__generated_with = "0.20.4"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(heading):
    title_hd = heading(1, "Interactive beanquery manual", number=False)
    title_hd
    return (title_hd,)


@app.cell
def _(mo):
    mo.md("""
    <style>
    h1, h2, h3, h4, h5 {
        margin-top: 0.1em;
        margin-bottom: 0.1em;
    }
    </style>
    """)
    return


@app.cell(hide_code=True)
def _():
    import io

    from beancount.loader import load_string
    from beancount.core import display_context
    from beancount.parser import printer as bc_printer

    from beanquery.query import run_query
    from beanquery.query_render import render_text

    import marimo as mo

    HEADING_COLOR = "#1e40af"
    _heading_counters = [0, 0, 0, 0]  # h2, h3, h4, h5

    def heading(level: int, text: str, number: bool = True) -> mo.Html:
        """Render a colored markdown heading with optional hierarchical numbering.

        Numbering starts from level 2 (level 1 is reserved for title).
        """
        prefix = ""
        if number and 2 <= level <= len(_heading_counters) + 1:
            idx = level - 2  # 0=h2, 1=h3, 2=h4
            _heading_counters[idx] += 1
            # Reset child counters
            for i in range(idx + 1, len(_heading_counters)):
                _heading_counters[i] = 0
            prefix = ".".join(str(_heading_counters[i]) for i in range(idx + 1)) + ". "
        return mo.md(
            f"<h{level} style='color: {HEADING_COLOR}; margin-top: 0.1em !important; margin-bottom: 0.1em !important;'>"
            f"{prefix}{text}</h{level}>"
        )

    def get_beanquery_output(ledger_text: str, query: str) -> str:
        """
        Executes a BeanQuery command on a ledger string and returns output as text.

        Args:
            ledger_text (str): Beancount ledger as text
            query (str): BeanQuery query

        Returns:
            str: formatted output (or formatted error)
        """

        # 1. Parse ledger
        entries, errors, options_map = load_string(ledger_text)

        if errors:
            buf = io.StringIO()
            bc_printer.print_errors(errors, file=buf)
            return buf.getvalue()

        # 2. Run query
        dcontext = display_context.DisplayContext()

        try:
            rtypes, rrows = run_query(entries, options_map, query)

            buf = io.StringIO()
            render_text(rtypes, rrows, dcontext, buf)

            return buf.getvalue()

        except Exception as e:
            return f"BeanQuery error: {type(e).__name__}: {e}"

    def query_output(ledger_text: str, query: str) -> mo.Html:
        """
        Runs a BeanQuery and returns the result as a marimo plain_text element.

        Args:
            ledger_text: Beancount ledger as text
            query: BeanQuery query string

        Returns:
            mo.Html: formatted output for display
        """
        return mo.plain_text(get_beanquery_output(ledger_text, query))


    def ledger_editor(default_text: str, label: str = ""):
        """
        Creates a marimo code editor for the ledger.
        Defined mainly for future extensibility (e.g. beancount syntax highlighting, etc.)
        Args:
            default_text: initial text for the editor
            label: label for the editor

        Returns:
            mo.ui.UIElement: the code editor UI element
        """
        # TODO: add beancount syntax highlighting
        ui = mo.ui.code_editor(default_text, label=label, show_copy_button=True, debounce=True)
        return ui

    def query_editor(default_text: str, label: str = ""):
        """
        Creates a marimo code editor for the query.
        Defined mainly for future extensibility (e.g. beanquery syntax highlighting, etc.)

        Args:
            default_text: initial text for the editor
            label: label for the editor

        Returns:
            mo.ui.UIElement: the code editor UI element
        """
        ui = mo.ui.code_editor(default_text, language="sql", label=label, show_copy_button=True, min_height=1, debounce=True)
        return ui

    return heading, ledger_editor, mo, query_editor, query_output


@app.cell(hide_code=True)
def _(heading, title_hd):
    _=title_hd
    intro_hd =heading(2, "Introduction to this document", number=True)
    intro_hd
    return (intro_hd,)


@app.cell
def _(heading, intro_hd):
    _=intro_hd
    purpose_hd =heading(3, "Purpose and scope", number=True)
    purpose_hd
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The purpose of this document is to be an interactive and updated to the beanquery v3 replacement of the [Beancount Query Language](https://docs.google.com/document/d/1s0GOZMcrKKCLlP29MD7kHO4L88evrwWdIO0p4EwRBE0/edit?usp=sharing) document
    """)
    return


@app.cell(hide_code=True)
def _(heading, intro_hd):
    # This is a workarount to enforce the sequence of the header executions, as marimo 
    # does not necessarily execute the cells in the top-to-bottom order, 
    # and the header numbering relies on the execution order.
    _=intro_hd
    how_to_use__man_h =heading(3, "How to use the manual")
    how_to_use__man_h
    return (how_to_use__man_h,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    You can read the manual as a normal text document.
    You can also change the default both ledger and query inputs.
    As soon an input widget will lose focus, a query will be re-executed and output output will be updated
    """)
    return


@app.cell
def _(heading, how_to_use__man_h):
    _ = how_to_use__man_h
    int_beanquery_hd = heading(2, "Introduction to beanquery", number=True)
    int_beanquery_hd
    return (int_beanquery_hd,)


@app.cell
def _(mo):
    mo.md(r"""
    Beancount’s parsed list of entries is like an in-memory database represented in a form of several tables. Beanquery is a command-line tool that acts like a client to that in-memory database in which you can type queries in a variant of SQL. You invoke it like this:

    ```shell
    beanquery  test.bean
    Input file: "Beancount"
    Ready with 3 directives (2 postings in 1 transactions, 0 validation errors)
    beanquery>
    ```
    Beanquery started as an experiment in beancount v2, but in v3 (when **bean-web** has been discontinued) became pretty much the only tool to query information out of beancount ledger. One can say, that beancount has moved towrds the [Self-service business intelligence](https://www.techtarget.com/searchbusinessanalytics/definition/self-service-business-intelligence-BI) model.
    """)
    return


@app.cell(hide_code=True)
def _(heading, int_beanquery_hd):
    _prev = int_beanquery_hd
    how_to_install_h = heading(2, "How to install beanquery")
    how_to_install_h
    return (how_to_install_h,)


@app.cell
def _(mo):
    mo.md(r"""
    `
    pip install beanquery
    `
    """)
    return


@app.cell
def _(heading, how_to_install_h):
    _prev = how_to_install_h
    how_to_start_h = heading(2, "How to run beanquery")
    how_to_start_h
    return (how_to_start_h,)


@app.cell
def _(mo):
    mo.md(r"""
    To run beanquery type

    ```shell
    beanquery [OPTIONS] FILENAME [QUERY]...
    ```

    **Result:** beanquery will load ledger and start the beanquery client

    e.g.:

    ```shell
    beanquery  test.bean
    Input file: "Beancount"
    Ready with 3 directives (2 postings in 1 transactions, 0 validation errors)
    beanquery>
    ```

    You can also start beanquery as a python module

    ```shell
    python -m beanquery [OPTIONS] FILENAME [QUERY]...
    ```
    """)
    return


@app.cell
def _(heading, how_to_start_h):
    _prev = how_to_start_h
    how_to_get_help_h = heading(2, "How to get help")
    how_to_get_help_h
    return


@app.cell
def _(mo):
    mo.md(r"""
    To get a help from the built in system, type `.help` when in the beanquery client

    ```shell
    beanquery> .help

    Shell utility commands (type help <topic>):
    ===========================================
    EOF    describe  exit     format  history  parse  reload  set
    clear  errors    explain  help    output   quit   run     tables

    Beancount query commands:
    =========================
    balances  from  journal  print  select  targets  where

    beanquery>
    ```

    To get a list of the tables, available for beancount type `.tables`

    ```shell
    beanquery> .tables
    accounts
    balances
    commodities
    documents
    entries
    events
    notes
    postings
    prices
    transactions
    beanquery>
    ```

    To see list of columns, available in every table type `.describe <table name>`

    e.g. to see list of columns in the **postigs** table type

    ```shell
    beanquery> .describe postings
    table postings:
      type (str)
      id (str)
      date (date)
      year (int)
      month (int)
      day (int)
      filename (str)
      lineno (int)
      location (str)
      flag (str)
      payee (str)
      narration (str)
      description (str)
      tags (set)
      links (set)
      posting_flag (str)
      account (str)
      other_accounts (set)
      number (decimal)
      currency (str)
      cost_number (decimal)
      cost_currency (str)
      cost_date (date)
      cost_label (str)
      position (position)
      price (amount)
      weight (amount)
      balance (inventory)
      meta (dict)
      entry (transaction)
      accounts (set[str])
    beanquery>
    ```
    To see the list of columns in the **transactions** table type:

    ```shell
    beanquery> .describe transactions
    table transactions:
      meta (metadata)
      date (date)
      flag (str)
      payee (str)
      narration (str)
      tags (set)
      links (set)
      accounts (set[str])
    beanquery>
    ```
    """)
    return


@app.cell
def _(ledger_editor):
    _ledger = """\
    2023-01-01 open Assets:Cash USD
    2023-01-01 open Expenses:Food USD

    2023-01-10 * "Shop"
      Expenses:Food   20 USD
      Assets:Cash    -20 USD"""

    ledger_ui = ledger_editor(_ledger, label="Ledger:")
    ledger_ui
    return (ledger_ui,)


@app.cell
def _(query_editor):
    _sql = "select *"
    sql_ui = query_editor(_sql, label="BeanQuery SQL:")
    sql_ui
    return (sql_ui,)


@app.cell
def _(ledger_ui, query_output, sql_ui):
    query_output(ledger_ui.value, sql_ui.value) 
    return


if __name__ == "__main__":
    app.run()
