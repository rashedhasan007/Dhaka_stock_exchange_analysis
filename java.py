import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from chart import livechart
from rsi import rsiFunc,rsichart,ploty_graph
from macd import  get_macd,plot_macd,ploty_mcd
import investpy
from coppock import COPP, coppcurve
from movingaverage import  EOM , movingcurve
from datarefine import refine
from linear_reg import linear_reg,L_plot
from K_nearnest import K_training,K_plot
from Auto_ARIMA import arima_training,arima_plot
from lstm import lstm_training,lstm_chart


stock_name=["SGBD(Singer Bangladesh limited)","MJLB(MJL Bangladesh Limited)","BATA(BATA Bangladesh)","ISLB(Islami Bank Bangladesh)","RAKC(Rak CeramicBangladesh)","BEXi(Bangladesh Export Import company)","HBCB(Heidelberg Cement Bangladesh)","BSCC(Bangladesh Submarine Cable)","BATC(British American tobacco bangladesh )","BSRR(Bangladesh steel rolling mills)","MARI(Marico Bangladesh)","BGLA(Bangladesh Lamps)","ATBG(Atlas bangladesh ltd)","BDAT(Bangladesh autocar ltd)","LIND(Linde bangladesh ltd)"]
stock_index=["SGBD","MJLB","BATA","ISLB","RAKC","BEXi","HBCB","BSCC","BATC","BSRR","MARI","BGLA","ATBG","BDAT","LIND"]
models=['Linear Regression','k-Nearest Neighbors','Auto ARIMA','Long Short Term Memory (LSTM)']
st.sidebar.title("Company Name")
get_name=st.sidebar.selectbox("stock name",stock_name)
st.sidebar.title("Machine learning model")
model=st.sidebar.selectbox("select model",models)

summery=["Singer (Bangladesh) Ltd. engages in the manufacture and marketing of televisions, air conditioners, furniture, and sewing machines. It operates through the following business segments: Home Appliances, Consumer Electronics, Sewing, and Other. The company was founded on September 4, 1979 and is headquartered in Dhaka, Bangladesh.",
         "MJL Bangladesh Ltd. engages in the process, manufacture, and trade of lubricants and grease products. It offers engine oils for vehicles, marine transportation, aviation, and industrial activities. The company was founded on December 3, 1998 and is headquartered in Dhaka, Bangladesh.",
         "Bata Shoe Co. (Bangladesh) Ltd. engages in the manufacturing and retailing of footwear products. The company offers a number of designer collections for men, women and children. It also markets renowned brands such as Bata Comfit, Marie Claire, Hush Puppies, Scholl, Nike, Bubblegummers, Sandak, Weinbrenner, and B'first to name a few. The company operates its business through two segments: Domestic and Unallocated. The Domestic segment manufactures and markets leather, rubber, plastic and canvass footwear, hosiery and accessories as well as finished leather. The company was founded in 1894 and is headquartered in Gazipur, Bangladesh.",
         "Islami Bank Bangladesh Ltd. engages in the provision of commercial banking services. It offers deposit, investment, rural development scheme, non-resident Bangladeshi, foreign exchange business, locker, and offshore banking service. The company was founded on March 13, 1983 and is headquartered in Dhaka, Bangladesh.",
         "RAK Ceramics (Bangladesh) Ltd. engages in the manufacture and marketing of ceramics tiles, bathroom sets, and all types of sanitary ware. It operates through the following segments: Ceramics and Sanitary Ware, Power and Security and Services. The Ceramics and Sanitary Ware segment manufactures and markets ceramics tiles, bathroom sets, and all types of sanitary ware. The Power segment sets up power utilities and operates power-generating plants, transmission system, and distribution system and sells the generated electric power to any legal entity. The Security and Services segment provides security guarding, cleaning services, termite and pest control services, and manpower technical training. The company was founded on November 26, 1998 and is headquartered in Dhaka, Bangladesh.",
         "Bangladesh Export Import Company Limited, together with its subsidiaries, engages in investment operation, agency, and trading in other commodities and produces in Bangladesh and internationally. It manufactures and markets cotton and polyester blended garments for men, women, and children; and retails apparel under the Yellow brand name. The company also manufactures and markets porcelain and bone china tableware.",
         "HeidelbergCement Bangladesh Limited is a producer of cement in Bangladesh. The Company is engaged in manufacturing and marketing of gray cement under Ruby and Scan cement brands. The Company's products include cement, ready-mixed concrete, aggregates and related activities. The Company's projects include Bijoy Sarani, Mohakhali Flyover, Lalon Shah (Pakshi) Bridge, Shah Amanat International Airport, Bahaddarhat Flyover, Third Karnaphuli Bridge, North South University, Chittagong Port Flyover, Karnaphuli Water Supply Project, GulistanJatrabary Flyover, Tongi Bhairab Double Track Project and Summit Meghnaghat Power Plant. The Company operates in approximately 40 countries. The total production capacity of its Dhaka and Chittagong plants is approximately 2,378,000 metric tons per annum.",
         "Bangladesh Submarine Cable Co. Ltd. engages in the provision of voice and data bandwidth services. Its services include international private leased circuits, internet service provider, and colocation services. The company was founded on June 24, 2008 and is headquartered in Dhaka, Bangladesh.",
         "British American Tobacco Bangladesh Co. engages in manufacturing of tobacco products. Its brand portfolio consists of Benson & Hedges, John Player Gold Leaf, Pall Mall, Capstan, Star, Pilot, Derby and Hollywood. The company was founded in 1910 and is headquartered in Dhaka, Bangladesh.",
         "Bangladesh Steel Re-Rolling Mills Ltd. engages in producing steel. The firm's products include Xtreme, Maxima, Ultima, Xtrong, and Centura. It rolls and markets sectional steels such as angles and channels and ribbed wire which are manufactured in separate plants. The company was founded by Taherali Alibhai Africawala in 1952 and is headquartered in Chattogram, Bangladesh.",
         "Marico Bangladesh Limited is a Bangladesh-based fast-moving consumer goods (FMCG) company operating in the beauty and wellness space. The Company offers products across various categories, including branded coconut oil, value added hair oil, hair dye, hair serum, edible oil and foods, male grooming, shampoo and skin care. The Company manufactures and markets products under the brands, such as parachute, parachute advanced beliphool, nihar shanti amla, parachute advanced extra care, parachute advanced enriched hair oil, hair code, hair code active, hair code keshkala, parachute advanced body lotion, saffola active, saffola masala oats, livon, mediker plus and set wet. The Company operates in Bangladesh, Egypt, India, Malaysia, the Middle East, South Africa and Vietnam. The Company sells its products through its own distribution channels consisting of sales depots located in Gazipur, Chittagong, Bogra, Jessore and Comilla. It is the subsidiary of Marico Limited",
         "Bangladesh Lamps Limited manufactures and sells lighting products in Bangladesh. The company offers electric bulbs under the Phillips and Transtec brand names; and compact fluorescent lamps, as well as luminaire, starters and light emitting diodes, and fluorescent tube lights under the Transtec brand name. It also imports and sells ballasts. The company was incorporated in 1960 and is headquartered in Dhaka, Bangladesh. Bangladesh Lamps Limited is a subsidiary of Transcom Limited",
         "Atlas Bangladesh Limited is a Bangladesh-based company engaged in assembling motor cycle and importing spare parts. The Company also manufactures and markets some of these spare parts locally. The Company's products include ZS 100-27, ZS125-68, ZS 150-58, ZOne T, Z ONE, ZS 110-56 and ZS 110-72. The Company markets assembled motors under ZONGSHEN brand. The Company's factory is located at Tongi, Gazipur, Bangladesh.",
         "The Bangladesh Autocars Ltd. was incorporated on 01 August, 1979 in Bangladesh as a Public Limited Company under the Companies Act, 1913 (Repealed in 1994) and its shares are listed in the Dhaka Stock Exchange Ltd. The Company produced three Wheelers Auto Tempo under technical Collaboration of Piaggio & C s.p.a (manufacturer of world famous Vespa Brand). Due to the government policy to ban two stroke three wheeled vehicles, the company had to stop production of three wheelers Auto Tempo during the year 1999. Now, the company has CNG Convert Workshop for the Vehicles and, CNG Refueling Station.",
         "Linde Bangladesh Ltd. engages in the production and distribution of industrial and medical gases, anesthesia, welding products and equipment and ancillary equipment. The firm also engages in the rental of cylinders for vacuum insulated evaporators. It operates through the following segments: Bulk Gases, Packaged Gases & Products and Healthcare. "]


st.title(get_name)
st.write(summery[stock_name.index(get_name)])
stcok_volume=st.sidebar.text_input('Input data volume:',200)
st.sidebar.title("Setting for RSI")

rsi_period=14
rsi_period=st.sidebar.slider("RSI period", 10, 50)
#rsi_period=st.sidebar.text_input('Input RSI period:',14)
rsi_volume=st.sidebar.text_input('Input RSI data volume:',100)
st.sidebar.title("Setting for MACD")
slow=st.sidebar.text_input('Input slow period:',26)
fast=st.sidebar.text_input('Input fast period:',12)
smooth=st.sidebar.text_input('Input smooth :',9)
st.sidebar.title("Setting for COPP")
copp_period=st.sidebar.slider("COPP n", 10, 50)
st.sidebar.title("Setting for EOM")
EOM_period=st.sidebar.slider("EOM n", 10, 50)
index=stock_name.index(get_name)
get_short=stock_index[index]
print(get_short)
df= investpy.get_stock_historical_data(stock=get_short,
                                        country='bangladesh',
                                        from_date='01/01/2010',
                                       to_date='01/01/2020')
st.title("Live Chart")
st.plotly_chart(livechart(df.tail(int(stcok_volume))))
col1, col2 = st.beta_columns(2)
if model=='Linear Regression':
    data=refine(df)
    rest=linear_reg(data[0],data[1],data[2],data[3])
    with col1:
        st.write("Resulting value ",rest[1])
        st.dataframe(data=rest[0], width=None, height=None)
    with col2:
        st.title("Linear Regression Chart")
        st.pyplot(L_plot(rest[0],data[4],data[5],data[6]))

if model=='k-Nearest Neighbors':
    data=refine(df)
    rest=K_training(data[0],data[1],data[2],data[3])
    st.write("Resulting value",rest)
    with col1:
        st.write("Resulting value ",rest[1])
        st.dataframe(data=rest[0], width=None, height=None)
    with col2:
        st.title("k-Nearest Neighbors Chart")
        st.pyplot(K_plot(rest[0],data[4],data[5],data[6]))
        
if model=='Auto ARIMA':

    data=refine(df)
    rest=arima_training(data[6],data[5])
    st.write("Resulting value",rest)
    with col1:
        st.write("Resulting value ",rest[1])
        st.dataframe(data=rest[0], width=None, height=None)
    with col2:
        #st.pyplot(arima_plot(rest[0],data[4],[5],data[6]))
        st.write("Resulting value ", rest[1])

if model == 'Long Short Term Memory (LSTM)':
    rest = lstm_training(df)
    data = refine(df)
    with col1:
        st.write("Resulting value ")
        st.dataframe(data=rest, width=None, height=None)
    with col2:
        st.title("Long Short Term Memory (LSTM) Chart")
        st.pyplot(lstm_chart(data[4],rest))


    



df['RSI']=rsiFunc(df['Close'],n=int(rsi_period))


search_result = investpy.search_quotes(text=get_short, products=['stocks'],
                                       countries=['bangladesh'], n_results=1)
technical_indicators = search_result.retrieve_technical_indicators(interval="daily")
indicators=pd.DataFrame(technical_indicators)
st.title("Important Indicator and Stock Signal ")
st.dataframe(data=indicators, width=None, height=None)

st.title("RSI Chart")
st.write("The relative strength index (RSI) is a momentum indicator used in technical analysis that measures the magnitude of recent price changes to evaluate overbought or oversold conditions in the price of a stock or other asset. The RSI is displayed as an oscillator (a line graph that moves between two extremes) and can have a reading from 0 to 100.")
st.write("The primary trend of the stock or asset is an important tool in making sure the indicator’s readings are properly understood. For example, well-known market technician Constance Brown, CMT, has promoted the idea that an oversold reading on the RSI in an uptrend is likely much higher than 30% and that an overbought reading on the RSI during a downtrend is much lower than the 70% level.")

st.plotly_chart(ploty_graph(df.tail(int(rsi_volume))))


f=get_macd(df['Close'],int(slow),int(fast),int(smooth))
df=df.tail(200)
st.title("MACD Chart)")

st.write("Moving average convergence divergence (MACD) is a trend-following momentum indicator that shows the relationship between two moving averages of a security’s price. The MACD is calculated by subtracting the 26-period exponential moving average (EMA) from the 12-period EMA.")
st.write("MACD is often displayed with a histogram (see the chart below) which graphs the distance between the MACD and its signal line. If the MACD is above the signal line, the histogram will be above the MACD’s baseline. If the MACD is below its signal line, the histogram will be below the MACD’s baseline. Traders use the MACD’s histogram to identify when bullish or bearish momentum is high.")
st.plotly_chart(ploty_mcd(df,f))

st.write("The Coppock Curve is a long-term price momentum indicator used primarily to recognize major downturns and upturns in a stock market index. It is calculated as a 10-month weighted moving average of the sum of the 14-month rate of change and the 11-month rate of change for the index. It is also known as the Coppock Guide")
st.write("Apply the Coppock Curve to a monthly price chart of a stock index or stock index exchange traded fund (ETF). The general strategy is to buy when the Curve rises above the zero line and consider selling when the Curve falls below zero. For investors who already own the ETF, when the Coppock curve is above zero the indicator is signaling to hold onto the investment.")
df['COPP']=COPP(df,copp_period)
st.title("COPP Chart)")
st.plotly_chart(coppcurve(df))
d=EOM(df,14)

st.title("Ease of Movement")
st.write("Richard Arms' Ease of Movement indicator is a technical study that attempts to quantify a mix of momentum and volume information into one value. The intent is to use this value to discern whether prices are able to rise, or fall, with little resistance in the directional movement. Theoretically, if prices move easily, they will continue to do so for a period of time that can be traded effectively")
st.write("")
st.plotly_chart(movingcurve(d,EOM_period))

