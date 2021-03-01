import API
import requests
import json 

class engine:
    def __init__(self):
        self.API = API.API
        self.SECRET = API.SECRET
        self.COINM = "https://dapi.binance.com/"
    #Get Candle sticks
    def Get_Klines(self,symbol,interval,limit=1500):
        #BNBUSD_PERP for perp futures coin M
        #BNBUSD_210326 for standard futures coin M
        responce = requests.get(
                self.COINM+"dapi/v1/klines",
                params={
                    'symbol':symbol,
                    'interval':interval, 
                    'limit':limit
                }
            )
        return responce.json()
    #Get Latest price        
    def Get_latestPrice(self,symbol):
        responce = requests.get(
                self.COINM+"dapi/v1/klines",
                params={
                    'symbol':symbol,
                    'interval':"1m", 
                    'limit':1
                }
            )
        return float(responce.json()[0][4])

    def get_OrderBook(self,symbol,limit=50):
        responce = requests.get(
                self.COINM+"dapi/v1/depth",
                params={
                    'symbol':symbol,
                    'limit':limit
                }
            )
        return responce.json()
    
    def get_BidPrice(self,symbol,amount):
        import pandas as pd
        responce = requests.get(
                self.COINM+"dapi/v1/depth",
                params={
                    'symbol':symbol,
                    'limit':500
                }
            )
        df = pd.DataFrame(responce.json()['bids'])
        df['Price'] = df[0].astype(float)
        df['Volume_c'] = df[1].astype(float)
        df = df[['Price','Volume_c']]
        df['Volume'] = df['Volume_c'] * 10
        df['Amount'] = df['Volume'] / df['Price']
        df['Volume_cumsum'] = df['Volume'].cumsum()
        df["Amount_cumsum"] = df['Amount'].cumsum()
        dt = df[df['Volume_cumsum']<amount]
        index = dt.last_valid_index()
        if index == None:
            return df['Price'][0]
        else:
            index = float(index) + 1
            df = df[df.index <= index]
            AMOUNTHELPER1 = 0
            AMOUNTHELPER2 = 0
            for index, rows in df.iterrows():
                if rows["Volume_cumsum"] < amount:
                    AMOUNTHELPER1 = AMOUNTHELPER1 + rows["Volume"]
                    AMOUNTHELPER2 = AMOUNTHELPER2 + rows["Amount"]
                else:
                    AMOUNTHELPER2 = AMOUNTHELPER2 + (amount - AMOUNTHELPER1)/rows['Price']
            return round(amount / AMOUNTHELPER2, 3)

    def get_AskPrice(self,symbol,amount):
        import pandas as pd
        responce = requests.get(
                self.COINM+"dapi/v1/depth",
                params={
                    'symbol':symbol,
                    'limit':500
                }
            )
        df = pd.DataFrame(responce.json()['asks'])
        df['Price'] = df[0].astype(float)
        df['Volume_c'] = df[1].astype(float)
        df = df[['Price','Volume_c']]
        df['Volume'] = df['Volume_c'] * 10
        df['Amount'] = df['Volume'] / df['Price']
        df['Volume_cumsum'] = df['Volume'].cumsum()
        df["Amount_cumsum"] = df['Amount'].cumsum()
        dt = df[df['Volume_cumsum']<amount]
        index = dt.last_valid_index()
        if index == None:
            return df['Price'][0]
        else:
            index = float(index) + 1
            df = df[df.index <= index]
            AMOUNTHELPER1 = 0
            AMOUNTHELPER2 = 0
            for index, rows in df.iterrows():
                if rows["Volume_cumsum"] < amount:
                    AMOUNTHELPER1 = AMOUNTHELPER1 + rows["Volume"]
                    AMOUNTHELPER2 = AMOUNTHELPER2 + rows["Amount"]
                else:
                    AMOUNTHELPER2 = AMOUNTHELPER2 + (amount - AMOUNTHELPER1)/rows['Price']
            return round(amount / AMOUNTHELPER2, 3)

        
    #Create and addit logs
    def additlog (self,file_name, list_of_elem):
        from csv import writer
        # Open file in append mode
        with open("logs/"+file_name, 'a+', newline='') as write_obj:
            # Create a writer object from csv module
            csv_writer = writer(write_obj)
            # Add contents of list as last row in the csv file
            csv_writer.writerow(list_of_elem)
    #send an email
    def SentAlert(self,title="No Title",Msg="This is empty email"):
        import smtplib, ssl
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        sender_email = API.SENDER_EMAIL
        receiver_email = API.RECEIVER_EMAIL
        password = API.PASSWORD_EMAIL

        message = MIMEMultipart("alternative")
        message["Subject"] = title
        message["From"] = sender_email
        message["To"] = receiver_email

        # Create the plain-text and HTML version of your message
        text = """Hi Giorgi, \n\nYou have new message: \n{Message}""".format(Message=Msg)
        
        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(text, "plain")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)

        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )