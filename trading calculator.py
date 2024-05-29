import tkinter as tk
from tkinter import messagebox
from math import floor

# it's best practice to define a GUI app in a class so everything is structured well

class StockTradingPlanner(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Trade Calculator")
        self.geometry("768x864")  # window size
        self.resizable(0,0)            # to prohibit resizing of window

        # What to do when user clicks X
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # registering numerical input validation command
        self.float_validation_cmd = self.register(self.validate_float)

        # CREATING FRAMES FOR WIDGETS
        self.frame1 = tk.LabelFrame(self,
                               text="Account Information",
                               font=("Calibri", 13, 'bold'))

        self.frame2 = tk.LabelFrame(self,
                               text="Trade Plan",
                               font=("Calibri", 13, 'bold'))

        self.app_header()
        self.frame1_widgets()
        self.frame2_widgets()
        self.grid_config()

    def app_header(self):
        # MAIN HEADING AND DESCRIPTION
        self.heading = tk.Label(self,
                                text="Trade Calculator",
                                font=("Calibri", 15, 'bold'))

        self.description = tk.Label(self,
                                    text="Use this Calculator to identify key numerical quantities in your trade,\n"
                                         "such as your profit/loss margins. All from a few numbers that you input.",
                                    justify="left",
                                    font=("Calibri", 11))

    def frame1_widgets(self):
        # ACCOUNT SIZE INPUT WIDGET
        self.account_size_label = tk.Label(self.frame1,
                                           text="Account Size ($)",
                                           font=("Calibri", 11, 'bold'))

        self.account_size_var = tk.StringVar()
        self.account_size_var.trace_add('write', self.dollar_amt)
        self.account_size_box = tk.Entry(self.frame1,
                                         validate="all",
                                         validatecommand=(self.float_validation_cmd, '%P'),
                                         textvariable=self.account_size_var,
                                         font=("Calibri", 11))

        # % RISK SLIDER WIDGET
        self.risk_slider_label = tk.Label(self.frame1,
                                          text="How Much Capital Can You Risk (%)?",
                                          font=("Calibri", 11, 'bold'))

        self.risk_slider_var = tk.DoubleVar()
        self.risk_slider_var.trace_add('write', self.dollar_amt)
        self.percent_risk_slider = tk.Scale(self.frame1,
                                            orient='horizontal',
                                            from_=0,
                                            to=20,
                                            tickinterval=2,
                                            resolution=0.1,
                                            length=240,
                                            sliderlength=20,
                                            variable=self.risk_slider_var,
                                            activebackground='#3778bf')

        # DOLLAR RISK BOX
        self.dollar_risk_box_label = tk.Label(self.frame1,
                                              text="Max Dollar Amount You Can Risk",
                                              font=("Calibri", 11, 'bold'))

        self.dollar_risk_var = tk.DoubleVar()
        self.dollar_risk_var.trace_add('write', self.partial_share_size_calc)
        self.dollar_risk_var.trace_add('write', self.max_share_size_calc)

        self.dollar_risk_box = tk.Text(self.frame1,
                                       height=1,
                                       width=18,
                                       state='disabled',
                                       bg='#D3D3D3')

        self.risk_box_description = tk.Label(self.frame1,
                                             text="This value depends on your account\nsize "
                                                  "and your % risk tolerance",
                                             justify="left",
                                             font=("Calibri", 10))

    def frame2_widgets(self):
        # ENTRY PRICE WIDGET
        self.entry_price_label = tk.Label(self.frame2,
                                          text="Entry Price ($)",
                                          font=("Calibri", 11, 'bold'))

        self.entry_price_var = tk.StringVar()
        self.entry_price_var.trace_add('write', self.percent_profit_loss)
        self.entry_price_var.trace_add('write', self.loss_per_share)
        self.entry_price_var.trace_add('write', self.partial_share_size_calc)

        self.entry_price_box = tk.Entry(self.frame2,
                                        validate="all",
                                        validatecommand=(self.float_validation_cmd, '%P'),
                                        textvariable=self.entry_price_var,
                                        font=("Calibri", 11),
                                        width=20)

        # STOP LOSS WIDGET
        self.stop_loss_label = tk.Label(self.frame2,
                                        text="Max Stop Loss ($)",
                                        font=("Calibri", 11, 'bold'))

        self.stop_loss_var = tk.StringVar()
        self.stop_loss_var.trace_add('write', self.percent_profit_loss)
        self.stop_loss_var.trace_add('write', self.loss_per_share)

        self.stop_loss_box = tk.Entry(self.frame2,
                                      validate='all',
                                      validatecommand=(self.float_validation_cmd, '%P'),
                                      textvariable=self.stop_loss_var,
                                      font=("Calibri", 11))

        # PROFIT PRICE WIDGET
        self.target_price_label = tk.Label(self.frame2,
                                           text="Target Price ($)",
                                           font=("Calibri", 11, 'bold'))

        self.target_price_var = tk.StringVar()
        self.target_price_var.trace_add('write', self.percent_profit_loss)
        self.target_price_var.trace_add('write', self.partial_share_size_calc)

        self.target_price_box = tk.Entry(self.frame2,
                                         validate='all',
                                         validatecommand=(self.float_validation_cmd, '%P'),
                                         textvariable=self.target_price_var,
                                         font=("Calibri", 11))

        # % PROFIT WIDGET
        self.percent_profit_label = tk.Label(self.frame2,
                                             text="% Profit a Target Price",
                                             font=("Calibri", 11, 'bold'))

        self.percent_profit_box = tk.Text(self.frame2,
                                          height=1,
                                          width=18,
                                          state='disabled',
                                          bg='#D3D3D3')

        # % LOSS WIDGET
        self.percent_loss_label = tk.Label(self.frame2,
                                           text="% Loss at Max Stop Loss",
                                           font=("Calibri", 11, 'bold'))

        self.percent_loss_box = tk.Text(self.frame2,
                                        height=1,
                                        width=18,
                                        state='disabled',
                                        bg='#D3D3D3')

        # LOSS PER SHARE WIDGET
        self.loss_per_share_label = tk.Label(self.frame2,
                                             text="Loss Per Share at Stop Loss",
                                             font=("Calibri", 11, 'bold'))

        self.loss_per_share_var = tk.DoubleVar()
        self.loss_per_share_var.trace_add('write', self.max_share_size_calc)

        self.loss_per_share_box = tk.Text(self.frame2,
                                          height=1,
                                          width=18,
                                          state='disabled',
                                          bg='#D3D3D3')

        # MAX SHARE SIZE WIDGET
        self.max_share_size_label = tk.Label(self.frame2,
                                             text="Max No. of Shares Allowed",
                                             font=("Calibri", 11, 'bold'))

        self.max_share_size_box = tk.Text(self.frame2,
                                          height=1,
                                          width=18,
                                          state='disabled',
                                          bg='#D3D3D3')

        # PARTIAL SHARE SIZE WIDGET
        self.partial_share_size_label = tk.Label(self.frame2,
                                                 text="Partial No. of Shares to Cover Risk",
                                                 font=("Calibri", 11, 'bold'))

        self.partial_share_size_box = tk.Text(self.frame2,
                                              height=1,
                                              width=18,
                                              state='disabled',
                                              bg='#D3D3D3')

        self.partial_share_size_description = tk.Label(self.frame2,
                                                       text="This is the number of shares\nyou can sell at your target price to\ncover your account risk basis",
                                                       justify='left')

    def grid_config(self):
        # HEADING AND DESCRIPTION
        self.heading.grid(row=0,
                          column=0,
                          sticky=tk.W,
                          padx=15,
                          pady=(5, 0))

        self.description.grid(row=1,
                              column=0,
                              sticky=tk.W,
                              padx=15,
                              pady=(0,20))

        self.frame1.grid(row=2,
                         column=0,
                         sticky=tk.NW,
                         padx=30)

        self.frame2.grid(row=2,
                         column=1,
                         sticky=tk.W,
                         padx=15)

        # FRAME 0 WIDGETS
        # ACCOUNT SIZE WIDGET
        self.account_size_label.grid(row=0,
                                     column=0,
                                     sticky=tk.W,
                                     padx=20,
                                     pady=(5,0))

        self.account_size_box.grid(row=1,
                                   column=0,
                                   sticky=tk.W,
                                   padx=20,
                                   ipady=2,
                                   pady=(0, 10))

        # % RISK SLIDER WIDGET
        self.risk_slider_label.grid(row=2,
                                    column=0,
                                    sticky=tk.W,
                                    padx=20)

        self.percent_risk_slider.grid(row=3,
                                      column=0,
                                      sticky=tk.W,
                                      padx=20,
                                      pady=(0, 10))

        # DOLLAR RISK BOX
        self.dollar_risk_box_label.grid(row=4,
                                        column=0,
                                        padx=20,
                                        sticky=tk.W)

        self.dollar_risk_box.grid(row=5,
                                  column=0,
                                  padx=20,
                                  ipady=3,
                                  sticky=tk.W)

        self.risk_box_description.grid(row=6,
                                       column=0,
                                       padx=15,
                                       pady=(0,10),
                                       sticky=tk.W)

        # FRAME 2 WIDGETS
        # ENTRY PRICE WIDGET
        self.entry_price_label.grid(row=0,
                                    column=1,
                                    padx=15,
                                    pady=(5,0),
                                    sticky=tk.W)

        self.entry_price_box.grid(row=1,
                                  column=1,
                                  sticky=tk.W,
                                  padx=15,
                                  ipady=2,
                                  pady=(0, 10))

        # STOP LOSS WIDGET
        self.stop_loss_label.grid(row=2,
                                  column=1,
                                  sticky=tk.W,
                                  padx=15)

        self.stop_loss_box.grid(row=3,
                                column=1,
                                sticky=tk.W,
                                padx=15,
                                ipady=2,
                                pady=(0,10))

        # TARGET PRICE WIDGET
        self.target_price_label.grid(row=4,
                                     column=1,
                                     sticky=tk.W,
                                     padx=15)

        self.target_price_box.grid(row=5,
                                   column=1,
                                   sticky=tk.W,
                                   ipady=2,
                                   padx=15,
                                   pady=(0,10))

        # % PROFIT WIDGET
        self.percent_profit_label.grid(row=6,
                                       column=1,
                                       sticky=tk.W,
                                       padx=15)

        self.percent_profit_box.grid(row=7,
                                     column=1,
                                     sticky=tk.W,
                                     padx=15,
                                     pady=(0, 10),
                                     ipady=3)

        # % LOSS WIDGET
        self.percent_loss_label.grid(row=8,
                                     column=1,
                                     sticky=tk.W,
                                     padx=15)

        self.percent_loss_box.grid(row=9,
                                   column=1,
                                   sticky=tk.W,
                                   padx=15,
                                   pady=(0,10),
                                   ipady=3)

        # LOSS PER SHARE WIDGET
        self.loss_per_share_label.grid(row=10,
                                       column=1,
                                       sticky=tk.W,
                                       padx=15)

        self.loss_per_share_box.grid(row=11,
                                     column=1,
                                     sticky=tk.W,
                                     padx=15,
                                     pady=(0, 10),
                                     ipady=3)

        # MAX SHARE SIZE WIDGET
        self.max_share_size_label.grid(row=12,
                                       column=1,
                                       sticky=tk.W,
                                       padx=15)

        self.max_share_size_box.grid(row=13,
                                     column=1,
                                     sticky=tk.W,
                                     padx=15,
                                     pady=(0, 10),
                                     ipady=3)

        # PARTIAL SHARE SIZE WIDGET
        self.partial_share_size_label.grid(row=14,
                                           column=1,
                                           sticky=tk.W,
                                           padx=15)

        self.partial_share_size_box.grid(row=15,
                                         column=1,
                                         sticky=tk.W,
                                         padx=15,
                                         ipady=3)

        self.partial_share_size_description.grid(row=16,
                                                 column=1,
                                                 padx=10,
                                                 pady=(0,10),
                                                 sticky=tk.W)

    # proprietary method to check if inputted value is a float
    def is_float(self, num):
        try:
            float(num)
            return True
        except ValueError:
            return False

    def validate_float(self, value):
        if self.is_float(value) or str(value) == "":
            return True
        else:
            return False

    def percent_change(self, initial, final):
        per_change = ((final - initial) / initial) * 100

        return round(per_change, 2)  # truncated to two decimals

    # Modifies the % Profit and Loss boxes depending on the entry, loss, and target price inputted
    def percent_profit_loss(self, *args):
        entry_price = float(self.entry_price_var.get())
        stop_loss_price = float(self.stop_loss_var.get())

        try:
            target_price = float(self.target_price_var.get())
        except ValueError:
            target_price = 0

        percent_profit = self.percent_change(entry_price, target_price)

        self.percent_profit_box.config(state='normal',
                                       font=('Calibri',11))
        self.percent_profit_box.delete('1.0', 'end')
        self.percent_profit_box.insert(tk.END, f"{percent_profit:.2f}%")
        self.percent_profit_box.config(state='disabled')

        percent_loss = self.percent_change(entry_price, stop_loss_price)

        self.percent_loss_box.config(state='normal',
                                     font=('Calibri', 11))
        self.percent_loss_box.delete('1.0', 'end')
        self.percent_loss_box.insert(tk.END, f"{percent_loss:.2f}%")
        self.percent_loss_box.config(state="disabled")


    def dollar_amt(self, *args):
        acct_size = float(self.account_size_var.get())
        percent = self.percent_risk_slider.get()

        dollar_value = round((percent/100)*acct_size, 2)
        self.dollar_risk_var.set(dollar_value)

        self.dollar_risk_box.config(state='normal',
                                    font=("Calibri", 11))

        self.dollar_risk_box.delete('1.0', 'end')

        self.dollar_risk_box.insert(tk.END,f"${dollar_value:.2f}")
        self.dollar_risk_box.config(state='disabled')

    def loss_per_share(self, *args):
        entry_price = float(self.entry_price_var.get())
        stop_price = float(self.stop_loss_var.get())

        loss_per = entry_price - stop_price

        self.loss_per_share_var.set(loss_per)

        self.loss_per_share_box.config(state='normal',
                                       font=("Calibri", 11))
        self.loss_per_share_box.delete('1.0', 'end')

        self.loss_per_share_box.insert(tk.END, f"${loss_per:.2f}")
        self.loss_per_share_box.config(state='disabled')

    def max_share_size_calc(self, *args):
        max_loss = self.dollar_risk_var.get()
        loss_per_share = self.loss_per_share_var.get()

        max_size = floor(max_loss/loss_per_share)

        self.max_share_size_box.config(state='normal',
                                       font=("Calibri", 11))
        self.max_share_size_box.delete('1.0', 'end')

        self.max_share_size_box.insert(tk.END, f"{max_size}")
        self.max_share_size_box.config(state='disabled')

    def partial_share_size_calc(self, *args):
        max_loss = self.dollar_risk_var.get()
        entry_price = float(self.entry_price_var.get())
        target_price = float(self.target_price_var.get())

        chg_in_price = target_price - entry_price

        partial_size = floor(max_loss / chg_in_price)

        self.partial_share_size_box.config(state='normal',
                                           font=("Calibri", 11))
        self.partial_share_size_box.delete('1.0', 'end')

        self.partial_share_size_box.insert(tk.END, f"{partial_size}")
        self.partial_share_size_box.config(state='disabled')

    # when user clicks X on window, confirmation appears
    def on_close(self):
        choice = messagebox.askyesno(title="Confirmation",
                                     message="Are you sure you want to quit Trade Calculator?")
        
        if choice:
            self.destroy()


application = StockTradingPlanner()
application.mainloop()


