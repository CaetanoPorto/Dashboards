import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title = 'Dashboard de vendas por mês' , layout = 'wide')

df = pd.read_csv("supermarket_sales.csv", sep = ';' , decimal = ',')

# Fizemos isso pois estava em type object
df['Date'] = pd.to_datetime(df['Date']) 

# Ordenando a base inteira pela data
df = df.sort_values(by = 'Date') 

# Agora vamos ordenar nosso df por mês (não por dia)
df['Month'] = df['Date'].apply(lambda x : str(x.year) + "-" +  str(x.month) )

# Criando uma caixa de seleção de cada mês
month = st.sidebar.selectbox("Mês" , df['Month'].unique())

# Criando Filtro do mês

df_filtered = df[df['Month'] == month]
df_filtered

# Agora vamos fazer colunas / divisões da tela duas em cima e 3 embaixo para colocar nossos gráficos

# Ele separar a tela em quantidade de colunas que vc definiu

col1 , col2 = st.columns(2)
col3 , col4 , col5 = st.columns(3)

#  Agora vamos montar nossos gráficos

# Data por total de vendas
fig_date = px.bar(df_filtered , x = 'Date' , y = 'Total' , 
                  color = 'City' , title =  'Faturamento por dia')

col1.plotly_chart(fig_date, use_container_width = True)

# Data por total de faturamete por prdouto
fig_prod = px.bar(df_filtered , x = 'Date' , y = 'Product line' , 
                  color = 'City' , title =  'Faturamento por Tipo de Produto' , 
                  orientation = 'h')

col2.plotly_chart(fig_prod, use_container_width = True)

# Data por contribuição de filial

# Aqui vamos juntar todas as filiais e somar o total de contribuição de cada uma
city_total = df_filtered.groupby('City')[['Total']].sum().reset_index()

fig_city = px.bar(city_total , x = 'City' , y = 'Total' , 
                  title =  'Faturamento por Filial' )

col3.plotly_chart(fig_city, use_container_width = True)

# Faturamento por tipo de pagamento 

fig_kind = px.pie(df_filtered , values = 'Total' , names =  'Payment' , 
                  title =  'Faturamento por Tipo de Pagamento' )

col4.plotly_chart(fig_kind, use_container_width = True)

# Média por cidade

city_mean = df_filtered.groupby('City')[['Rating']].mean().reset_index()

fig_mean = px.bar(city_mean , x = 'City' , y = 'Rating' , 
                  title =  'Avaliação' )

col5.plotly_chart(fig_mean, use_container_width = True)

# Use_container_width usado apenas para ficar bunitinho na tela
# Para rodar esses código é necessário ir no terminal e colocar 'streamlit run nome do arquivo'