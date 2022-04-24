from binance.client import Client
from datetime import datetime

def get_timestamp(day,month):
    #year is fixed to 2022.
    outputdate = '{} {} 2022 - 0:0:0'.format(day,month)
    outputdate = datetime.strptime(outputdate, "%d %m %Y - %H:%M:%S")
    outputdate = datetime.timestamp(outputdate)
    outputdate*=1000
    return outputdate
def month_check(minusday):
    #this function gets the "minusday" day ago from today's date
    today = datetime.today()
    func_month=today.month
    func_day=today.day
    while(minusday!=0):
        func_day-=1
        if(func_day==0):
            func_month-=1
            if(func_month==4 or func_month==6 or func_month==9 or func_month==1):
                func_day=30
            elif(func_month==2):
                func_day=28
            else:
                func_day=31
        minusday-=1
    return func_day,func_month
def get_daily_PNL(loop_day):

    day,month=month_check(loop_day)            #gets the date "loop_day" days ago 
    tenapril=get_timestamp(day,month)          #converts to timestamp
    day,month=month_check(loop_day-1) 
    finishdate=get_timestamp(day,month)
    alltimepositions=client.futures_income_history(startTime=int(tenapril),endTime=int(finishdate),incomeType="REALIZED_PNL")
    alltimepositions_COMM=client.futures_income_history(startTime=int(tenapril),endTime=int(finishdate),incomeType="COMMISSION")

    income=0.0
    commission=0.0
    for loop_positions in alltimepositions:
        income+=float(loop_positions["income"])
       
    for loop_positions in alltimepositions_COMM:
        commission+=float(loop_positions["income"])
        
    
    return income,commission

def get_balance_USDT():
    #This function stores USDT balance in "tether" variable
    info = client.futures_account_balance()

    for loop_info in info:

        if(str(loop_info["asset"]).upper()=="USDT"):
            tether=loop_info["balance"]
    #print(tether)
    return tether
def get_monthly_PNL():
    #this function prints last 30 day's PNL/COMMISSION values.
    i=7
    total_comm=0.0
    total_PNL=0.0
#-----------------------------------------------
    while(i!=0):
        PNL,COMM=get_daily_PNL(i)
        
        total_comm+=COMM
        realPNL=PNL-COMM
        total_PNL+=realPNL
        day,month=month_check(i)            #gets the date "loop_day" days ago 

        if(PNL!=0):
            print("#############################")
            print("{}/{}'s PNL is= ${:3.2f}".format(day,month,realPNL))
        i-=1
#-----------------------------------------------
    print("#############################")
    print("#############################")

    print("ALL TIME PNL:",total_PNL)
    print("ALL TIME COMM:",total_comm)


def get_current_positions():
    #-----------------------------------------------------
    #bu fonksiyon şuanda açık olan pozları dictionary'ye kaydedecek.
    positions=client.futures_position_information()
    pos_List_Dict= {}
    i=1
    for position in positions:
        if(float(position["positionAmt"])!=0):
            
            pos_List_Dict[i]={
                "symbol":position["symbol"],
                "positionAmt":position["positionAmt"],
                "entryPrice":position["entryPrice"],
                "markPrice":position["markPrice"],
                "unRealizedProfit":position["unRealizedProfit"],
                "liquidationPrice":position["liquidationPrice"],
                "positionSide":position["positionSide"],
                "isolatedWallet":position["isolatedWallet"],
                }
            
            i+=1

    if pos_List_Dict:
        return pos_List_Dict
    else:
        print("you do not have any positions right now!")


#############################################################################################################################
######################################                                              #########################################
######################################                   MAIN                       #########################################
######################################                   BODY                       #########################################
######################################                                              #########################################
#############################################################################################################################

api_key="your api here"
api_secret="your secret key here"
client = Client(api_key, api_secret)



    # print(get_balance_USDT())
#today = datetime.today()
#print(today)
#currentmonth=today.month



